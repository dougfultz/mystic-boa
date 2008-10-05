#!/usr/bin/python

#mystic-boa

import os
import feedparser
import ConfigParser

#initialization
configFile="./mystic-boa.conf"
ini=ConfigParser.ConfigParser()
ini.read(configFile)

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
def processFeed(workingDir, curFeedURL):
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
#---------------------------------------------------------------------------
def getSections():
	"""Reads the config file and returns a list of the sections."""
	goodSections=[]
	for folder in ini.sections():
		if (os.path.exists(folder)==True):
			goodSections.append(folder)
		else:
			print "Section "+folder+" is not a valid path.  Please edit the config or create the directory."
			os.system("sleep 60s")
	return goodSections
#----------------------------------------------------------------------------
def getFeeds(section):
	"""Returns the list of feeds in the current section."""
	goodItems=[]
	for item in ini.items(section):
		goodItems.append(item[len(item)-1])
	return goodItems
#  MAIN  ####################################################################

print "Mystic-Boa"

for curSection in getSections():
	for curFeed in getFeeds(curSection):
		processFeed(curSection,curFeed)
