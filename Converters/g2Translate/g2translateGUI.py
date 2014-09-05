#!/usr/bin/env python
# Contact: Will Wade <will@e-wade.net>
# Date: July 2014
# Binary: pyinstaller.py --icon=g2Translate/icon.ico --onefile --nowindow --noconsole g2translateGUI.py
# -*- coding: utf-8 -*-
"""
G2LangConverter. Convert from one language to another for Grid 2 User dir.  
"""
from easygui import *
import sys
from lxml import etree
# Main G2 code here
import urllib2
import os.path, csv, codecs
from lxml import etree
from unicodecsv import UnicodeWriter, UnicodeReader 

def translate(to_translate, to_langage="auto", langage="auto"):
	'''Return the translation using google translate
	you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
	if you don't define anything it will detect it or use english by default
	Example:
	print(translate("salut tu vas bien?", "en"))
	hello you alright?'''
	agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
	before_trans = 'class="t0">'
	link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s" % (to_langage, langage, to_translate.replace(" ", "+"))
	request = urllib2.Request(link, headers=agents)
	page = urllib2.urlopen(request).read()
	result = page[page.find(before_trans)+len(before_trans):]
	result = result.split("<")[0]
	return result


def _add_to_list(finalList, addList):
    for word in addList:
        # Some dodgy characters getting in from somewhere.. 
        uniword = word.replace(u"\u00A0", " ")
        if uniword not in finalList:
            finalList.append(uniword)
    return finalList          

def get_LangADict(userdir='',output_file='Lang.csv',auto_translate=False,lang_code='es'):
    '''
    Look for wordlist.xml files and grid.xml files
    extract any cdata plonking into a translate file for now.. 
    '''
    
    userdir = os.path.normpath(userdir+'/Grids/')
    wordlist = list()
    # Get gridsetname
    for r,d,f in os.walk(userdir):   # Parse  directories to find Grids directory
        for files in f:
            if 'xml' in files:
                pth = r+'/'+files
                parser = etree.XMLParser(strip_cdata=False)
                tree = etree.parse(pth, parser) # Parse the file
                wordlist = _add_to_list(wordlist, tree.xpath('//commands/command[id = "type"]/parameter[@index = "1"]/text()'))
                wordlist = _add_to_list(wordlist, tree.xpath('//wordtext/text()'))
                wordlist = _add_to_list(wordlist, tree.xpath('//tooltip/text()'))
                wordlist = _add_to_list(wordlist, tree.xpath('//caption/text()'))
                # now dump all words to a big file.. 
                # wordtext, tooltip, caption 
    
    #wordFile = UnicodeWriter(open('Language.csv', 'wb'), delimiter=',', quotechar='"')
    
    ff = open(output_file, 'wb')
    #ff.write(codecs.BOM_UTF8)
    wordFile = UnicodeWriter(ff)
    
    for word in wordlist:
        if auto_translate:
            wordFile.writerow([word,translate(word, lang_code)])
        else:
             wordFile.writerow([word,'tbc'])
    return True

    # ok lets do it...

def _get_lang_file(LangFile):
    ff = open(LangFile, 'rb')
    wordFile = UnicodeReader(ff)
    return list(wordFile)

def _get_word_in_csv(langlist,word):
    for row in langlist:
        if unicode(word) == unicode(row[0]):
            return unicode(row[1])
        
          
def convertAtoB(userdir='',LangFile='Lang.csv'):
    userdir = os.path.normpath(userdir+'/Grids/')
    wordlist = list()
    langlist = _get_lang_file(LangFile)
    
    # Get gridsetname
    for r,d,f in os.walk(userdir):   # Parse  directories to find Grids directory
        for files in f:
            if 'xml' in files:
                pth = r+'/'+files
                parser = etree.XMLParser(strip_cdata=False)
                tree = etree.parse(pth, parser) # Parse the file
                words = tree.xpath('//wordtext')
                for word in words:
                    translation = _get_word_in_csv(langlist, unicode(word.text))
                    if translation == None:
                        translation = unicode(word.text)
                    word.text = etree.CDATA(translation)
                
                words = tree.xpath('//tooltip')
                for word in words:
                    translation = _get_word_in_csv(langlist, unicode(word.text))
                    if translation == None:
                        translation = unicode(word.text)
                    word.text = etree.CDATA(translation)
                
                words = tree.xpath('//caption')
                for word in words:
                    translation = _get_word_in_csv(langlist, unicode(word.text))
                    if translation == None:
                        translation = unicode(word.text)
                    word.text = etree.CDATA(translation)
                
                words = tree.xpath('//commands/command[id = "type"]/parameter[@index = "1"]')
                for word in words:
                    translation = _get_word_in_csv(langlist, unicode(word.text))
                    if translation == None:
                        translation = unicode(word.text)
                    word.text = etree.CDATA(translation)
                                    
                file_out = open(pth, 'wb')
                file_out.write('<?xml version="1.0" encoding="utf-8" ?>' + etree.tostring(tree, pretty_print=True, encoding="UTF-8"))
                

