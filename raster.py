import numpy as np
from numpy import array as vec
from PIL import Image as IMG
import time
class Triangle:
    def __init__(self, vertices, color, z):
        v1 = vertices[0]
        v2 = vertices[1]
        v3 = vertices[2]
        self.z = z
        self.vertices = vec([[v1[0]+1, v1[1]+1], [v2[0]+1, v2[1]+1], [v3[0]+1, v3[1]+1]])
        self.color = color
        
class Raster:
    def __init__(self,resolution):        
        self.width = resolution[1]+1
        self.height = resolution[0]+1
        self.image = np.zeros((self.width, self.height, 4))
        self.image = IMG.fromarray((self.image * 255).astype(np.uint8))
    def draw(self, triangle, z_buffer=False):
        if triangle.vertices.shape != (3, 2):
            raise ValueError('Triangle must have 3 vertices')
        #check if vetices are within boundsd
        boundX = [min(triangle.vertices[0][0], triangle.vertices[1][0], triangle.vertices[2][0]), max(triangle.vertices[0][0], triangle.vertices[1][0], triangle.vertices[2][0])]
        boundY = [min(triangle.vertices[0][1], triangle.vertices[1][1], triangle.vertices[2][1]), max(triangle.vertices[0][1], triangle.vertices[1][1], triangle.vertices[2][1])]
        imagem = np.zeros((boundY[1]-boundY[0]+1, boundX[1]-boundX[0]+1, 4))
        triangle.vertices = triangle.vertices - [boundX[0], boundY[0]]
        # Ensure color is set for the triangle if not provided in your triangle object
        if z_buffer:
            zto255 = max(min((((triangle.z-0.09)/0.035)*255 + 30), 255), 0)
            triangle_color = (zto255, zto255, zto255, 255)
        else:
            triangle_color = triangle.color
        linhas = []
        # Draw edges
        for i in range(3):
            linha = []
            if i == 2:
                first, last = triangle.vertices[2], triangle.vertices[0]
            else:
                first, last = triangle.vertices[i], triangle.vertices[i+1]
            # Swap if first is to the right of last to simplify drawing logic
            if first[0] > last[0]:
                first, last = last, first

            dx = last[0] - first[0]
            dy = last[1] - first[1]
            try:
                slope = dy / dx
            except ZeroDivisionError:
                slope = np.inf
            previousY = round(first[1])
            if dx == 0:  # Vertical line
                for y in range(int(min(first[1], last[1])), int(max(first[1], last[1])) + 1):
                    imagem[round(y)][round(first[0])] = triangle_color
                    linha.append([round(y),round(first[0])])
            
            else:
                for x in range(int(first[0]), int(last[0]) + 1):
                    change = False
                    y = round(first[1] + slope * (x - first[0]))
                    if 0 <= x < imagem.shape[1] and 0 <= y < imagem.shape[0]:  # Check bounds
                        imagem[y][x] = triangle_color
                        linha.append([y, x])
                        if abs(previousY - y)> 1:
                            if previousY > y:
                                y, previousY = previousY, y
                                change = True
                            try:
                                for i in range(previousY+1, y):
                                    imagem[i][x-1] = triangle_color
                                    linha.append([y, x])
                            except:
                                pass                                
                            if change:
                                y, previousY = previousY, y
                        previousY = y
            linhas.append(linha)
        # find triangle bounds
        
        for i in range(len(imagem)):
            linha = vec(imagem[i])
            
            linha = np.where((linha == [0, 0, 0, 0]).all(axis=1), 0, 1)
            dif = np.diff(linha)
            try:
                viraCor = np.where(dif == -1)[0][0]
            except:
                continue
            try:
                deixaCor = np.where(dif == 1)[0][1]
            except:
                try:
                    deixaCor = np.where(dif == 1)[0][0]
                except:
                    continue
            linha[viraCor+1:deixaCor+1] = 1
            transformed_array_fast = np.zeros((linha.size,4))
            # Apply transformation
            transformed_array_fast[linha == 0] = [0, 0, 0, 0]
            transformed_array_fast[linha == 1] = triangle_color
            imagem[i] = transformed_array_fast
        
        imagem = IMG.fromarray((imagem).astype(np.uint8))
        # make alpha composite
        self.image.paste(imagem, (boundX[0], boundY[0]), imagem)
        return self.image
    def clear(self):
        self.image = np.zeros((self.width, self.height, 4))
        self.image = IMG.fromarray((self.image * 255).astype(np.uint8))
    def save(self, name):
        self.image.save(name)
