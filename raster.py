import numpy as np
from numpy import array as vec
from PIL import Image as IMG

class Triangle:
    def __init__(self, vertices, color):
        v1 = vertices[0]
        v2 = vertices[1]
        v3 = vertices[2]
        self.vertices = vec([[v1[0]+1, v1[1]+1], [v2[0]+1, v2[1]+1], [v3[0]+1, v3[1]+1]])
        self.color = color
class Raster:
    def __init__(self,resolution):        
        self.width = resolution[0]+1
        self.height = resolution[1]+1
        self.image = np.zeros((self.width, self.height, 4))
        self.image = IMG.fromarray((self.image * 255).astype(np.uint8))
        self.blank = np.zeros((self.width, self.height, 4))
    def draw(self, triangle):        
        if triangle.vertices.shape != (3, 2):
            raise ValueError('Triangle must have 3 vertices')
        #check if vetices are within boundsd
        imagem = self.blank.copy()
        # Ensure color is set for the triangle if not provided in your triangle object
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
        
        for i in range(len(imagem)):
            linha = vec(imagem[i])
            linha = np.where((linha == [0, 0, 0, 0]).all(axis=1), 0, 1)
            dif = np.diff(linha)
            try:
                viraCor = np.where(dif == -1)[0][0]
                deixaCor = np.where(dif == 1)[0][1]
                linha[viraCor+1:deixaCor+1] = 1
            except:
                continue

            transformed_array_fast = np.zeros((linha.size, 4))
            # Apply transformation
            transformed_array_fast[linha == 0] = [0, 0, 0, 0]
            transformed_array_fast[linha == 1] = triangle_color
            imagem[i] = transformed_array_fast
        imagem = IMG.fromarray((imagem).astype(np.uint8))
        self.image = IMG.alpha_composite(self.image, imagem)
        return self.image
    def clear(self):
        self.image = self.blank.copy()
    def save(self, name):
        self.image.save(name)
