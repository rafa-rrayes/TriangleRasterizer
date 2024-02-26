import toRaster
import numpy as np
from numpy import array as vec
from PIL import Image as IMG
import time
global temp1
temp1 = 0
global temp2
temp2 = 0
global temp3
temp3 = 0
class Triangle:
    def __init__(self, v1, v2, v3, color):
        self.vertices = vec([[v1[0]+1, v1[1]+1], [v2[0]+1, v2[1]+1], [v3[0]+1, v3[1]+1]])
        self.color = color
class Screen:
    def __init__(self, width, height):
        self.width = height+1
        self.height = width+1
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
            print(dif)
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
    def save(self, name):
        self.image.save(name)
tela = toRaster.Raster([20,20], [200, 200 ], 2)

point1 = vec([4.0, 3.0, 3.0])
point3 = vec([1.0, 6.0, 3.0])
point4 = vec([5.0, 7.0, 2.0])
point5 = vec([3.0, 5.0, 5.0])


p1 = tela.CalculatePoint(point1)
p3 = tela.CalculatePoint(point3)
p4 = tela.CalculatePoint(point4)
p5 = tela.CalculatePoint(point5)

tri1 = Triangle(p1,p3, p4, [255, 0, 0, 128])
tri2 = Triangle(p1,p3, p5, [255, 255, 255, 128])
tri3 = Triangle(p3,p4, p5, [0, 0, 255, 128])
tri4 = Triangle(p1,p4, p5, [255, 255, 0, 128])
tela2 = Screen(200, 200)
tempo = time.time()
tela2.draw(tri1)
# tela2.draw(tri2)
# tela2.draw(tri3)
# tela2.draw(tri4)
print(time.time()-tempo)
tela2.save('imagemFinal.png')

# import pygame

# import sys

# # Initialize Pygame
# pygame.init()

# # Set the width and height of the screen (width, height).
# screen = pygame.display.set_mode((800, 500))

# # Set the title of the window
# pygame.display.set_caption("Pygame Image Display")

# size = tela2.image.size
# mode = tela2.image.mode
# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         # check if key is pressed
#         keys=pygame.key.get_pressed()
#         if keys[pygame.K_a]:
#             point1 -= vec([0.1, 0, 0])
#             # point3 -= vec([0.1, 0, 0])
#             # point4 -= vec([0.1, 0, 0])
#             # point5 -= vec([0.1, 0, 0])
#         if keys[pygame.K_d]:
#             point1 += vec([0.1, 0, 0])
#             # point3 += vec([0.1, 0, 0])
#             # point4 += vec([0.1, 0, 0])
#             # point5 += vec([0.1, 0, 0])
#         if keys[pygame.K_s]:
#             point1 += vec([0, 0, 0.1])
#             # point3 += vec([0, 0, 0.1])
#             # point4 += vec([0, 0, 0.1])
#             # point5 += vec([0, 0, 0.1])
#         if keys[pygame.K_w]:
#             point1 -= vec([0, 0, 0.1])
#             # point3 -= vec([0, 0, 0.1])
#             # point4 -= vec([0, 0, 0.1])
#             # point5 -= vec([0, 0, 0.1])
#         if keys[pygame.K_f]:
#             point1 -= vec([0, 0.1, 0])
#             # point3 -= vec([0, 0.1, 0])
#             # point4 -= vec([0, 0.1, 0])
#             # point5 -= vec([0, 0.1, 0])
#         if keys[pygame.K_g]:
#             point1 += vec([0, 0.1, 0])
#             # point3 += vec([0, 0.1, 0])
#             # point4 += vec([0, 0.1, 0])
#             # point5 += vec([0, 0.1, 0])
#         tela2 = Screen(800, 500)
#         p1 = tela.CalculatePoint(point1)
#         p3 = tela.CalculatePoint(point3)
#         p4 = tela.CalculatePoint(point4)
#         p5 = tela.CalculatePoint(point5)
#         tri1 = Triangle(p1,p3, p4, [1, 0, 0])
#         tri2 = Triangle(p1,p3, p5, [1, 1, 1])
#         tri3 = Triangle(p3,p4, p5, [0, 0, 1])
#         tri4 = Triangle(p1,p4, p5, [1, 1, 0])
#         tela2.draw(tri1)
#         tela2.draw(tri2)
#         tela2.draw(tri3)
#         tela2.draw(tri4)

#     # Fill the screen with black
#     data = tela2.image.tobytes()
#     image = pygame.image.fromstring(data, size, mode)
#     screen.fill((0, 0, 0))
#     # check if user presses A or D
#     # Blit the image on the screen at (0, 0)
#     screen.blit(image, (0, 0))

#     # Update the display
#     pygame.display.flip()

# # Quit Pygame
# pygame.quit()
# sys.exit()