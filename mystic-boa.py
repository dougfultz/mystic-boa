#!/usr/bin/python

#mystic-boa

import os
import feedparser

#initialization
workingDir="/home/videos"
feeds=["http://revision3.com/diggnation/feed/quicktime-high-definition","http://revision3.com/diggreel/feed/quicktime-high-definition","http://revision3.com/epicfu/feed/quicktime-large","http://revision3.com/hak5/feed/quicktime-large","http://revision3.com/internetsuperstar/feed/quicktime-high-definition","http://revision3.com/internetsuperstar/feed/quicktime-high-definition","http://revision3.com/rev3gazette/feed/quicktime-high-definition","http://revision3.com/scamschool/feed/quicktime-high-definition","http://revision3.com/systm/feed/quicktime-high-definition","http://revision3.com/tekzilla/feed/quicktime-high-definition","http://revision3.com/trs/feed/quicktime-high-definition","http://revision3.com/webdrifter/feed/quicktime-high-definition","http://revision3.com/winelibrarytv/feed/quicktime-high-definition"]

print "Mystic-Boa"

for curFeedNum in range(0,len(feeds)):
    os.chdir(workingDir)
    print "Downloading and parsing - "+feeds[curFeedNum]
    curFeed=feedparser.parse(feeds[curFeedNum])
    
    print "Checking if directory, "+curFeed.feed.title+", exists."
    if (os.path.exists(curFeed.feed.title)==False):
        print "\tDirectory does not exist, creating it.\n"
        os.mkdir(curFeed.feed.title)
    else:
        print "\tDirectory Exists.\n"
    os.chdir(workingDir+"/"+curFeed.feed.title)
        
    #loop through entries in feed
    for item in range(0,len(curFeed['entries'])):
        print curFeed.entries[item].title
        for enc in range(0,len(curFeed.entries[item].enclosures)):
            print "Downloading - "+curFeed.entries[item].title
            os.system("wget -c "+curFeed.entries[item].enclosures[enc].href)
            print "Finished Downloading - "+curFeed.entries[item].title
        print "\n\n\n\n"
