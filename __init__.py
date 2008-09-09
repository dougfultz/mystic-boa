#mystic-boa

import os
import feedparser

#initialization
workingDir="/home/videos"
feeds=["http://revision3.com/diggnation/feed/quicktime-high-definition","http://revision3.com/trs/feed/quicktime-high-definition"]
itemTypes=["video/quicktime"]
wgetLocation="wget"
wgetOptions="-c"

for curFeedNum in range(0,len(feeds)):
    os.chdir(workingDir)
    
    curFeed=feedparser.parse(feeds[curFeedNum])
    print "Processing... "+curFeed.feed.title
    print "\tChecking if directory, "+curFeed.feed.title+", exists."
    if (os.path.exists(curFeed.feed.title)==False):
        print "\tDirectory does not exist, creating it."
        os.mkdir(curFeed.feed.title)
    else:
        print "\tDirectory Exists."
    os.chdir(workingDir+"/"+curFeed.feed.title)
        
    #loop through entries in feed
    for item in range(24,len(curFeed['entries'])):
        print "Processing... "+curFeed.entries[item].title
        for enc in range(0,len(curFeed.entries[item].enclosures)):
            temp=curFeed.entries[item].enclosures[enc].href.split("/")
            
            if (curFeed.entries[item].enclosures[enc].type in itemTypes) and (os.path.exists(temp[len(temp)-1])==False):
                print "\tDownloading - "+curFeed.entries[item].title
                os.system(wgetLocation+" "+wgetOptions+" "+curFeed.entries[item].enclosures[enc].href)
                print "\tFinished Downloading - "+curFeed.entries[item].title
            else:
                print "\t"+curFeed.entries[item].title+" already exists."
        print "\n\n\n\n"