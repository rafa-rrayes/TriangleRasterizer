import numpy as np
from PIL import Image as IMG
from math import radians, tan
from raster import *
from findIntersection import *
from extractor import *
import time

# Assuming Raster and Triangle classes are defined as given in Code 2

class Renderer:
    def __init__(self, resolution, position, direction, clip_distance, FOV):
        self.height, self.width = resolution
        self.position = np.array(position)
        self.direction = np.array(direction) / np.linalg.norm(direction)
        self.clip_distance = clip_distance
        self.FOV = radians(FOV)
        self.aspectRatio = self.width/self.height
        self.rasterSize = (tan(self.FOV / 2) * clip_distance , tan(self.FOV / 2) * clip_distance*self.aspectRatio)
        self.raster = Raster(resolution, useNumba=True)
    def renderImage(self, triangles):
        # sort triangles by z, each triangle has a z value
        triangles2d = []    
        for triangle in triangles:

            triangle2d = triangle.project2d(self.position, self.direction, self.clip_distance, self.rasterSize, (self.height, self.width))
            if triangle2d is not None:

                triangles2d.append(triangle2d)
        triangles2d.sort(key=lambda triangle: triangle.z, reverse=True)
        for triangle2d in triangles2d:
                self.raster.draw(triangle2d, z_buffer=False)

        return self.raster.image

# # Example of using Renderer
triangles = extractTriangles("Donut.stl")
re = Renderer((1920, 1080), (0, -1,0), (0, 1, 0), 3, 120)
totalTime = []
re.renderImage(triangles).show()

for i in range(10):
    start = time.time()
    re.renderImage(triangles)
    totalTime.append(time.time()-start)
print(sum(totalTime)/len(totalTime))
