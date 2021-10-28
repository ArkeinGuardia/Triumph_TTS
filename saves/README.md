Saved game as it should be loaded into the Steam Store
======================================================

A saved game should be cleaned by copying it into this 
directory and then executing:

./clean_save

Cleaning will update the LuaScript in the save file
to use the contents of the .ttslua data files.  

Cleaning will remove extra data that should not be part 
of a game that is in the store.

After thae game has been cleaned it should be moved
to Table Top Simulator Saves directory for loading 
for testing.

Windows
=======
cp *.json  My\ Documents/My\ Games/Tabletop\ Simulator/Saves/
cp *.png   My\ Documents/My\ Games/Tabletop\ Simulator/Saves/


