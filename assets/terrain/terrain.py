#!/usr/bin/python3

# Run this script in Blender prior to committing the 
# objects to GitHub so they can be consumed by
# TableTop Simulator.
#
# After executing the script check that the objects are
# still sane in Blender by examining from the "+z axis".

# In the blender console
# import importlib
# import sys
# sys.path.append( 'c:\\Users\\marcp\\GitHub\\Triumph_TTS\\assets\\terrain' )
# import terrain
# To reload:
# terrain = importlib.reload(terrain)
#
# To generate data file containing location of terrain.
#   terrain.terrain_data()
#
# To take an .obj file and make it ready for use in TTS:
#   terrain.clean_obj("name of file without .obj extension") 



import bpy
import glob
import math
import mathutils
import os
import sys
from math import pi, acos

terrain_dir = "c:\\users\\marcp\\GitHub\\Triumph_TTS\\assets\\terrain"
if not os.path.exists(terrain_dir) :
    raise Exception("terrain_dir does not exist: " + terrain_dir)

terrain_data_file = os.path.join(terrain_dir, "terrain_data.ttslua")

#def is_inside(p, obj, max_dist=1.84467e+19 ):
#    """
#    https://blender.stackexchange.com/questions/31693/how-to-find-if-a-point-is-inside-a-mesh
#    """
#    result, point, normal, face = obj.closest_point_on_mesh(origin=p, distance=max_dist)
#    if not result :
#        return False
#    if point is None:
#        return False
#    p2 = point-p
#    v = p2.dot(normal)
#    inside = not(v < 0.0)
#    if inside :
#        print("inside ", p, " ", point)
#    return inside


#def is_inside(target_pt_global, mesh_obj, tolerance=0.05):
#    """
#    https://blender.stackexchange.com/questions/31693/how-to-find-if-a-point-is-inside-a-mesh
#    """
#
#    # Convert the point from global space to mesh local space
#    target_pt_local = mesh_obj.matrix_world.inverted() @ target_pt_global
#
#    # Find the nearest point on the mesh and the nearest face normal
#    _, pt_closest, face_normal, _ = mesh_obj.closest_point_on_mesh(target_pt_local)
#
#    # Get the target-closest pt vector
#    target_closest_pt_vec = (pt_closest - target_pt_local).normalized()
#
#    # Compute the dot product = |a||b|*cos(angle)
#    dot_prod = target_closest_pt_vec.dot(face_normal)
#
#    # Get the angle between the normal and the target-closest-pt vector (from the dot prod)
#    angle = acos(min(max(dot_prod, -1), 1)) * 180 / pi
#
#    # Allow for some rounding error
#    inside = angle < 90-tolerance
#    if inside :
#        print("inside ", target_pt_global, " ", pt_closest)
#
#    return inside

#def is_inside(point,ob):
#  """
#  https://blender.stackexchange.com/questions/31693/how-to-find-if-a-point-is-inside-a-mesh
#  """
#  axes = [ mathutils.Vector((1,0,0)) ]
#  outside = False
#  for axis in axes:
#    mat = ob.matrix_world
#    mat.invert()
#    orig = mat @ point
#    count = 0
#    while True:
#        contact, location,normal,index = ob.ray_cast(orig,orig+axis*10000.0)
#        print(point, " ", contact, " ", location, " ", normal, " ", index)
#        if not contact :
#            return False
#        if index == -1: break
#        count += 1
#        orig = location + axis*0.00001
#    if count%2 == 0:
#        outside = True
#        break
#  return not outside

def is_inside(point,ob):
    box_size = 0.15
    bpy.ops.mesh.primitive_cube_add(size=box_size, enter_editmode=False, align='WORLD', location=point, scale=(1,1,1))
    box=bpy.data.objects[bpy.context.active_object.name]
    vertices_before = len(box.data.vertices)
    try:
        bpy.ops.object.modifier_add(type='BOOLEAN')
        bpy.context.object.modifiers["Boolean"].operation = 'INTERSECT'
        bpy.context.object.modifiers["Boolean"].object =    ob
        bpy.ops.object.modifier_apply(modifier="Boolean")
        vertices_after =  len(box.data.vertices)
        result = (box.dimensions.x >= box_size) and \
                 (box.dimensions.y >= box_size) and \
                 (box.dimensions.z >= box_size) and \
                 (vertices_after == vertices_before) 
