#!/usr/bin/python

#mystic-boa

import os
import feedparser
import ConfigParser

#initialization
configFile=os.getcwd()+"/mystic-boa.conf"
ini=ConfigParser.SafeConfigParser()
ini.read(configFile)
tempDir=None
errors=[]

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
def getFileName(URL):
	URL=URL.split('/')
	return URL[len(URL)-1]
#----------------------------------------------------------------------------
def downloadFile(title,fileURL):
	"""Output to user, download the file, output to user"""
	global errors
	rc=None
	downloadDir=os.getcwd()
	os.chdir(tempDir)
	print "Downloading content - "+title
	rc=os.system("wget -c "+fileURL)
	if (rc==0):
		try:
			print "Moving "+getFileName(fileURL)+" from "+tempDir+" to "+downloadDir+"."
			for filename in os.listdir('.'):
				if (filename.startswith(getFileName(fileURL))==True):
					os.rename(filename,getFileName(fileURL))
			os.system("mv \""+tempDir+"/"+getFileName(fileURL)+"\" \""+downloadDir+"/\"")
		except:
			print "move failed"
			errors.append(getFileName(fileURL)+"move failed")
	print "Finished Downloading content - "+title
	os.chdir(downloadDir)
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
			if(os.path.exists(getFileName(curFeed.entries[item].enclosures[enc].href))==True):
				print getFileName(curFeed.entries[item].enclosures[enc].href)+" already exists."
			else:
				downloadFile(curFeed.entries[item].title,curFeed.entries[item].enclosures[enc].href)
#---------------------------------------------------------------------------
def getSections():
	"""Reads the config file and returns a list of the sections."""
	goodSections=[]
	for folder in ini.sections():
		if (os.path.exists(folder)==True):
			goodSections.append(folder)
		elif (folder=="global"):
			pass
		else:
			print "Section "+folder+" is not a valid path.  Please edit the config or create the directory."
			os.system("sleep 60s")
	return goodSections
#----------------------------------------------------------------------------
def getFeeds(section):
	"""Returns the list of feeds in the current section."""
	f = open(configFile)
	try:
		for line in f:
			goodItems = []
			section="["+section+"]"
			while section not in line:
				line = f.next()
			line = f.next()
			while not line.startswith('['):
				item=line.strip()
				item=item.split('=')
				if (item[0]=="feedURL"):
					goodItems.append(item[1])
				line = f.next()
			break
	except StopIteration:
		pass
	f.close()
	return goodItems
#----------------------------------------------------------------------------
def setGlobals():
	"""Checks all values from global section to verify that the config is correct."""
	goodList=[]
	global tempDir
	tempDir=ini.get("global","tempDir")
	if (os.path.exists(tempDir)==False):
		print tempDir+" is not a valid path.  Please edit the config or create the directory."
		goodList.append(False)
		tempDir=None
	for good in goodList:
		if (good==False):
			return good
	return True
#  MAIN  ####################################################################

print "Mystic-Boa"

try:
	if (setGlobals()==True):
		for curSection in getSections():
			for curFeed in getFeeds(curSection):
				try:
					processFeed(curSection,curFeed)
				except AttributeError, detail:
					print "An error has occured.\n"+curFeed
					print detail
					os.system("sleep 30s")
					errors.append(curFeed+" has had the following error "+detail.args)
except KeyboardInterrupt:
	print "Canceled by user."

print "Errors:\n",errors
