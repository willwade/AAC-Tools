#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Grid 2 Language Converter.

To use this tool first run the script with a 'create' command. This creates a csv (speadsheet) of all the words in the Grid user supplied.
Then go through each line of this document and in column 2 add the translation. You can make your life easier by copying the entire column and pasting it into google.translate.com. Paste the returned text into column two. 
Lastly map these changes to the Grid user by doing a 'convert' command - supplying the language csv file you have just created.
NB: There is a way of getting this script to do the google lookup automatically - however I don't recommend it. It's slow and likely to ban you from googles translate server.. 

Usage:
  g2translate.py create <lang_file> <Raw_G2_User_Directory> [-g | --google <lang_code>]   
  g2translate.py convert <lang_file> <Raw_G2_User_Directory>
  g2translate.py (-h | --help)
  g2translate.py --version

Options: 
  <lang_file>               The lang file. File out will be a csv. Please provide the updated one with your language in second column for a convert [default: Lang.csv]
  <Raw_G2_User_Directory>   The User directory. This is not a grid bundle. This is not the Top Users directory - This is ONE user directory. 
  -g --google               Try and Use Google for language conversion. Warning: Slow and possibly deadly [default: False]
  <lang_code>               If you use the Google tool please provide a language code [default: es]
  -h --help                 Show this screen.
  --version                 Show version.
"""
try:
    from docopt import docopt
except ImportError:
    exit('This script requires that `docopt` library'
         ' is installed: \n    pip install docopt\n'
         'https://github.com/docopt/docopt')

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
        if word not in finalList:
            finalList.append(word)
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
    
    ff = open(output_file, 'w')
    ff.write(codecs.BOM_UTF8)
    wordFile = UnicodeWriter(ff)
    
    for word in wordlist:
        if auto_translate:
            wordFile.writerow([word,translate(word, lang_code)])
        else:
             wordFile.writerow([word,'tbc'])
    return True

    # ok lets do it...

def _get_word_in_csv(LangFile,word):
    ff = open(LangFile, 'r')
    wordFile = UnicodeReader(ff)
    
    for row in list(wordFile):
        if unicode(word) == unicode(row[0]):
            return unicode(row[1])
        
          
def convertAtoB(userdir='',LangFile='Lang.csv'):
    userdir = os.path.normpath(userdir+'/Grids/')
    wordlist = list()
    
    # Get gridsetname
    for r,d,f in os.walk(userdir):   # Parse  directories to find Grids directory
        for files in f:
            if 'xml' in files:
                pth = r+'/'+files
                parser = etree.XMLParser(strip_cdata=False)
                tree = etree.parse(pth, parser) # Parse the file
                words = tree.xpath('//wordtext')
                for word in words:
                    translation = _get_word_in_csv(LangFile, unicode(word.text))
                    if translation == None:
                        translation = unicode(word.text)
                    word.text = etree.CDATA(translation)
                
                words = tree.xpath('//tooltip')
                for word in words:
                    translation = _get_word_in_csv(LangFile, unicode(word.text))
                    if translation == None:
                        translation = unicode(word.text)
                    word.text = etree.CDATA(translation)
                
                words = tree.xpath('//caption')
                for word in words:
                    translation = _get_word_in_csv(LangFile, unicode(word.text))
                    if translation == None:
                        translation = unicode(word.text)
                    word.text = etree.CDATA(translation)
                
                words = tree.xpath('//commands/command[id = "type"]/parameter[@index = "1"]')
                for word in words:
                    translation = _get_word_in_csv(LangFile, unicode(word.text))
                    if translation == None:
                        translation = unicode(word.text)
                    word.text = etree.CDATA(translation)
                                    
                file_out = open(pth, 'wb')
                file_out.write('<?xml version="1.0" encoding="utf-8" ?>' + etree.tostring(tree, pretty_print=True, encoding="UTF-8"))
                

if __name__ == '__main__':
    args = docopt(__doc__, version='Grid 2 Language Converter 1.0 ')
    if args['create']:
        lang = 'es' if (args['<lang_code>'] == None) else args['<lang_code>']
        get_LangADict(args['<Raw_G2_User_Directory>'], args['<lang_file>'], args['--google'], lang)
        print 'Your dictionary file has now been created. Please copy the entire column 1 of the spreadsheet and paste into google translate. Paste the results into column 2 and save'
    elif args['convert']:
	    convertAtoB(args['<Raw_G2_User_Directory>'], args['<lang_file>'])
	    
        
	

