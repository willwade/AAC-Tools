import sys, argparse, sqlite3
import nltk    
from nltk.corpus import wordnet

def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

# Not in use just yet
def setup_db(sqlitefile, symbolset):
    try:
        connection = sqlite3.connect(sqlitefile)
        cur = connection.cursor()  
        cur.executescript('DROP TABLE IF EXISTS ssMatch;' +
            'CREATE TABLE ssMatch (Id INTEGER PRIMARY KEY, '+symbolsfrom+' INTEGER, '+symbolsto+' INTEGER);')
        connection.commit()
        
    except sqlite3.Error, e:
        print "Error %s:" % e.args[0]
        sys.exit(1)

# used for the names in synonyms. 
# NB: note that they are dups because usually you would want info on the diff types of words..
# From: http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
def match_symbols(sqlitefile, symbolsetfrom, symbolsetto):
    connection = sqlite3.connect(sqlitefile)
    c = connection.cursor()
    # Get all the rows in the symbolset from..
    c.execute('SELECT Id, SymbolName FROM %s' % symbolsetfrom)
    rows=c.fetchall()
    for row in rows:
        # See if there is a direct translation
        c.execute('SELECT Id, SymbolName FROM %s WHERE SymbolName = "%s" COLLATE NOCASE' % (symbolsetto, row[1]))
        foundrow=c.fetchone()
        if foundrow is not None:
            #print 'Woot! Found direct replacement:'+row[1]+' can be found in PCS id:'+str(foundrow[0])
            try:
                c.execute('UPDATE %s SET PCSSyn=%s WHERE Id=%s' % (symbolsetfrom, str(foundrow[0]), str(row[0])))
                connection.commit()
            except:
                print 'Error updating db at 1'
        else:
            c.execute('SELECT Id, SymbolName FROM '+symbolsetto+' WHERE (" " || SymbolName || " ") LIKE "% '+row[1]+' %" COLLATE NOCASE')
            foundrows=c.fetchall()
            if (len(foundrows)==1):
                # we will have this
                try:
                    c.execute('UPDATE %s SET PCSSyn=%s WHERE Id=%s' % (symbolsetfrom, str(foundrows[0][0]), str(row[0])))
                    connection.commit()
                except:
                    print 'Error updating db at 2'
            elif (len(foundrows)>0):
                print 'Hmm. Which one...'
                for foundrow in foundrows: 
                    print 'looking for:%s found: %s' % (row[1], foundrow[1])
            else:
            # ok lets do this the hard way! lets get the synonym of the word/phrase
                syns = wordnet.synsets(row[1].replace('_',' '))
                if syns:
                    #print syns
                    names = [s.lemmas[0].name for s in syns]
                    #is the synonm available?? 
                    print row[1]+':..Lets get some syns:'
                    for name in f7(names):
                        print '  '+ name
                        # lets now see if this name is in the db
                        c.execute('SELECT Id, SymbolName FROM %s WHERE SymbolName = "%s" COLLATE NOCASE' % (symbolsetto, name.replace('_',' ')))
                        foundrow=c.fetchone()
                        if foundrow is not None:
                            print 'Woot! Found direct replacement for:%s (using: %s) can be found in PCS id:%s' % (row[1], name, str(foundrow[0]))
                            try:
                                c.execute('UPDATE %s SET PCSSyn=%i WHERE Id=%i' % (symbolsetfrom, int(foundrow[0]), int(row[0])))
                                connection.commit()
                            except:
                                print 'Error updating db at 3'
                                print 'UPDATE %s SET PCSSyn=%i WHERE Id=%i' % (symbolsetfrom, int(foundrow[0]), int(row[0]))



parser = argparse.ArgumentParser(prog='SymbolMatcher',description='Tries desperatley hard to match symbols in one database to another. Uses all sorts of magic. Mileage may vary')
# Basics
parser.add_argument('--verbose','-v', type=bool, default=True, help='Verbose output True/False. Default: True')
parser.add_argument('--database','-d', type=str, default='SymbolCollector.db', help='Location of the SQLLite database file. Default: .SymbolCollector.db')
parser.add_argument('--symbolsfrom','-f', type=str, default='ssWLSColour', help='Name of the symbolset to find symbols in')
parser.add_argument('--symbolsto','-t', type=str, default='ssMJPCS', help='Name of the symbolset (Table) to convert to')
args = parser.parse_args() 

#setup_db(sqlitefile, args.symbolsfrom, args.symbolsto)
match_symbols(args.database, args.symbolsfrom, args.symbolsto)
