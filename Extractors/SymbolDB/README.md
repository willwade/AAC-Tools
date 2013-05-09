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
    

**NB:**

- symbolset should be one word
- Browse the SymbolCollector.db to see what has already been done

