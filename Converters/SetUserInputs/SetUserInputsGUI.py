#!/usr/bin/env python
# -*- coding: cp1252 -*-
# Contact: Will Wade <will@e-wade.net>
# Date: July 2014
# Binary: pyinstaller.py --icon=SetUserInputsGui/icon_256px.ico --onefile --nowindow --noconsole SetUserInputsGUI.py
# -*- coding: iso-8859-15 -*-
"""
SetUserInputs. Copy one Grid 2 user input methods to all the rest.  
"""
from easygui import *
# For the line command aspects
import sys
import os.path
from lxml import etree

readme = """
This application simply looks for your Grid 2 Users directory (where all the raw data is held on your grid bundles) and then asks you to select a user to base all other users Input methods on.

For example. Say you have a device you have recently setup for one user and you wish that user to use the same access method for all grid bundles on that machine.
Currently you would have to manually edit each user in the Grid. Now just edit one user, run this tool, select the User you have just edited and then the rest of them will get these settings transferred.

NB: It can take a little while. 
NB2: Please please backup your users directory if you have any concerns
NB3: If it can't find your users directory it will ask you to locate it. To find it go to the Grid 2. Go to File menu, then Preferences and look at the "File Locations". You want the field that says 'Location for user files:'

Any issues feel free to send them to Will @ ACE and I will try and fix (but if your Grid stops working I can't take responsibility! See NB2!)

Press OK in the top right to continue.. 
"""


def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]
            
def findPotentialDirs(dirs={}):
    """ Looks through a list of potential directories. This does seem to take an age """
    found = False
    foundDirs = []
    for dir in dirs:
        if os.path.isdir(dir):
            for r,d,f in walklevel(dir,2): 
                # is d a potential grid 2 dir?  - look for a settings.xml
                for files in f:
                    if files.endswith("settings.xml"):
                        found = True
                        if dir not in foundDirs:                
                            foundDirs.append(dir)
                        # This may speed things up a bit.. 
                        break
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
    for r,d,f in walklevel(gridDir,2):                                  
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
        for r,d,f in walklevel(dir,2): 
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

    textbox('',"Grid 2 User Input copier",readme)
    found, userdirs = findPotentialDirs({os.path.normpath("C:\Users\Public\Documents\Sensory Software\The Grid 2\Users"),os.path.normpath("/Users/willwade/bin/AAC-Tools/temp/Grids/")})
    if found:
        if len(userdirs) > 1:
            # Ask which dir to choose
            msg ="Which is the user directory you wish to use?"
            title = "Grid2 User Input Copier - Select User directory"
            userdirs = choicebox(msg, title, userdirs)
    else:
        #
        msg = "No usual directories were found for the Grid 2 User settings. Can you locate the Users Directory you wish to use?" 
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
    msg ="Choose a User to copy Input methods from"
    title = "Grid2 User Input Copier"
    userDir = choicebox(msg, title, choices)
    if userDir == None:
            sys.exit(0)           # user chose Cancel
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
    