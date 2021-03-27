Triumph! for Tabletop Simulator
===============================

Features: Setup
---------------

- Create tables with different environments, like grass fields, steppe or deserts.
- Automatically fix terrain to the table so it doesn't move.
- Automatic army creation based on the Triumph! lists. The models have been adapted and lists are easy to create using a scripting system.
- Spawned bases have a base ground theme depending on the table created. Furtheremore, lighter troops spawn in a loose formation, and there are variations between models and textures.
- The game will tell the options of the army so you don't have to doublecheck everything.
- There's a checkbox to enable deployment rulers which significantly help with the deployment.
- The armies, including bases, are color coded, to avoid confusions.
- The models have a specific minimal collider to avoid problem with pikes, calvary, etc.

Features: Gameplay (pending)
----------------------------

- Snapping system: When you drop a base close to another, they will snap, as long as they are close enough and the angle is correct. Snapping includes charging and even "close the door" manouver. It can be turned off for particular manouvers.
- Single movement: If you pick a base and move it, a small text will appear in the screen telling exactly in realtime how many BWs you are moving. This includes all corners, so it's useful for rotations etc. Once dropped, the total will be shown in the log.
- Reset movement: When moving a single base, if snapping is active, and you move less than 0.2 MUs, resets the abse to its original position, which can be useful to evaluate future movements.
- Group movement: Select multiple bases and with one click move all as a group forward! You can select how much to move with a slider.
- Preview movement: Using the slider, you also have a small gizmo in front of the troops that shows where the base will end after pressing move.
- Preview Bow/Artillery range: Like the movement, the range is also projected from the future movement position (which you can set position to check the current range).
- Show ZOC: Like the arty range, this is an option that can be toggled that shows how far the ZOC extends.
- Push back Column: Moves a column back, by the depth of the front element (if the element has more depth than width, only pushes back by its width).

License
-------

See the LICENSE.md at the top directory.

Unit Testing
------------

Unit tests are in unit tests and require a "Unix" like environment.  

Windows users can use WSL2 (or WSL) https://docs.microsoft.com/en-us/windows/wsl/install-win10, and install
Ubuntu.  In Ubuntu install make and lua with:
sudo apt-get install make
sudo apt-get install lua
Note: your home directory is under /mnt/c/Users

Mac users can use brew to install make and lua.

Execution of the unit tests is done by:
cd unittests
make

Adding an army
--------------

A base in army is defined as a table.  We call this table the "base definition".

Base definition fields are:
* name Augmented type of the base. Starts with the type, e.g. "Knights".  
  Can have a suffix added to indicate a general "  General".
  Can have a suffix added to indicate mounted infantry "_Mounted".
* base Tile tht the figures are to be placed on when rendering.
* n_modelsa Number of models to place on the base
* fixed_models Figures to add to the base when rendering.
* loose = true (optional) Indictes that the models should be placed in a
    non-grid formation.  Used to indicate open order troops.
* points (optional) Number of points the base is worth. Default is the points
  for the type.
* battle_card (optional) Battle card that modifies the standard behviour of
  the type
* dismount_as (optional) String containing the name of the variable for
  the base defintion of that will replace this base if the unit
  is dismounted.  i.e. The base is mobile infantry.

A base definition that has points, battle_card, or dismount_as set must be an external
base definition, otherwise it may be external or internal.

An external base definition is one in which a variable is declared for the definition.
See burgundian_ordannances_1471_to_1477_ad_knights_gen for an example.

An army is declared with data for the army, and its bases.  For an external
base definition the definition is a string of the variable name.  Example:
base1 = "burgundian_ordannances_1471_to_1477_ad_knights_gen",

An internal base defintion is just the table itself.  Internal definitions will take
a tiny amount of less memory.

How to add a building to terrain
--------------------------------

Buildings are placed in Villages.  In DBA, villages are called
Built Up Areas (BUA), so BUA is used in the code.w

When the terrain is locked, the buildings are added to make the table look
pretty.  The have no effect in the game, as the area of the village
is what is used.

Create a building that has its floor centered at 0,0,0, and have the
.obj and .jpeg files on the local file system.

Test the files by starting DBA3 in TTS.  Select
Objects/Components/Custom/Model.The cursor will change to a chess pawn.
Click on the table, which should leave a white dot.  Then click on the
select menu item.  You should get a dialog for Custom Model. Under Model
select your .obj and .jpeg file for Model/Mesh and Defuse/Image,
choose local file.  Under Material select Carboard.

Ensure that the model looks good.

Now we need to scale the model.  We first create a sample lot to place the
building on.  Objects/Blocks/Red Square, to create a 1x1x1 box.

Click Gizmo/Scale and click on the box.  In the transform dialog change
the position of the box to 0,1.16,0 and the scale to
3,0.25,2.25, and close the dialog.  The building will have to fit
on this box, with a bit of space for the front yard and back yard.

Click Gizmo/Scale and click on the building.  Change the position
to 0,1,0; the building should move on top of the box.  Without
exiting the dialog adjust the scale values to the same value (e.g. 0.3),
so that the building fits comfortably on the box.

You may now add a BUA area, and lock the table. Spawn an army
with models.  Compare your new building to the existing buildings.
Adjust the scaling as desired. Write down the final scale.

Spawn a new model like before but this this time select to have the files
on the cloud. Write down the URLs on the steam server.

In a text editor open data_terrain.ttsla.  Copy the entry for
terrain_building_desert_shack, and change the contents to
the values for your building.

Find the entry for "bua = { object = {" for the terrain where your
building fits, and add the variable name as a string.

Test by commenting out the other buildings and have a game with all BUA
areas on the table, with the BUAs rotated in different directions,
ond lock the table.  Your building should be enclosed in the BUAs, and
should not overlap other buildings.
Uncomment the other builds, and run the test again.
