#!/usr/bin/python3

# Takes the selected object and duplicates it.
# On the duplicate:
# 1. Calculates the location where terrain features, e.g. trees, may be placed.
# 2. Generates texture map with extra highlights for the peak
# 2.a Export to OBJ fo data retrieval
# 3. Export to OBJ version for TTS
# 3.a Triangulates it.
# 3.b Exports it to .obj file with same base name and location as the .blend file.
# 3.c Deletes the duplicate.


import bpy
import glob
import math
import mathutils
import os
import sys
from math import pi, acos

# Setup path for terrain manipulation scripts
libdir = os.path.abspath(os.path.join(
                  os.path.dirname(bpy.context.blend_data.filepath),
                            "..",
                            "..",
                            "python"))
assert(os.path.isdir(libdir))
sys.path.append(libdir)
import hilltexture


def change_to_object_mode() :
    
    res1=bpy.ops.object.mode_set.poll()
    print("res1: ", res1)
    res2=bpy.ops.object.mode_set()
    print("res2: ", res2)
    if bpy.context.active_object is not None:
        if bpy.context.active_object.mode is not None:
            if bpy.context.active_object.mode == "OBJECT" :
                return
    res3=bpy.ops.object.mode_set(mode='OBJECT')
    print("res3: ", res3)


def duplicate(obj_object) :
    change_to_object_mode()
    before = bpy.data.objects[:]
    dup_result = bpy.ops.object.duplicate_move(
      OBJECT_OT_duplicate={ "linked":False, "mode":'TRANSLATION'}, 
      TRANSFORM_OT_translate={
        "value":(0, 0, 0), 
        "orient_type":'GLOBAL', 
        "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
        "orient_matrix_type":'GLOBAL', 
        "constraint_axis":(False, False, False), 
        "mirror":True, 
        "use_proportional_edit":False, 
        "proportional_edit_falloff":'SMOOTH', 
        "proportional_size":1, 
        "use_proportional_connected":False, 
        "use_proportional_projected":False, 
        "snap":False, 
        "snap_target":'CLOSEST', 
        "snap_point":(0, 0, 0), 
        "snap_align":False, 
        "snap_normal":(0, 0, 0), 
        "gpencil_strokes":False, 
        "cursor_transform":False, 
        "texture_space":False, 
        "remove_on_cancel":False, 
        "release_confirm":False, 
        "use_accurate":False, 
        "use_automerge_and_split":False})
    if dup_result != {"FINISHED"} :
        raise Exception("dup failed")
    new_obj = None
    for obj in bpy.data.objects :
        if obj not in before :
            new_obj = obj
            break
    if new_obj is None :
        raise Exception("Unable to find newly created object.")
    return new_obj

def triangulate(obj_object):
    change_to_object_mode()
    bpy.ops.object.select_all(action="DESELECT")
    obj_object.select_set(True)
    bpy.ops.object.modifier_add(type='TRIANGULATE')
    result=bpy.ops.object.modifier_apply(modifier="Triangulate")
    if result != {"FINISHED"} :
        raise Exception("triangulate failed")

def delete_object(obj_object) :
    change_to_object_mode()
    bpy.ops.object.select_all(action='DESELECT')
    obj_object.select_set(True)
    bpy.ops.object.delete() 
        
def tts_out(obj_object, file_name_extra="", triangles=True) :
    """Write the selected object for consumption by TTS"""

    
    # Normalize object rotation
    obj_object.rotation_euler[0] = 0
    obj_object.rotation_euler[1] = 0
    obj_object.rotation_euler[2] = 0 

    # Set the objects origin
    #bpy.ops.object.select_all(action='SELECT')
    #bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # Set object origin to origin
    obj_object.location[0] = 0
    obj_object.location[1] = 0
    obj_object.location[2] = 0    


    # Export the object
    # .obj name is same as .blend file with new extension.
    extension = bpy.context.blend_data.filepath.rfind(".blend")
    base=bpy.context.blend_data.filepath[:extension]
    obj_file = base + file_name_extra + ".obj"
    mtl_file = base + file_name_extra + ".mtl"

    if os.path.exists(obj_file) :
        os.unlink(obj_file)
    if os.path.exists(mtl_file) :
        os.unlink(mtl_file)

    bpy.ops.export_scene.obj(
      filepath=obj_file,
      check_existing=True,
      use_selection=True,
      use_mesh_modifiers=True,
      use_normals=True,
      use_uvs=True,
      use_materials=True,
      use_triangles=triangles,
      axis_forward='Z',
      axis_up='Y')

    return (obj_file, mtl_file)
      
