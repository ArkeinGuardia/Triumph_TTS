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
  Can have a suffix added to indicate a general "_Gen".
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


