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
lockFile="mystic-boa.lock"
numItems=None
errors=[]

#----------------------------------------------------------------------------
def checkCreateDir(path, dirName):
    """Checks to verify that the directory exists.  If the directory does not exist then create the directory."""
    print "Checking if directory, "+dirName+", exists."
    if (os.path.exists(dirName)==False):
        print "\tDirectory does not exist, creating it.\n"
        os.mkdir(dirName)
    else:
        print "\tDirectory Exists."
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
    rc=os.system("wget -c -q "+fileURL)
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
    rc=None
    print "\nDownloading and parsing - "+curFeedURL

    rc=os.system("wget -q -O "+tempDir+"/rss.xml "+curFeedURL)
    if (rc==0):
        curFeed=feedparser.parse(tempDir+"/rss.xml")
    else:
        print "Trying old method..."
        curFeed=feedparser.parse(curFeedURL)

    checkCreateDir(workingDir,curFeed.feed.title)
    os.chdir(workingDir+"/"+curFeed.feed.title)

    #loop through entries in feed
    for item in range(0,numItems):
        try:
            for enc in range(0,len(curFeed.entries[item].enclosures)):
                if(os.path.exists(getFileName(curFeed.entries[item].enclosures[enc].href))==True):
                    print getFileName(curFeed.entries[item].enclosures[enc].href)+" already exists."
                else:
                    downloadFile(curFeed.entries[item].title,curFeed.entries[item].enclosures[enc].href)
        except:
            print "Error Occurred."

    #remove old files
    for item in range(numItems,numItems+10):
        try:
            for enc in range(0,len(curFeed.entries[item].enclosures)):
                if(os.path.exists(getFileName(curFeed.entries[item].enclosures[enc].href))==True):
                    print "Removing "+os.getcwd()+"/"+getFileName(curFeed.entries[item].enclosures[enc].href)
                    #remove file
                    try:
                        os.remove(os.getcwd()+"/"+getFileName(curFeed.entries[item].enclosures[enc].href))
                    except:
                        print "Error removing "+os.getcwd()+"/"+getFileName(curFeed.entries[item].enclosures[enc].href)
        except:
            #print "Error Occured."
            pass
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
                if not line.startswith('#'):
                    goodItems.append(line.lstrip("feedURL="))
                #item=item.split('=')
                #if (item[0]=="feedURL"):
                #    goodItems.append(item[1])
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
    global numItems
    tempDir=ini.get("global","tempDir")
    numItems=ini.get("global","numItems")
    try:
        numItems=int(numItems)
    except:
        numItems=0
    if (os.path.exists(tempDir)==False):
        print tempDir+" is not a valid path.  Please edit the config or create the directory."
        goodList.append(False)
        tempDir=None
    if (numItems<=0):
        print "numItems, must be 1 or greater."
        goodList.append(False)
        numItems=None
    for good in goodList:
        if (good==False):
            return good
    return True
#----------------------------------------------------------------------------
def runLock():
    """Checks to see if other instances are running, if not create run lock."""
    if (not tempDir==None):
        if (os.path.isfile(tempDir+"/"+lockFile)==False):
            #create lock with pid written to file
            f = open(tempDir+"/"+lockFile,'w')
            f.write(str(os.getpid()))
            return True
        else:
            print "Another instance may already be running.  If this is in error please delete this file: "+tempDir+"/"+lockFile
    return False
#  MAIN  ####################################################################

print "Mystic-Boa"

try:
    if (setGlobals()==True and runLock()==True):
        for curSection in getSections():
            for curFeed in getFeeds(curSection):
                try:
                    processFeed(curSection,curFeed)
                except AttributeError, detail:
                    print "An error has occured.\n"+curFeed
                    print detail
                    os.system("sleep 5s")
                    errors.append(curFeed+" has had an error")
        os.remove(tempDir+"/"+lockFile)
        os.remove(tempDir+"/rss.xml")
except KeyboardInterrupt:
    print "Canceled by user."
    os.remove(tempDir+"/"+lockFile)
    os.remove(tempDir+"/rss.xml")

print "Errors:\n",errors
