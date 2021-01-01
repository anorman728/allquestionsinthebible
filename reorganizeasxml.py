# This needs to be copied into a directory that contains all the files from this
# archive:
# https://ebible.org/Scriptures/eng-web_html.zip

# Running this script will create one giant XML file that contains the whole
# World English Bible (about 5MB).

import os
import re

from bs4 import BeautifulSoup as BSoup

'''
The path of the output filename.
'''
outputfilename = './complete.xml'

# Delete this file if it exists.
if os.path.exists(outputfilename):
    os.remove(outputfilename)

'''
The actual file output stream.  (Just declaring and opening it for now so it's
in the scope.)
'''
outputfile = open(outputfilename, 'a')


def main():
    '''
    Main method, just so I don't have to write this at the bottom of the script.
    '''

    appendToFile('<?xml version="1.0" encoding="UTF-8"?>')
    appendToFile('<web>')

    # Get the files and order them.  (Not efficient, at all, but works.)
    files = [x for x in os.listdir('./') if x.endswith('.htm') and getNameAndChapter(x)[0] in bookOrder and getNameAndChapter(x)[1] != 0]
    files.sort(key = customOrder)

    currentBk = getNameAndChapter(files[0])[0]

    # Open first book.
    writeBookLineStart(currentBk)

    for filename in files:
        nameChap = getNameAndChapter(filename)

        # If new book, close old book and open new.
        if nameChap[0] != currentBk:
            currentBk = nameChap[0]
            writeBookLineEnd()
            writeBookLineStart(currentBk)

        writeChapterLineStart(nameChap[1])
        findAllVerses(filename)
        writeChapterLineEnd()

    # Close last book.
    writeBookLineEnd();

    appendToFile('</web>')

def appendToFile(string, indlvl = 0):
    '''
    Write to the output XML file, defining the indent level.
    '''
    outputfile.write((' ' * indlvl * 4) + string + '\n')


'''
List of books in the order they occur in (Protestant canon).
Excludes htm files in this directory that are not valid.

Not gonna lie.  This was a pain.  I don't know how to make this apart from
making it manually.
'''
bookOrder = [
'GEN', 'EXO', 'LEV', 'NUM', 'DEU', 'JOS', 'JDG', 'RUT', '1SA', '2SA', '1KI', # 11 columns here
'2KI', '1CH', '2CH', 'EZR', 'NEH', 'EST', 'JOB', 'PSA', 'PRO', 'ECC', 'SNG',
'ISA', 'JER', 'LAM', 'EZK', 'DAN', 'HOS', 'JOL', 'AMO', 'OBA', 'JON', 'MIC',
'NAM', 'HAB', 'ZEP', 'HAG', 'ZEC', 'MAL', 'MAT', 'MRK', 'LUK', 'JHN', 'ACT',
'ROM', '1CO', '2CO', 'GAL', 'EPH', 'PHP', 'COL', '1TH', '2TH', '1TI', '2TI',
'TIT', 'PHM', 'HEB', 'JAS', '1PE', '2PE', '1JN', '2JN', '3JN', 'JUD', 'REV']

def customOrder(filename):
    '''
    Convert a filename into a number for the purposes of ordering.
    '''

    nameChap = getNameAndChapter(filename)

    bkNum   = str(bookOrder.index(nameChap[0]) if nameChap[0] in bookOrder else -1)
    chForm  = str(nameChap[1]).zfill(3)

    # Note these are strings, not numbers, so they're appended!  But then we
    # convert back to integer so it sorts correctly, by number instead of
    # alphabetically by numeric strings.
    # It's weird and probably inefficient, but it's easy to understand and it
    # works.
    return int(bkNum + chForm)

def writeBookLineStart(bookname):
    appendToFile('<bk name="' + bookname + '">', 1)

def writeBookLineEnd():
    appendToFile('</bk>', 1)

def writeChapterLineStart(chnum):
    appendToFile('<ch num="' + str(chnum) + '">', 2)

def writeChapterLineEnd():
    appendToFile('</ch>', 2)

