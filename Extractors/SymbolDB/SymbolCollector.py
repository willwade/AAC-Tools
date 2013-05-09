#!/usr/bin/env python
# -*- coding: cp1252 -*-
# Contact: Will Wade <will@e-wade.net>
# Date: Jan 2012

# Convert folder of images to a sqllite database so can use it for symbol lookups

import os.path, sys, sqlite3
import argparse

def parse_images(imagedir, sqlitefile, symbolset):
    SQLInsert = ''
    a = 1;
    for r,d,f in os.walk(imagedir):     
        for n in f:
            # SymmbolName: strip .emf, .wmf, .png .jpg .jpeg, from file
            #   replace _ - with SPACE             
            SymbolName = os.path.splitext(n)[0]
            # keywords = file path words (minus numbers and any 7-7 pattern) plus SymbolBane             
            parts = r[len(imagedir):].split('/')
            partsTxt = ','.join(parts)
            SQLInsert = SQLInsert + 'INSERT INTO ss' + symbolset +' VALUES ('+str(a)+',"'+SymbolName+'","'+r+'/'+n+'","'+ partsTxt +'"); '
            a=a+1
    try:
        connection = sqlite3.connect(sqlitefile)
        cur = connection.cursor()  
        cur.executescript(SQLInsert)
        connection.commit()
        print str(a)+" images inserted into ss"+symbolset+" of "+sqlitefile
    
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

def parse_pixfile(pixfile, sqlitefile, symbolset):
    # a pix file looks like lines of :
    # b\bookmark.wmf=[MJPCS#]6523.wmf
    # simply split at =                
    lines = pixfile.readlines()
    SQLInsert = ''
    a = 1;
    for line in lines:
        bits = line.strip().split('=')
        print 'name:'+bits[0]
        #keywords
        try:
            parts = bits[0].split('\\')
            partsTxt = parts[0]
            name = parts[1][:-4]
            location = bits[1]
            print "name: %s, locn: %s, parts: %s" % (name, location, partsTxt)        
            SQLInsert = SQLInsert + 'INSERT INTO ss' + symbolset +' VALUES ('+str(a)+',"'+name+'","'+location+'","'+ partsTxt +'"); '
            a=a+1        
        except:
            print 'failure'

    try:
        connection = sqlite3.connect(sqlitefile)
        cur = connection.cursor()  
        cur.executescript(SQLInsert)
        connection.commit()
        print str(a)+" images inserted into ss"+symbolset+" of "+sqlitefile
    
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)
    
def setup_db(sqlitefile, symbolset):
    try:
        connection = sqlite3.connect(sqlitefile)
        cur = connection.cursor()  
        cur.executescript('DROP TABLE IF EXISTS ss' + symbolset +';' +
            'CREATE TABLE ss' + symbolset +'(Id INTEGER PRIMARY KEY, SymbolName TEXT, Path TEXT, Keywords TEXT);')
        connection.commit()
        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)


def readable_dir(prospective_dir):
  if not os.path.isdir(prospective_dir):
    raise Exception("readable_dir:{0} is not a valid path".format(prospective_dir))
  if os.access(prospective_dir, os.R_OK):
    return prospective_dir
  else:
    raise Exception("readable_dir:{0} is not a readable dir".format(prospective_dir))


def main():
    imagedir='.'
    sqlitefile ='SymbolCollector.db'
    symbolset='Widgit'

parser = argparse.ArgumentParser(prog='SymbolCollector',description='Collects information regarding a directory of symbols or a pix file to a database')
# Basics
parser.add_argument('--verbose','-v', type=bool, default=True, help='Verbose output True/False. Default: True')
parser.add_argument('--database','-d', type=str, default='SymbolCollector.db', help='Location of the SQLLite database file. Default: .SymbolCollector.db')
parser.add_argument('--symbolset','-s', type=str, default='', help='Whats the name of the symbol set? NB: This creates a table with this name')
parser.add_argument('--imagedir','-i', type=readable_dir, help='Locate the directory with the images to pass. NB: If pix file given this is ignored.')      
parser.add_argument('--pixfile', type=argparse.FileType('r'), help='Read data from a file')
args = parser.parse_args() 

verbose = args.verbose
symbolset = args.symbolset        
sqlitefile = args.database

setup_db(sqlitefile, symbolset)

pixfile = args.pixfile
if pixfile:
    parse_pixfile(pixfile, sqlitefile, symbolset)
else:
    imagedir = args.imagedir
    if imagedir:
        parse_images(imagedir, sqlitefile, symbolset)
    
if __name__ == "__main__":
    main()
