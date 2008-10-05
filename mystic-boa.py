#!/usr/bin/python

#mystic-boa

import os
import feedparser

#initialization
workingDir="/home/videos"
feeds=["http://revision3.com/diggnation/feed/quicktime-high-definition","http://revision3.com/diggreel/feed/quicktime-high-definition"]
feeds2=["http://revision3.com/diggnation/feed/quicktime-high-definition","http://revision3.com/diggreel/feed/quicktime-high-definition","http://revision3.com/epicfu/feed/quicktime-large","http://revision3.com/hak5/feed/quicktime-large","http://revision3.com/internetsuperstar/feed/quicktime-high-definition","http://revision3.com/internetsuperstar/feed/quicktime-high-definition","http://revision3.com/rev3gazette/feed/quicktime-high-definition","http://revision3.com/scamschool/feed/quicktime-high-definition","http://revision3.com/systm/feed/quicktime-high-definition","http://revision3.com/tekzilla/feed/quicktime-high-definition","http://revision3.com/trs/feed/quicktime-high-definition","http://revision3.com/webdrifter/feed/quicktime-high-definition","http://revision3.com/winelibrarytv/feed/quicktime-high-definition"]
#----------------------------------------------------------------------------
def checkCreateDir(path, dirName):
	"""Checks to verify that the directory exists.  If the directory does not exist then create the directory."""
	print "Checking if directory, "+dirName+", exists."
	if (os.path.exists(dirName)==False):
		print "\tDirectory does not exist, creating it.\n"
		os.mkdir(dirName)
	else:
		print "\tDirectory Exists.\n"
#----------------------------------------------------------------------------
def downloadFile(title,fileURL):
	"""Output to user, download the file, output to user"""
	print "Downloading content - "+title
	os.system("wget -c "+fileURL)
	print "Finished Downloading content - "+title
#----------------------------------------------------------------------------
def processFeed(curFeedURL):
	"""Processes the current feed URL"""
	os.chdir(workingDir)
	print "Downloading and parsing - "+curFeedURL
	curFeed=feedparser.parse(curFeedURL)
    
	checkCreateDir(workingDir,curFeed.feed.title)
	os.chdir(workingDir+"/"+curFeed.feed.title)
        
	#loop through entries in feed
	for item in range(0,len(curFeed['entries'])):
		for enc in range(0,len(curFeed.entries[item].enclosures)):
			downloadFile(curFeed.entries[item].title,curFeed.entries[item].enclosures[enc].href)
		print "\n\n\n\n"
#  MAIN  ####################################################################

print "Mystic-Boa"

for curFeedNum in range(0,len(feeds)):
	processFeed(feeds[curFeedNum])
