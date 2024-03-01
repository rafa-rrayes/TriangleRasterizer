from findIntersection import project
import numpy as np
class Triangle:
    def __init__(self, vertices, color, z):
        v1 = vertices[0]
        v2 = vertices[1]
        v3 = vertices[2]
        self.z = z
        self.vertices = np.array([[v1[0]+1, v1[1]+1], [v2[0]+1, v2[1]+1], [v3[0]+1, v3[1]+1]])
        self.color = color
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