SymbolDB
========

**Aim**

- To collect the file paths and details of Symbol Systems used in vocab packages
- Originally designed to programmatically change a vocab package from one symbol system to another

**Usage:**

        SymbolCollector.py --imagedir="Path\To\Your\Image\Folder"  --symbolset=NameOfSymbolSet -database="SymbolCollector.db

or 

        SymbolCollector.py --pixfile="Path\To\Your\Pixfile.pix"  --symbolset=NameOfSymbolSet -database="SymbolCollector.db

- the DB is a sqllite database
- the pixfile is a file format used by the Grid 2 software. Its a file with each line being a lookup table. e.g.:

    a\somefile.wmf=[string]String|Int.wmf
    

Once the database is populated with some images then we need to do some symbol matching. Right now this is a bit of a work-in progress. It should really write to ssMatch which is designed as a linking table but its currently fixed to work with ssWLSColour and ssMJPCS updating a column in ssWLSColour.

so anyway.. it works like this:

    SymbolMatcher.py --symbolsfrom ssWLSColour --symbolsto ssMJCS 
    
It then looks through symbolsfrom table and does three things
* Finds direct matches
* Finds matches with the word in the sentence (lower ranked)
* Finds synonyms of words with the word then searches the symbolsto database for any symbols that match

Its not complete as of yet. Some asides:

* Wordnet seems to neatly find synonyms English=American English 
* This isn't yet using any of the word categorisation that could be available to the parser

 **NB:**

- symbolset should be one word
- Browse the SymbolCollector.db to see what has already been done
- The actual Grid/Pageset converter is yet at a stage of publishing. It will break your machine and possibly your life