def is_inside(point, ob):
    """Is a point inside an object?
       @param x,y of the point to check.
       @param obj Object we are checking against.
       @return None if the point is in the object, otherwise (x,y,z) where z is the top
         of the object for the point.
    """
    box_size = 0.15
    bpy.ops.mesh.primitive_cube_add(size=box_size, enter_editmode=False, align='WORLD', location=point, scale=(1,1,200))
    box=bpy.data.objects[bpy.context.active_object.name]
    vertices_before = len(box.data.vertices)
    try:
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
        bpy.context.object.modifiers["Boolean"].object =    ob
        bpy.ops.object.modifier_apply(modifier="Boolean")
        vertices_after =  len(box.data.vertices)
        if  (box.dimensions.x < box_size) or \
                 (box.dimensions.y < box_size) or \
                 (vertices_after != vertices_before) :
          return None
        # terrain detail sits on the top of the terrain
        z = max(map (lambda vertix: vertix.co[2], box.data.vertices))
        return (point.x, point.y, z)
    finally:
        bpy.data.objects.remove(box, do_unlink=True)
        pass
      
def calc_model_terrain_data(obj_object) :
    """Calculate points were terrain details such as trees can be placed."""
    # Set up a consistent environment
    bpy.context.scene.unit_settings.system = 'METRIC'

    #obj_object.dimensions.z = 4

    delta = 0.5
    nb_x = math.floor(obj_object.dimensions.x / delta)
    nb_y = math.floor(obj_object.dimensions.y / delta)

    points = []

    half_x = obj_object.dimensions.x / 2
    half_y = obj_object.dimensions.y / 2
    x = -half_x
    while x <= half_x :
        y = -half_y
        while y <= half_y :
            p = mathutils.Vector((x, y, 0.1))
            point = is_inside(p, obj_object) 
            if point is not None:
                points.append(point)
            y = y + delta
        x = x + delta
    return points          
      

def generate_terrain_data_file(obj) :
    # Export the objects points where terrain features may be placed.
    
    points = calc_model_terrain_data(obj)
    
    # _points.ttslua name is same as .blend file with new extension.
    extension = bpy.context.blend_data.filepath.rfind(".blend")
    base=bpy.context.blend_data.filepath[:extension]
    points_file = base + "_points.ttslua"

    if os.path.exists(points_file) :
        os.unlink(points_file)
                
        
    with open(points_file, "w") as terrain_data_stream:
      terrain_data_stream.write("g_terrain_data['%s']={\n" % (obj.name))
      terrain_data_stream.write("  points={" )
      for point in points :
        (x,y,z) = point
        terrain_data_stream.write("{x=%f, y=%f, z=%f}," % (x,z,y))
      terrain_data_stream.write("}\n}\n")
        
def find_background_file() :
  """Finds that background texture for a hill."""
  background_file = os.path.join( 
          os.path.dirname(bpy.context.blend_data.filepath),
          "background.jpg")
  if os.path.exists(background_file) :
      return background_file
  background_file = os.path.join( 
          os.path.dirname(bpy.context.blend_data.filepath),
          "..",
          "background.jpg")
  if os.path.exists(background_file) :
      return background_file
  raise Exception("background.jpg not found.")

def generate_texture(nt_obj_file) :
  """Generate the texture for a hill.
     Combines the background tile, with generated highlights for the peak and
     edge of the hill.

     @param nt_obj_file OBJ file for the non-triangulated version of the hill.
  """
  background_file = find_background_file()
  hilltexture.create_texture(nt_obj_file, background_file)


if len(bpy.context.selected_objects) != 1 :
    raise Exception("Exactly one object can be selected for duplicate")
obj_object = bpy.context.selected_objects[0]

(nt_obj_file, nt_mtl_file) = tts_out(obj_object, ".nt", triangles=False)
generate_texture(nt_obj_file) 

 
# Write out triangulated version of the object.
new_obj = duplicate(obj_object)     
triangulate(new_obj)
tts_out(new_obj)
delete_object(new_obj)


generate_terrain_data_file(obj_object)


print("DONE")