def walklevel(some_dir, level=1):
    some_dir = some_dir.rstrip(os.path.sep)
    if os.path.isdir(some_dir):
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


readme = """
This application does the heavy lifting for converting A Grid 2 User from one language to another.  This is done in two steps:
1. Create a language file for your User. This is simply a csv file (i.e. it can be read in Excel) with column one being a list of the words or phrases found in the user. Once this is created you then either manually translate each cell in column 1 putting your translation into column 2, or copying and pasting the entire column into google translate. The translated text can then be copied back into the spreadsheet into column 2. 
2. Once you have a complete Language file (NB: This MUST be a csv - don't try and expect it to read a xls file!) run the 'Convert' part of the conversion tool and it will then map anything in column 1 to column 2. 

Some things to look out for:
- CREATE A BACKUP OF YOUR VOCAB USER FILE! I can't warn you enough of this. It WILL Overwrite your entire vocabulary for ONE user - back that user up.. If you ever want to re-run this tool you need to do it on the original language version
- Don't try and be clever and remove any spaces from column 1 text. Those spaces are generally important for the Grid 2 when text goes to the message bar 
- As I say above - don't go converting that CSV file to something else. Excel will try and warn you and get you to save it as excel spreadsheet. By all means create a backup - but don't expect this tool to read it. (Also note: If you are entering funny characters and its not saving it make sure it is being opened with the encoding 'UTF-8') 
"""


textbox('',"Grid 2 User Language Converter",readme)
title = "Grid2 User Language Converter"


msg = "Do you want to create a language file or convert a Grid 2 User directory with a already created language file?"
choices = ["Create","Convert","Cancel"]
reply   = buttonbox(msg,choices=choices)
if reply is 'Cancel':
    sys.exit(0)           # user chose Cancel


found, userdirs = findPotentialDirs({os.path.normpath("C:\Users\Public\Documents\Sensory Software\The Grid 2\Users"), os.path.normpath(os.path.expanduser('~')+'\My Documents\Sensory Software\The Grid 2\Users')})
if found:
    if len(userdirs) > 1:
        #Ask which dir to choose
        msg ="Which is the user directory you wish to use?"
        userdirs = choicebox(msg, title + " - Select User directory", userdirs)
        print userdirs
else:
    #
    msg = "No usual directories were found for the Grid 2 User settings. Can you locate the Users Directory you wish to use? (See the 'Grid 2 - Preferences - File Locations - User Files')" 
    msgbox(msg, title + "Please provide a directory")
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
msg ="Choose a User to convert into another language"
userDir = choicebox(msg, title, choices)
userDirPath = userdirs[0]+os.sep+userDir
if userDir == None:
        sys.exit(0)           # user chose Cancel
# Now use choice as the one to use 
# Lets double check
if reply is 'Create':
    # We have the user directory.. Lets ask them where they want to save the Lang file.. 
    msgbox('Please choose where and what the language file will be called. It should end with a .csv extension. Please remember where you are saving this!!!')
    langfile = filesavebox(msg, title, default='LangFile.csv')
    # NB: see if windows keeps the ending.. 
    # RUN create
    get_LangADict(userDirPath, langfile, False, 'es')
    msgbox('Yay! Its created the Language file. You can find it at '+langfile+' . Now please translate each line of the file putting your translation into column 2 (overwriting tbc in each cell). You can use Google translate if you want to cheat..')
    sys.exit(0)
elif reply is 'Convert':
    # We have the user directory.. We just need their language file.. 
    msgbox('Please choose your language file - with the translations in the second column!!')
    langfile = fileopenbox(msg, title, default='LangFile.csv')
    msg = "Warning: The next step will overwrite ALL of the language data in'"+userDir+"'. Want to continue? Note: It does take a little while to run..."
    title = "Please Confirm"
    if ccbox(msg, title):     # show a Continue/Cancel dialog
        pass  # user chose Continue
        convertAtoB(userDirPath, langfile)
        msg = "Great. You have just converted your Grid 2 user"+userDir
        msgbox(msg)
    else:
        sys.exit(0)           # user chose Cancel
else:
        sys.exit(0) # Lets continue
