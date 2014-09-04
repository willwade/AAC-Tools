#Set User Inputs#

[Download it here](http://script-exes.s3.amazonaws.com/SetUserInputsGUI.exe)


##The problem##

You use [The Grid 2 software](http://sensorysoftware.com/grid-software-for-aac/grid2_aac_software/) and you want to use a number of different users. The problem is that your access method is the same for each user and you have to remember to set the same user settings for each new user. This can be a little time consuming.. and when you have lots of users a pain.

##What does this little application do?##
It looks for your Grid 2 User directory, asks you to choose a user whose Access (Input method) settings you want to copy. It then copies the selected User settings to all the rest. 

##Cautions and notes##

- After running restart the Grid
- It can take a little while. I'll try and speed this up.. In the meantime if nothing happens in between steps don't fret - something is happening..
- Please please backup your users directory if you have any concerns
-  If it can't find your users directory it will ask you to locate it. To find it go to the Grid 2. Go to File menu, then Preferences and look at the "File Locations". You want the field that says 'Location for user files:' (NB: I need to add to the list of standard settings locations to make this less of a problem..)
- If it says it has made the changes and you don't see any difference then its likely due to the fact you have a Users folder somewhere on your machine that is no longer being used. If so just rename the following directories: 
        
        C:\Users\Public\Documents\Sensory Software\The Grid 2\Users
        C:\\My Documents\Sensory Software\The Grid 2\Users

Any issues feel free to send them to Will @ ACE and I will try and fix (but if your Grid stops working I can't take responsibility!)


