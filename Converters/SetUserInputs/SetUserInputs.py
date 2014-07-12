#!/usr/bin/env python
# -*- coding: cp1252 -*-
# Contact: Will Wade <will@e-wade.net>
# Date: July 2014

# -*- coding: iso-8859-15 -*-
"""
SetUserInputs. Copy one Grid 2 user input methods to all the rest.  

usage: SetUserInputs [-u] [--userdir=DIR] [--griddir=GRIDDIR] 

Runs a Mind Express Control Server.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show the version number of this script and exit
  --userdir=DIR         Allow from one or several ip-address. [default: .]
  --griddir=GRIDDIR        Change the default Mind Express Port number. [default: C:/Users/Documents/Whatever]
  
"""
# Utils
import sys
sys.path.append('../utils')
# For the line command aspects
try:
    from docopt import docopt
except ImportError:
    exit('This script requires that `docopt` library'
         ' is installed: \n    pip install docopt\n'
         'https://github.com/docopt/docopt')

import pdb
import os.path, errno, re
from lxml import etree
import getopt, sys, csv

def parseUserInputXML(userDir):
    """ Grab a userdir and then find the settings.xml and grab the Input tree """
    settingsf = userDir+'/Settings0/settings.xml'
    if(os.path.isfile(settingsf)):    
        parser = etree.XMLParser(strip_cdata=False)
        tree = etree.parse(settingsf, parser)
        return etree.tostring(tree.xpath('//input')[0])
    else:
        print 'Not a file:'+settingsf                   

def writeUserInput(inputXML, gridDir, excludeUser=None):
    """ Go through the User Dir and find all settings.xml and write over the new input settings"""
    # Go to the dir and loop through the directories looking for Settings0/settings.xml files
    for r,d,f in os.walk(gridDir):                                  
        page = os.path.split(r)[1]
        for files in f:

            if files.endswith("settings.xml"):
                settingsf = os.path.join(r,files)
                # Now find the input node and overwrite
                parser = etree.XMLParser(strip_cdata=False)
                tree = etree.parse(settingsf, parser)
                ## DO COPY here
                
                # Now write it
                newxml = etree.tostring(tree, pretty_print=True)
                f = open(settingsf, 'w')
                f.write(newxml)
                f.close()

def getUsers(dirs={}):
    """ Look into directorys for any user folders """
    b = dict()
    found = False
    for dir in dirs:
        for r,d,f in os.walk(dir): 
            # is d a potential grid 2 dir?  - look for a settings.xml
            for files in f:
                if files.endswith("settings.xml"):
                    found = True
                    b[r[:-9]] = r.split(os.sep)[-2]

    if found:
        return b 
    else:
        return None
            
if __name__ == '__main__':
    args = docopt(__doc__, version='SetUserInputs vb1')

    inputXML = parseUserInputXML(args['--userdir'])
    # Now find other directories and copy it
    #writeUserInput(inputXML, args['--griddir'],args['--userdir'])
    # This should get all the User dirs in the Grid 2 dir. Provide all possible 
    print getUsers({'/Users/willwade/bin/AAC-Tools/temp/grids/'})