import numpy as np
from PIL import Image as IMG
from numba import njit, prange
class Raster:
    def __init__(self,resolution, useNumba=False):        
        self.width = resolution[1]+1
        self.height = resolution[0]+1
        self.image = np.zeros((self.width, self.height, 4))
        self.image = IMG.fromarray((self.image * 255).astype(np.uint8))
        self.useNumba = useNumba
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
            triangle_color = np.array([zto255, zto255, zto255, 255])
        else:
            triangle_color = np.array(triangle.color)
        # Draw edges
        
        # find triangle bounds
        if self.useNumba:
            imagem = drawLines(imagem, triangle.vertices, triangle_color)
            imagem = scanLine(imagem, triangle_color)
        else:
            
            imagem = drawLinesNormal(imagem, triangle.vertices, triangle_color)  
            imagem = scanLineNormal(imagem, triangle_color)  
        
        imagem = IMG.fromarray((imagem).astype(np.uint8))
        # make alpha composite
        self.image.paste(imagem, (boundX[0], boundY[0]), imagem)
        return self.image
    def clear(self):
        self.image = np.zeros((self.width, self.height, 4))
        self.image = IMG.fromarray((self.image * 255).astype(np.uint8))
    def save(self, name):
        self.image.save(name)
@njit(cache=True)
def scanLine(imagem, triangle_color):
    for i in range(len(imagem)):
        linha = imagem[i]
        linha = np.where(np_all_axis1((linha == np.array([0, 0, 0, 0]))), 0, 1)
        dif = np.diff(linha)
        indexVira = np.asarray(dif == -1).nonzero()
        indexDeixa = np.asarray(dif == 1).nonzero()
        if indexVira[0].size != 0:
            viraCor = indexVira[0][0]
        else:
            continue
        if indexDeixa[0].size!= 0:
            deixaCor = indexDeixa[0][-1]
        else:
            continue
        linha[viraCor+1:deixaCor+1] = 1
        transformed_array_fast = np.zeros((linha.size,4))
        # Apply transformation
        transformed_array_fast[linha == 0] = np.array([0, 0, 0, 0])
        transformed_array_fast[linha == 1] = triangle_color
        
        imagem[i] = transformed_array_fast
    return imagem
@njit(cache=True)
def np_all_axis1(x):
    """Numba compatible version of np.all(x, axis=1)."""
    out = np.ones(x.shape[0], dtype=np.bool8)
    for i in range(x.shape[1]):
        out = np.logical_and(out, x[:, i])
    return out
def scanLineNormal(imagem, triangle_color):
    for i in range(len(imagem)):
        linha = imagem[i]
        linha= np.where((linha == np.array([0, 0, 0, 0])).all(axis=1), 0, 1)
        dif = np.diff(linha)
        indexVira = np.asarray(dif == -1).nonzero()
        indexDeixa = np.asarray(dif == 1).nonzero()
        if indexVira[0].size != 0:
            viraCor = indexVira[0][0]
        else:
            continue
        if indexDeixa[0].size!= 0:
            deixaCor = indexDeixa[0][-1]
        else:
            continue
        linha[viraCor+1:deixaCor+1] = 1
        transformed_array_fast = np.zeros((linha.size,4))
        # Apply transformation
        transformed_array_fast[linha == 0] = np.array([0, 0, 0, 0])
        transformed_array_fast[linha == 1] = np.array(triangle_color)
        
        imagem[i] = transformed_array_fast
    return imagem
@njit(cache=True)
def drawLines(imagem, vertices, triangle_color):
    for i in prange(3):
        if i == 2:
            first, last = vertices[2], vertices[0]
        else:
            first, last = vertices[i], vertices[i+1]
        # Swap if first is to the right of last to simplify drawing logic
        if first[0] > last[0]:
            first, last = last, first

        dx = last[0] - first[0]
        dy = last[1] - first[1]
        if dx != 0:
            slope = dy / dx
        elif dy != 0:
            slope = np.inf
        else:
            slope = 0
        previousY = round(first[1])
        if dx == 0:  # Vertical line
            for y in range(int(min(first[1], last[1])), int(max(first[1], last[1])) + 1):
                imagem[round(y)][round(first[0])] = triangle_color
        else:
            for x in range(int(first[0]), int(last[0]) + 1):
                change = False
                y = round(first[1] + slope * (x - first[0]))
                if 0 <= x < imagem.shape[1] and 0 <= y < imagem.shape[0]:  # Check bounds
                    imagem[y][x] = triangle_color
                    if abs(previousY - y)> 1:
                        if previousY > y:
                            y, previousY = previousY, y
                            change = True
                        try:
                            for i in range(previousY+1, y):
                                imagem[i][x-1] = triangle_color
                        except:
                            pass                                
                        if change:
                            y, previousY = previousY, y
                    previousY = y
    return imagem
def drawLinesNormal(imagem, vertices, triangle_color):
    for i in range(3):
        if i == 2:
            first, last = vertices[2], vertices[0]
        else:
            first, last = vertices[i], vertices[i+1]
        # Swap if first is to the right of last to simplify drawing logic
        if first[0] > last[0]:
            first, last = last, first

        dx = last[0] - first[0]
        dy = last[1] - first[1]
        if dx != 0:
            slope = dy / dx
        elif dy != 0:
            slope = np.inf
        else:
            slope = 0
        previousY = round(first[1])
        if dx == 0:  # Vertical line
            for y in range(int(min(first[1], last[1])), int(max(first[1], last[1])) + 1):
                imagem[round(y)][round(first[0])] = triangle_color
        else:
            for x in range(int(first[0]), int(last[0]) + 1):
                change = False
                y = round(first[1] + slope * (x - first[0]))
                if 0 <= x < imagem.shape[1] and 0 <= y < imagem.shape[0]:  # Check bounds
                    imagem[y][x] = triangle_color
                    if abs(previousY - y)> 1:
                        if previousY > y:
                            y, previousY = previousY, y
                            change = True
                        try:
                            for i in range(previousY+1, y):
                                imagem[i][x-1] = triangle_color
                        except:
                            pass                                
                        if change:
                            y, previousY = previousY, y
                    previousY = y
    return imagem