import csv
import os

from bs4 import BeautifulSoup as BSoup
from string import Template

# Read and parse the complete xml.
print('Reading file.')

f = open('./complete.xml', 'r')
xmlRaw = f.read()
f.close()

soup = BSoup(xmlRaw, 'lxml')


# Get all the questions (according to the question marks).
print('Getting all verses that have "?" in them.')
allQs = [verse for verse in soup.find_all('vs') if '?' in verse.text]
# Surprisingly, this doesn't take a massive amount of time.


# Write all questions to CSV file.
outputfilename = './allquestions.csv'
print('Writing to output file: ' + outputfilename + '.')

if os.path.exists(outputfilename):
    os.remove(outputfilename)

outFile = open(outputfilename, 'a', newline='\n')
out = csv.writer(outFile)
out.writerow(['Book','Chapter','Verse','Asker','Asked','Link','Content'])

for vs in allQs:
    print('.', end='')
    ch = vs.parent
    bk = ch.parent

    urlTemp = Template('https://www.blueletterbible.org/esv/$bk/$ch/$vs')
    url = urlTemp.substitute(bk=bk.attrs['name'], ch=ch.attrs['num'], vs=vs.attrs['num'])

    out.writerow([bk.attrs['name'], ch.attrs['num'], vs.attrs['num'], '', '', url, vs.text])

outFile.close()

print('')
print('Done')
