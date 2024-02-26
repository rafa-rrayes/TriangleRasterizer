import numpy as np
from PIL import Image as IMG
from math import radians, tan
from raster import *
from findIntersection import *
# Assuming Raster and Triangle classes are defined as given in Code 2
class Triangle3d:
    def __init__(self, vertices, color):
        self.vertices = np.array(vertices)
        self.color = color
    def project2d(self, camera_position, camera_direction, clip_distance):
        vertices2d = []
        for point in self.vertices:
            point2d = project(camera_position, camera_direction, clip_distance, point)
            if point2d is None:
                print('Point is behind the camera')
                return None
            vertices2d.append(project(camera_position, camera_direction, clip_distance, point))
        return Triangle(vertices2d, self.color)
class Renderer:
    def __init__(self, resolution, position, direction, clip_distance, FOV):
        self.width, self.height = resolution
        self.position = np.array(position)
        self.direction = np.array(direction) / np.linalg.norm(direction)
        self.clip_distance = clip_distance
        self.FOV = radians(FOV)
        self.aspect_ratio = self.width / self.height
        self.raster = Raster(resolution)

    def project_to_2d(self, triangle):
        for point in triangle.vertices:
            print(point)

    def renderImage(self, triangles):
        for triangle in triangles:
            self.raster.draw(triangle)
        return self.raster.image

# Example of using Renderer
triangle1 = Triangle3d([[5, 1, 1], [5, 3, 1], [7, 2, -2]], (1, 0, 0, 0))
tri = triangle1.project2d((0, 0, 0), (-1, 0, 0), 2)
re = Renderer((800, 600), (0, 0, 0), (1, 0, 0), 2, 60)
triangles = [tri]
re.renderImage(triangles).show()

# Initialize Renderer

# Render image from 3D triangles
# image = re.renderImage(triangles)
