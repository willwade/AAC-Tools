#!/usr/bin/env python
# -*- coding: cp1252 -*-
# Contact: Will Wade <will@e-wade.net>
# Date: July 2014

# -*- coding: iso-8859-15 -*-
"""
SetUserInputs. Copy one Grid 2 user input methods to all the rest.  

usage: SetUserInputs [-u] [--userdir=DIR] [--griddir=GRIDDIR] 

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show the version number of this script and exit
  --userdir=DIR         Allow from one or several ip-address. [default: .]
  --griddir=GRIDDIR        Change the default Mind Express Port number. [default: C:/Users/Documents/Whatever]
  
"""
from easygui import *
# For the line command aspects
import pdb
import sys
import os.path, errno, re
from lxml import etree
from lxml import objectify

def findPotentialDirs(dirs={}):
    """ Looks through a list of potential directories """
    found = False
    foundDirs = []
    for dir in dirs:
        for r,d,f in os.walk(dir): 
            # is d a potential grid 2 dir?  - look for a settings.xml
            for files in f:
                if files.endswith("settings.xml"):
                    found = True
                    if dir not in foundDirs:                
                        foundDirs.append(dir)
    return found, foundDirs
                    
def parseUserInputXML(userDir):
    """ Grab a userdir and then find the settings.xml and grab the Input tree """
    settingsf = userDir+os.sep+'Settings0'+os.sep+'settings.xml'
    if(os.path.isfile(settingsf)):    
        parser = etree.XMLParser(strip_cdata=False)
        tree = etree.parse(settingsf, parser)
        doc = tree.getroot()
        #return etree.tostring(tree.xpath('//input')[0])
        inputt =  doc.find('input')
        return inputt
    else:
        print 'Not a file:'+settingsf                   
        return False

def writeUserInput(inputXML, gridDir, excludeUser=None):
    """ Go through the User Dir and find all settings.xml and write over the new input settings"""
    # Go to the dir and loop through the directories looking for Settings0/settings.xml files
    writeFiles = 0
    for r,d,f in os.walk(gridDir):                                  
        page = os.path.split(r)[1]
        for files in f:

            if files.endswith("settings.xml"):
                settingsf = os.path.join(r,files)
                # Now find the input node and overwrite
                parser = etree.XMLParser(strip_cdata=False)
                tree = etree.parse(settingsf, parser)
                ## DO COPY here
                doc = tree.getroot()
                doc.remove(doc.find('input'))
                doc.append(inputXML)   
                # Now write it
                newxml = etree.tostring(tree, pretty_print=True)
                f = open(settingsf, 'w')
                f.write(newxml)
                writeFiles +=1
                f.close()
    return writeFiles

def getUsers(dirs={}):
    """ Look into directorys for any user folders """
    #b = dict()
    b = []
    found = False
    for dir in dirs:
        for r,d,f in os.walk(dir): 
            # is d a potential grid 2 dir?  - look for a settings.xml
            for files in f:
                if files.endswith("settings.xml"):
                    found = True
                    b.append(r.split(os.sep)[-2])
                    #b[r[:-9]] = r.split(os.sep)[-2]
    if found:
        return b 
    else:
        return None
            
if __name__ == '__main__':

    #inputXML = parseUserInputXML(args['--userdir'])
    # Now find other directories and copy it
    #writeUserInput(inputXML, args['--griddir'],args['--userdir'])
    # This should get all the User dirs in the Grid 2 dir. Provide all possible 
    
    found, userdirs = findPotentialDirs({os.path.normpath("C:\Users\Public\Documents\Sensory Software\The Grid 2\Users")})
    if found:
        if len(userdirs) > 1:
            # Ask which dir to choose
            msg ="Which is the user directory you wish to use?"
            title = "Grid2 User Input Copier - Select User directory"
            userdirs = choicebox(msg, title, dirs)
    else:
        #
        msg = "No usual directories were found for the Grid 2 User settings. Can you locate the User you wish to use?" 
        title = "Please provide a directory"
        msgbox(msg)
        tdir = diropenbox()
        # Now check dir is actually one..
        dirs = []
        dirs.append(tdir)
        found, userdirs = findPotentialDirs(dirs)
        if not found:
            msgbox('Sorry. That isnt a Grid 2 User directory. This program will now quit.')
            sys.exit(0)
    # Lets continue
    choices =  getUsers(userdirs)
    msg ="Choose a User to serve to copy Input methods from"
    title = "Grid2 User Input Copier"
    userDir = choicebox(msg, title, choices)
    # Now use choice as the one to use 
    # Lets double check
    msg = "Warning: The next step will overwrite ALL users with the same Input method. Want to continue? "
    title = "Please Confirm"
    if ccbox(msg, title):     # show a Continue/Cancel dialog
        pass  # user chose Continue
        inputXML = parseUserInputXML(userdirs[0]+os.sep+userDir)
        filesChanged = writeUserInput(inputXML,userdirs[0])
        msg = "Great. All of the User Input settings ("+ str(filesChanged)+" files) are now the same. Happy days."
        msgbox(msg)
    else:
        sys.exit(0)           # user chose Cancel
    # Lets continue
    