#        if not result:
#            bpy.data.objects.remove(box, do_unlink=True)
#        print(result, point)
        return result
    finally:
        bpy.data.objects.remove(box, do_unlink=True)
        pass

def remove_all_objects() :
    while len(bpy.data.objects) > 0:
        bpy.data.objects.remove(bpy.data.objects[-1], do_unlink=True)

def import_model(model_name) :
    obj_file= os.path.join(terrain_dir, model_name + ".obj")
    imported_object = bpy.ops.import_scene.obj(filepath=obj_file)
    obj_object = bpy.context.selected_objects[0] # Source file must have only one object
    obj_object.name = model_name
    print('Imported name: ', obj_object.name)
    return obj_object
    
def normalize(obj_object) :
    """Scale and orient the terrain object."""

    # Set height of object
    obj_object.dimensions.y = 0.04

    # Normalize object rotation
    obj_object.rotation_euler[0] = 1.5708
    obj_object.rotation_euler[1] = 0
    obj_object.rotation_euler[2] = 0 #1.5708

    # Set the objects origin
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

    # Set object origin to origin
    obj_object.location[0] = 0
    obj_object.location[1] = 0
    obj_object.location[2] = 0    

def clean_obj(model_name):
    obj_file= os.path.join(terrain_dir, model_name + ".obj")
    mtl_file= os.path.join(terrain_dir, model_name + ".mtl")

    # Set up a consistent environment
    bpy.context.scene.unit_settings.system = 'METRIC'

    # Delete all objects
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

    # import the file we are going to normalize
    obj_object = import_model(model_name)

    normalize(obj_object)

    # Export the object
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
      use_triangles=True,
      axis_forward='Z',
      axis_up='Y')
      


def calc_model_terrain_data(model_name) :
    """Write out the terrain data for a model."""
    # Set up a consistent environment
    bpy.context.scene.unit_settings.system = 'METRIC'

    remove_all_objects()

    # import the file we are going to normalize
    obj_object = import_model(model_name)
    obj_object.dimensions.y = 4

    box_size = 0.15    
    delta = 0.5
    nb_x = math.floor(obj_object.dimensions.x / delta)
    nb_z = math.floor(obj_object.dimensions.z / delta)
    
    points = []

    half_x = obj_object.dimensions.x / 2
    half_z = obj_object.dimensions.z / 2
    x = -half_x
    while x <= half_x :
        z = -half_z
        while z <= half_z :
            p = mathutils.Vector((x, z, 0))
            if is_inside(p, obj_object) :
                points.append((x,z))
            z = z + delta
        x = x + delta
    return points

def model_terrain_data(terrain_data_stream, model_name) :
    """Write out the terrain data for a model."""
    points = calc_model_terrain_data(model_name)
    terrain_data_stream.write("g_terrain_data['%s']={\n" % (model_name))
    terrain_data_stream.write("  points={" )
    for point in points :
        (x,z) = point
        terrain_data_stream.write("{x=%f, z=%f}," % (x,-z))
    terrain_data_stream.write("}\n}\n")

def terrain_data() :
    """Create the terrain data .ttslua file"""
    terrain_data_stream = open(terrain_data_file, "w")
    terrain_data_stream.write("g_terrain_data = {}\n")
    files=os.listdir(terrain_dir)
    files.sort()
    for file in files:
        if file.endswith(".obj") :
            if ("Rough" in file) or ("Woods" in file) or ("Marsh" in file) or ("Oasis" in file):
                print("processing ", file[:-4])
                model_terrain_data(terrain_data_stream, file[:-4])
    terrain_data_stream.close()      
            



#files=os.listdir(terrain_dir)
#files.sort()
#for file in files:
#  if file.endswith(".obj") :
#    if "Oasis" in file or "Marsh" in file :
#        print("Cleaning ", file[:-4])
#        clean_obj(file[:-4])
##
terrain_data()

#calc_model_terrain_data("terrain Marsh #70")

print("DONE")
