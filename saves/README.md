
Copying Saved Game
==================

To get a saved game from TTS into the correct directory for working on it:

./from_tts
or
cp ~/My\ Documents/My\ Games/Tabletop\ Simulator/Saves/TS_Save_1.* .

To put the game into TTS so you can run it

./to_tts 
or
cp *.json  *.png ~/My\ Documents/My\ Games/Tabletop\ Simulator/Saves/

You may have to create a symbolic link for "My Documents" in  your
home directory.

from_tts uses TS_Save_1.* as the file to copy into the current directory.

Split Save
==========

Takes the saved game and extracts the objects so you can work on them.
Also makes it easier to see what TTS changed if you create a new save
file in TTS.

./split_save

Clean Save
==========

Updates the save file to contain the latest source.

.ttslu files, main.xml are copied into the save file.
The objects that have been extracted from split_save are used as the source for updating.

The Lua script is modified with the current date unless the --no-date option is used.

Cleaning will remove extra data that should not be part 
of a game that is in the store.

Examples:
  ./clean_save --no-date

If there are any modifications on the file system that have not pushed to Github then
assets are referenced by a URL to the file system.  Otherwise assets are referenced
with URL on Github.

The version of TS_Save_1.json that has no assets referencing the file system may be 
uploaded to Steam.




