import sys, sqlite3
import nltk    
from nltk.corpus import wordnet

# used for the names in synonyms. 
# NB: note that they are dups because usually you would want info on the diff types of words..
# From: http://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-in-python-whilst-preserving-order
def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]

connection = sqlite3.connect('SymbolCollector.db')
c = connection.cursor()
c.execute('SELECT Id, SymbolName FROM ssWLSColour')
rows=c.fetchall()
for row in rows:
    # See if there is a direct translation
    c.execute('SELECT Id, SymbolName FROM ssPCSColCatUK WHERE SymbolName = "'+row[1]+'" COLLATE NOCASE')
    foundrow=c.fetchone()
    if foundrow is not None:
        #print 'Woot! Found direct replacement:'+row[1]+' can be found in PCS id:'+str(foundrow[0])
        try:
            c.execute('UPDATE ssWLSColour SET PCSSyn='+str(foundrow[0])+' WHERE Id='+str(row[0]))
            connection.commit()
        except:
            print 'Error updating db'
    else:
        c.execute('SELECT Id, SymbolName FROM ssPCSColCatUK WHERE (" " || SymbolName || " ") LIKE "% '+ row[1] +' %" COLLATE NOCASE')
        foundrows=c.fetchall()
        if (len(foundrows)==1):
            # we will have this
            try:
                c.execute('UPDATE ssWLSColour SET PCSSyn='+str(foundrows[0][0])+' WHERE Id='+str(row[0]))
                connection.commit()
            except:
                print 'Error updating db'
        elif (len(foundrows)>0):
            print 'Hmm. Which one...'
            for foundrow in foundrows: 
                print 'looking for:'+row[1]+'  found:'+ foundrow[1]
        else:
        # ok lets do this the hard way! lets get the synonym of the word/phrase
            syns = wordnet.synsets(row[1])
            if syns:
                #print syns
                names = [s.lemmas[0].name for s in syns]
                #is the synonm available?? 
                print row[1]+':..Lets get some syns:'
                for name in f7(names):
                    print '  '+ name
                    # lets now see if this name is in the db
                    c.execute('SELECT Id, SymbolName FROM ssPCSColCatUK WHERE SymbolName = "'+name.replace('_',' ')+'" COLLATE NOCASE')
                    foundrow=c.fetchone()
                    if foundrow is not None:
                        print 'Woot! Found direct replacement for:'+row[1]+' (using: '+name+') can be found in PCS id:'+str(foundrow[0])
                        try:
                            c.execute('UPDATE ssWLSColour SET PCSSyn='+str(foundrow[0])+' WHERE Id='+str(row[0]))
                            connection.commit()
                        except:
                            print 'Error updating db'

c.execute('select COUNT(id) from ssWLSColour where PCSSyn NOTNULL')
converted=c.fetchone()[0]                    
print 'Converted '+str(converted)+ ' symbols'
