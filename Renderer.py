import numpy as np
from PIL import Image as IMG
from math import radians, tan
from raster import *
from findIntersection import *
# Assuming Raster and Triangle classes are defined as given in Code 2
class Triangle3d:
    def __init__(self, vertices, color):
        self.vertices = vertices
        self.color = color
    def project2d(self, camera_position, camera_direction, clip_distance, raster_size, resolution):
        vertices2d = []
        for point in self.vertices:
            point2d = np.array(project(camera_position, camera_direction, clip_distance, point))
            print(point2d, 'point')
            point2d = [round((((point2d[0]/raster_size[0])+1)/2)*resolution[0]), round((((point2d[1]/raster_size[1])+1)/2)*resolution[1])]
            print()
            print(point2d, 'point2d')
            if point2d is None:
                return None
            vertices2d.append(point2d)
        return Triangle(vertices2d, self.color)
class Renderer:
    def __init__(self, resolution, position, direction, clip_distance, FOV):
        self.height, self.width = resolution
        self.position = np.array(position)
        self.direction = np.array(direction) / np.linalg.norm(direction)
        self.clip_distance = clip_distance
        self.FOV = radians(FOV)
        self.aspectRatio = self.width/self.height
        self.rasterSize = (tan(self.FOV / 2) * 2 * clip_distance , tan(self.FOV / 2) * 2 * clip_distance*self.aspectRatio)
        self.raster = Raster(resolution)
    def renderImage(self, triangles):
        for triangle in triangles:
            triangle2d = triangle.project2d(self.position, self.direction, self.clip_distance, self.rasterSize, (self.height, self.width))
            if triangle2d is not None:
                self.raster.draw(triangle2d)
        return self.raster.image

# Example of using Renderer
triangle1 = Triangle3d([[7, 1, 1], [7, 3, 1], [8, 2, -2]], (255, 0, 0, 255))
triangle2 = Triangle3d([[6, 0, 0], [7, -2, -1], [8, -2, 4]], (255, 255, 0, 255))
triangle3 = Triangle3d([[7, 1, 1], [7, 3, 1], [8, 2, 4]], (255, 0, 0, 255))

re = Renderer((2000, 2000), (0, 0, 0), (1, 0, 0), 5, 90)
re.renderImage([triangle1, triangle2, triangle3]).show()
