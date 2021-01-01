Programming Should Be For Everybody: An Example

--

I've long been a proponent (admittedly, not a particularly vocal one) that everyone should learn to code at least a little.  I don't mean in the sense of the "You lost your job, so learn to code" buffoonery, just because coding *professionally* isn't for everyone.  That said, even if you have zero intention of using code professionally, it can be very handy to learn, say, a little bit of Python to get a job done.

What I have to present to you today is an example of how code can be a useful tool in your belt.  This is just one of many instances of my using Python to demonstrate achieving a goal that would be difficult to do manually, whether you're a professional developer or not.  (And I don't actually write Python professionally-- My professional work is PHP, which is very different.)

There's a background to this that's relevant here.  One of my Sunday School teachers made a passing comment at the Christmas party that he'd like to see a list of every question asked in the Bible.  I thought to myself, "That should be easy, since every question ends with a question mark", and I said I could probably do that with a Python script.  He said he'd pay me if I did it, and I said it wasn't necessary since it would be only about five lines of Python.

Well, it turned out *not* to be five lines of Python, but it was a pretty fun project in any case.

More importantly, though, it's a great example of something that I could do because I knew how to write code, and why I think it would be beneficial for anybody to learn to code.

Essentially, code does nothing more than automate a monotonous task.  So, something like finding every question in the Bible could be done by taking out a Bible and a sheet of paper, and painstakingly finding every single question, as a months-long task that in ages past would be performed by monks with nothing better to do (or by Strong, whoever that is).  Or you could write a Python script that does all of it for you in seconds.

So, I took on the task during the week between Christmas and New Years, and this is how I did it.  (I didn't spend the whole week doing it, ftr.)

First off, I needed to use the World English Bible translation (WEB).  The reason for this is that it is a modern language translation that is public domain.  I could hypothetically do some webscraping and get the entirety of the ESV, but that would be legally sketchy at best.

I was disappointed to find that the current organization of the WEB in html is not terribly programmer-friendly.  It's far from *horrendous*, but I was expecting each verse to be in its own span or div, with an appropriate class name.  Instead, the chapter and verse numbers themselves are in these divs/spans, and interspersed throughout the text.  It makes perfect sense if you're reading it in a browser, but makes things slightly difficult from a programmatic perspective.  So, the first thing I did was reorganize everything-- All of the WEB (just the Protestant canon) as an XML file.  This is the first script, `reorganizeasxml.py`, and was the bulk of the work done.

To do this, I used the [archive of the html version of the WEB](https://ebible.org/Scriptures/eng-web_html.zip).  To run the first script to generate the XML, unzip the contents of that archive into a folder, drop `reorganizeasxml.py` into the directory, and run it.  It will create `complete.xml`-- One giant XML file containing the entire WEB translation, in a programmer-friendly XML format.

It's about five MB in size, so I do not recommend trying to open it in Notepad or any other text editor that's not designed for large files (I used `less` to view the contents).

I could have made this easier, theoretically, by using the plaintext version, which *seems* to have one verse per line.  I decided against that, though, because I'm not 100% sure that it's always the case that it's one verse per line-- It never explicitly says so-- and since the file names seem to indicate to me that these files exist for the purpose of reading out loud, so I expect they're not necessarily going to be particularly careful about line breaks.  I think, then, that it would be better to put in the extra effort in the clearer source material.  (And, honestly, a big part of my motivation here is that doing it the hard way is a lot more fun.)

`reorganizeasxml.py` loops through every file, uses BeautifulSoup to identify where every verse begins and ends, and dumps every verse into the output file, in (Protestant) canonical order.  This is mostly pretty easy-- The only thing that was mildly difficult is getting the end of the final verse, because the text content of each chapter is not organized into one big div, so I had to find where the site navigation began instead.  Apart from that, it's pretty straightforward.

After running `reorganizeasxml.py`, we have `complete.xml`.  We can now run `findallquestions.py`, which is significantly simpler overall, and doesn't even define any functions.  It doesn't need to because of how `reorganizeasxml.py` built the xml structure.

It starts out by finding every `vs` element that contains a question mark.  Then it creates a csv file, creates a header line, and then dumps all of the information into that csv file, one line at a time.  Bam.  Done.

What this script does *not* do is identify the one asking or the one being asked.  I think I'd have to use some AI/ML for that, and I've never done anything with that.  For that reason, those columns are blank, to be filled in manually.  (I don't actually expect that that would ever be 100% completed.)

Well, there you go.  There's a case study in a one-off use of Python code to accomplish a task that would be a pain to do manually.  It's just one example of how coding can be useful in day-to-day things, whether you're a developer or not.

Another example is [something that I made using matplotlib](https://github.com/anorman728/oklahomacovid19) when the Covid panic started.  The only historical data Oklahoma gave us at the time was the the cumulative case count, but I had a friend that wanted a graph of the daily case count.  Converting the raw data from cumulative to daily was easy, so I made a graph in matplotlib, then made a script to scrape the website and update the chart on Github.  I then made a cron job on my laptop to update it daily.  It was a fun project, but only lasted about a week before the Oklahoma health dept changed the format of the website so it stopped working.  At that point, they started giving us the chart exactly as we wanted it anyway, so there wasn't much point in fixing it.

The Bible questions scripts probably seem overwhelming to someone new to coding, but I can assure you that, given time, writing code becomes as natural as breathing.  What's hard today is easy tomorrow (which I keep telling myself while learning C++).  I've learned that lesson repeatedly a million times.
