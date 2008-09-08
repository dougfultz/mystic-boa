#mystic-boa

import os
import feedparser

#initialization
workingDir="/home/videos"
feeds=["http://revision3.com/diggnation/feed/quicktime-high-definition","http://revision3.com/trs/feed/quicktime-high-definition"]
itemTypes=["video/quicktime"]

for curFeedNum in range(0,len(feeds)):
    os.chdir(workingDir)
    
    curFeed=feedparser.parse(feeds[curFeedNum])
    
    print "Checking if directory, "+curFeed.feed.title+", exists."
    if (os.path.exists(curFeed.feed.title)==False):
        print "\tDirectory does not exist, creating it.\n"
        os.mkdir(curFeed.feed.title)
    else:
        print "\tDirectory Exists.\n"
    os.chdir(workingDir+"/"+curFeed.feed.title)
        
    #loop through entries in feed
    for item in range(24,len(curFeed['entries'])):
        print curFeed.entries[item].title
        for enc in range(0,len(curFeed.entries[item].enclosures)): 
            print enc
            print curFeed.entries[item].enclosures[enc].href
            print curFeed.entries[item].enclosures[enc].type
            if (curFeed.entries[item].enclosures[enc].type in itemTypes):
                print "Downloading - "+curFeed.entries[item].title
                os.system("wget -c "+curFeed.entries[item].enclosures[enc].href)
                print "Finished Downloading - "+curFeed.entries[item].title
        print "\n\n\n\n"