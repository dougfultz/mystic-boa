#rss-get

import os
import feedparser

#initialization
workingDir="/home/videos"

curFeed=feedparser.parse("http://revision3.com/diggnation/feed/quicktime-high-definition")

os.chdir(workingDir)

print "Checking if directory, "+curFeed.feed.title+", exists."
if (os.path.exists(curFeed.feed.title)==False):
    print "\tDirectory does not exist, creating it.\n"
    os.mkdir(curFeed.feed.title)
else:
    print "\tDirectory Exists.\n"
    
#loop through entries in feed
for i in range(24,len(curFeed['entries'])):
    print curFeed.entries[i].title
    print curFeed.entries[i].enclosures[0].href
    print curFeed.entries[i].enclosures[0].length
    print curFeed.entries[i].enclosures[0].type