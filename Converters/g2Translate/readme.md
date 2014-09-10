#Grid 2 - User Language Converter#

[Download it here](http://script-exes.s3.amazonaws.com/g2translateGUI.exe)


##What this does

It will convert a Grid 2 User (not bundle - it works on the raw user data) from one language to another - using a supplied Language dictionary file

##To use this
1. Create. You need to extract all the language from a user. Use the create tool to do this. 
2. Open your created language file and add the translations in to column 2. (It should open in Excel). Save the document as a CSV file format. Don't edit the words in column 1. 
3. Convert. Pass the tool the Language file and it will then look for any words in column 1 and replace them with the words in column 2. 

Once converted you may have some problems seeing your converted language - particularly languages with non-english characters. To fix this:

1. You need to install the correct language version of the Grid. 
2. Change the language of the user (User settings - About Me - Change Language..") to the correct language (I should do this in my tool to be honest)
3. Change the locale of windows for non-unicode programs: http://windows.microsoft.com/en-us/windows/change-system-locale#1TC=windows-7 to the same language (The grid it appears is a bit rough around the edges on Unicode..)


##Warnings:

- Create a backup (do a "Save as Grid Bundle") of your user before running this.
- If you want to rerun it you will need to run on the original user. i.e. Once you have converted it there is NO UNDO!
- There are some bugs with the file reading of the csv file. Until I get a chance to rewrite this code make sure its a standard CSV (with UTF-8 encoding if your editor gives you that option)


## The command line tool


    Usage:
      g2translate.py create <lang_file> <Raw_G2_User_Directory> [-g | --google <lang_code>]   
      g2translate.py convert <lang_file> <Raw_G2_User_Directory>
      g2translate.py (-h | --help)
      g2translate.py --version

Note: this does contain a way of automatically getting the language from google. However it takes quite a while.. and you may get banned from Google translate for running it.. 