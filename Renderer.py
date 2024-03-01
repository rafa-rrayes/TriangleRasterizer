import numpy as np
from PIL import Image as IMG
from math import radians, tan
from raster import *
from findIntersection import *
from extractor import *
import random
# Assuming Raster and Triangle classes are defined as given in Code 2
class Triangle3d:
    def __init__(self, vertices, color):
        self.vertices = vertices
        self.color = color
    def project2d(self, camera_position, camera_direction, clip_distance, raster_size, resolution):
        vertices2d = []
        for point in self.vertices:
            try:
                point2d, z = project(camera_position, camera_direction, clip_distance, point)
                point2d = np.array(point2d)
            except:
                return None
            
            point2d = [round((((point2d[0]/raster_size[0])+1)/2)*resolution[0]), round((((point2d[1]/raster_size[1])+1)/2)*resolution[1])]
            vertices2d.append(point2d)
        return Triangle(vertices2d, self.color, z)
class Renderer:
    def __init__(self, resolution, position, direction, clip_distance, FOV):
        self.height, self.width = resolution
        self.position = np.array(position)
        self.direction = np.array(direction) / np.linalg.norm(direction)
        self.clip_distance = clip_distance
        self.FOV = radians(FOV)
        self.aspectRatio = self.width/self.height
        self.rasterSize = (tan(self.FOV / 2) * clip_distance , tan(self.FOV / 2) * clip_distance*self.aspectRatio)
        self.raster = Raster(resolution)
    def renderImage(self, triangles):
        # sort triangles by z, each triangle has a z value
        triangles2d = []    
        for triangle in triangles:

            triangle2d = triangle.project2d(self.position, self.direction, self.clip_distance, self.rasterSize, (self.height, self.width))
            if triangle2d is not None:

                triangles2d.append(triangle2d)
        triangles2d.sort(key=lambda triangle: triangle.z, reverse=True)
        print(triangles2d[0].z, triangles2d[-1].z)
        for triangle2d in triangles2d:
                self.raster.draw(triangle2d, z_buffer=True)

        return self.raster.image

# # Example of using Renderer
triangles = []
for i in extractTriangles("Donut.stl"):
    triangles.append(Triangle3d(i, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)))
re = Renderer((1920, 1080), (0, -1, 0), (0, 1, 0), 3, 120)
import time
tempo = time.time()
image = re.renderImage(triangles)
print(time.time()-tempo)
image.show()