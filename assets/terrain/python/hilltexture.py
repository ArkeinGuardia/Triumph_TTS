import math
import os
import pathlib
import subprocess
import sys
from typing import List, Tuple

magick = "C:\\Program Files\\ImageMagick-7.1.0-Q16-HDRI\\magick"

ModelCoordinates = Tuple[float, float, float]
TextureCoordinates = Tuple[float, float]


class FacePoint:

    def __init__(self, vertex: ModelCoordinates, texture: TextureCoordinates):
        self.vertex = vertex
        self.texture = texture


class Face:
    def __init__(self, points: List[FacePoint]):
        self.points = points

    def edges(self) -> List[Tuple[FacePoint, FacePoint]]:
        result = []
        prev = self.points[0]
        for v in self.points[1:]:
            result.append((prev, v))
            prev = v
        result.append((self.points[-1], self.points[0]))
        return result


class OBJ:
    def __init__(self, filename):
        """Load a Wavefront OBJ file"""
        self.vertices: List[ModelCoordinates] = []
        self.textcoords: TextureCoordinates = []
        self.faces: List[Face] = []

        for line in open(filename, "r"):
            if line.startswith("#"): continue
            values = line.split()
            if not values: continue
            if values[0] == "v":
                v = map(float, values[1:])
                self.vertices.append(list(v))
                pass
            elif values[0] == "vt":
                v = map(float, values[1:])
                self.textcoords.append(list(v))
                pass
            elif values[0] == "f":
                face = []
                texcoords = []
                for v in values[1:]:
                    w = v.split('/')

                    vertix_index = int(w[0])
                    if (len(w) >= 2) and (len(w[1]) > 0):
                        texture_index = int(w[1])
                    else:
                        texture_index = 0
                    vertix = self.vertices[vertix_index - 1]
                    texture = self.textcoords[texture_index - 1]
                    fp = FacePoint(vertix, texture)
                    face.append(fp)
                self.faces.append(Face(face))
            else:
                # Ignored for now
                pass

    def face_to_vertices(self, face: Face) -> List[ModelCoordinates]:
        """
        @param face Face object.
        @return Coordinates of the vertices that make up a face.
        """

        def get_vertix(fp: FacePoint) -> ModelCoordinates:
            return fp.vertex

        return list(map(get_vertix, face))

    def face_to_textures(self, face):
        """
        @param face Face object.
        @return Coordinates of the texture that make up a face.
        """
        coords = []
        for v in face['texture']:
            if v < 1:
                raise Exception("negative texture index not handled: " + str(v))
            coords.append(self.textcoords[v - 1])
        return coords

    def bounding_box(self):
        bl = [sys.float_info.max, sys.float_info.max, sys.float_info.max]
        tr = [-sys.float_info.max, -sys.float_info.max, -sys.float_info.max]
        for v in self.vertices:
            tr[0] = max(tr[0], v[0])
            tr[1] = max(tr[1], v[1])
            tr[2] = max(tr[2], v[2])
            bl[0] = min(bl[0], v[0])
            bl[1] = min(bl[1], v[1])
            bl[2] = min(bl[2], v[2])
        bb = {"tr": tr, "bl": bl}
        if not ( (tr[0] > 0) and
                 (tr[1] > 0) and
                 (bl[0] < 0) and
                 (bl[1] < 0) ) :
            print("Bounding box invalid ", bb)
            raise Exception("bounding box invalid " + str(bb))
        return bb

    def edges(self) -> List[Tuple[FacePoint, FacePoint]]:
        edges = []
        for face in self.faces:
            edges.extend(face.edges())
        return edges


texture_size = 512


def texture_to_pixels(texture):
    return [int(texture[0] * texture_size), texture_size - int(texture[1] * texture_size)]


def texture_points_to_line(start, end):
    s = texture_to_pixels(start)
    e = texture_to_pixels(end)
    return "line %d,%d %d,%d" % (s[0], s[1], e[0], e[1])


def texture_to_lines(texture):
    lines = []
    for v in range(1, len(texture)):
        lines.append(texture_points_to_line(texture[v - 1], texture[v]))
    lines.append(texture_points_to_line(texture[-1], texture[0]))
    return lines


def is_top(bounding_box, vertices: List[FacePoint]):
    """Are all vertices at the top of the bounding box."""
    top = bounding_box["tr"][1]
    def is_close(v:FacePoint) :
        return math.isclose(top, v.vertex[1], abs_tol=0.0001)
    return all( map(is_close, vertices))



def is_bottom(bounding_box, vertices: List[FacePoint]):
    """Are all vertices at the bottom of the bounding box."""
    bottom = bounding_box["bl"][1]
    def is_close(v:FacePoint) :
        return math.isclose(bottom, v.vertex[1], abs_tol=0.0001)
    return all( map(is_close, vertices))

def create_texture(nt_obj_file, background_file):
    """ Creates a texture file for a hill.
        @param nt_obj_file OBJ file that contains the non-triangulated data for
          the hill.
        @param background_file Texture for the the hill that will have super
          imposed on it markings for the peak and base of the hill.
    """
    obj_path = pathlib.Path(nt_obj_file)
    o = OBJ(nt_obj_file)
    bb = o.bounding_box()
    highlight_path = obj_path.parent.joinpath(obj_path.name[:-4] + ".higlights.png")
    print(highlight_path)
    if os.path.exists(highlight_path):
        os.unlink(highlight_path)
    cmd = [magick, 'convert', '-size',
           str(texture_size) + "x" + str(texture_size),
           'canvas:white']
    cmd.append("-fill")
    cmd.append("black")
    cmd.append("-strokewidth")
    cmd.append("3")
    for edge in o.edges():
        if is_bottom(bb, edge) or is_top(bb, edge):
            t0 = edge[0].texture
            t1 = edge[1].texture
            line = texture_points_to_line(t0, t1)
            cmd.append("-draw")
            cmd.append(line)

    cmd.append(str(highlight_path))
    print(cmd)
    print(" ".join(cmd))
    subprocess.check_call(cmd)

    texture_path = obj_path.parent.joinpath(obj_path.name[:-7] + ".jpg")

    cmd = [magick, "composite", "-compose", "darken",
           str(highlight_path), background_file,
           str(texture_path)]
    subprocess.check_call(cmd)