def findAllVerses(filename):
    '''
    Find all verses within an individual file and append them to the final
    csv file.
    '''

    namechap = getNameAndChapter(filename)

    if namechap[1] == 0:
        # This is a TOC file, so we skip it.
        # (Note from the future: This shouldn't ever actually happen anymore.)
        return

    soup = getBSoup(filename)

    print('Finding all verses in ' + namechap[0] + ' ' + str(namechap[1]) + '.')

    bounds = getBounds(soup)
    for i in range(0, len(bounds) - 1):
        appendToFile(buildVerse(str(soup)[bounds[i]:bounds[i+1]]), 3)

def getBSoup(filename):
    '''
    Create a BeautifulSoup object representing a particular file.
    '''
    f = open(filename, 'r')
    htmlRaw = f.read()
    f.close()

    return BSoup(htmlRaw, 'html.parser')

def getNameAndChapter(filename):
    '''
    Get name and chapter of the specified file as a list.

    Books without chapters (like 2 and 3 John) will always return chapter 1.
    (That's how they're defined by the WEB.)

    TOC files will return chapter 0.  (Their filename contains no number at
    all.)
    '''
    bk = re.findall('^\d?[a-zA-Z]+', filename)[0]

    chDum = re.findall('\d+\.htm', filename)
    ch = 0 if len(chDum) == 0 else int(chDum[0].rstrip('.htm'))
    # If there is no number found, hardcode return zero.

    return [bk, ch]

def getBounds(soup):
    '''
    Get the bounds (of str(soup), i.e., the soup converted to a string) where we
    would find the beginning and end of verses.
    '''
    bounds = [str(soup).find(str(verse)) for verse in soup.find_all(class_='verse')]
    bounds.sort()
    # Find everywhere in the chapter that the verse divisions are displayed.

    # Note: No two verses are identical because of the verse numbers at the
    # beginning, so even with repetition in Hebrew poetry, we don't need to
    # worry about that being a problem.

    # Still need to find final bound, because verse divisions only occur at
    # beginning of verse.
    bounds.append(getFinalBound(soup, bounds))

    return bounds

def getFinalBound(soup, existingBounds):
    '''
    Get the last bound. (Does not correspond to a 'verse' class, so it needs
    special treatment.)
    '''

    # Every chapter begins and ends with a navigation unordered list, so we can
    # find the first instance of that after the last verse.

    # Find all elements with class 'tnav'.
    navTags = {str(x) for x in soup.find_all(class_='tnav')}

    # Find iterators generating all instances of those elements in the master
    # string.
    eachNavTag = [re.finditer(re.escape(inst), str(soup)) for inst in navTags]

    # Use the iterators to actually find the starting points for all these
    # elements in the master string.
    # Note: Even if I figure out how to do this with a comprehension, it would
    # be difficult to read, so I'm keeping it in a loop.
    navTagInd = set() # Initialize.  Use set to avoid dupes.
    for iter01 in eachNavTag:
        navTagInd = navTagInd.union({x.start() for x in iter01})

    # Get all elements larger than the largest bound, then sort the list,
    # because...
    listdum = [x for x in navTagInd if (x > existingBounds[-1])]
    listdum.sort()

    # ...we want to get the *first* element that is *larger* than the bounds we
    # already have.
    return listdum[0]

def buildVerse(strInput):
    '''
    Take a raw string of the html verse and convert it to the raw string of the
    XML output.
    '''

    soupDum = BSoup(strInput, 'html.parser')

    verseSpan = soupDum.find('span', class_='verse')
    verseNum = int(verseSpan.text)
    # Convert to int partly to trim, also because I want to throw an exception
    # if it's not a valid int so I know about it.

    verseSpan.decompose()
    # Remove the span, because we don't want it in the element content.  It's
    # going to be an attribute.

    for note in soupDum.find_all('a', class_='notemark'):
        # Remove notes, at least for the moment.  May deal with them in future
        # revision.
        note.decompose()

    return '<vs num="' + str(verseNum) + '">' + soupDum.text.strip() + '</vs>'

main()

outputfile.close()
