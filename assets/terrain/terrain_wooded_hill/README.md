Wooded Hills
============

Modelling
---------

Hills are kept as non-triangulated Blender models. 

Blender models are to be in metric, we are using the scale of 1 meter in Blender
is 1 inch in Table Top simulator.

Large hills are 1 MU high, 20/25.4 meters in Blender.
Small hills are 1/2 MU high, 20/25.4/2 meters in Blender.
Hills should have a flat peak.

Rule 15, Table 2 governs tarrain size.

-- Ordinary Small, 4--6 x 4--8 x 0.5 MU, 3.14--4.72 x 3.14--6.299 x 0.394 meters
-- Ordinary Large, 6-8 x 6-12 x 1 MU, 4.72--6.299 x 4.72--9.44 x 0.787 meters
-- Edge Small, 2-4 x 6-12 x 0.5 MU, 1.574--3.14 x 4.72--9.448 x 0.394 meters
-- Edge Large, 3-6 x 9-16 x 1 MU, 2.362--4.72 x 7.377--12.598 x 0.787 meters


The models must be:
-- object must be named the same as in TTS, e.g. "terrain Wooded Hill #120"
-- geometrically centered on the world origin.  
-- -- Object Mode
-- -- Select model, 
-- -- Object/Set Origin/Origin to Geometry
-- -- Shift-S, Cursor to Wold Origin
-- -- Shift-S, Selection to cursor.
-- z-axis up.
-- Location is 0,0,0. Select model, Ctrl-A apply Location.
-- Rotation to 0,0,0. Select model, Ctrl-A, apply Rotation. 
-- scale 1,1,1. Select model, Ctrl-A, apply Scale.

Each hill should be in its own directory. The texture for the hill can be a file in the directory called
background.jpg, or in the hills parent directory also called background.png.

The texture in Blender should look good on the hill, check for stretching and incongruities near
seams.  

Start texturing by:
1. Enter shading tab
1.a. Drag background.jpg to workflow and connect color to base color.
1.b. Drag background.jpg to image area
2. Enter UV editing tag.
2.a z-axis top down view.  Edit mode. Faces Select. "A" to select ALL. Right click on object,
UV Unwarap faces, Smart UV Project.
2.b -z axis bottom view.  Select the bottom, in image select all veritices, scale to smallest size, and
move to top-right blue corner.


There should be no other objects, including lights and cameras, in the .blend file.

Export for TTS
--------------

To export the hill for Tabletop Simulator in Blender open the hill's .blend file.
In Layout, select object mode, and select the hill.  Go to Scripting mode, and unlink
any scripts.  Save the .blend file.  Open the script ../../python/blend_to_tts.py and
run it, do NOT save the .blend file the hill has been modified by the scripts.

In the directory that contains the .blend file the following files will be there, with different prefixes:

-- terrain_wooded_hill_110.blend  
   file you saved

-- background.jpg or ../background.jpg
   Input for the generation of terrain_wooded_hill_110.jpg.  Contains the texture of the hill.
   512x512 pixels.  The upper left corner (0,0) should be 16x16
   blue patch to indictate the bottom of the hills.  Think of construction insulating foam.

-- terrain_wooded_hill_110.jpg    
   Texture of the hill to be used in Tabletop Simulator as DiffuseURL.
   Combination of terrain_wooded_hill_110.nt.higlights.png and background.jpg.

-- terrain_wooded_hill_110.obj
   Triangulated version of the hill for use in Tabletop Simmulator as MeshURL and ColliderURL.

-- terrain_wooded_hill_110_points.ttslua
   Data file used in Tabletop Simulator indicting where terrain features such as trees may be
   placed.

-- terrain_wooded_hill_110.blend1 
   backup of the file you created, should not be in git.

-- terrain_wooded_hill_110.nt.higlights.png 
   Input into file that will be used by DiffuseURL. Contains lines that are super imposed on the
   background to show the base and the peak of the hill. Should not be in git.

-- terrain_wooded_hill_110.nt.obj
   Non-triangulated version of the hill.  Used to generate highlights file.  Should not be in git.

-- terrain_wooded_hill_110.nt.mtl   
   Material file for non-triangulated version of the hill.  Should not be in git.

-- terrain_wooded_hill_110.mtl
   Material file for triangulated version of the hill.  Should not be in git.

