import random
from triangle import Triangle3d
def extractTriangles(filepath):
    with open(filepath, "r") as file:
        text = file.read()
    text = text.replace("solid ASCII", "")
    text = text.replace("endsolid", "")
    text = text.replace("endloop", "triangle")
    text = text.replace("outer loop", "triangle")
    text = text.split("triangle")
    text = [x for x in text if 'vertex' in x]
    text = [x.replace("      vertex   ", "") for x in text]

    text = "".join(text)
    text = text.removeprefix("\n")
    text = text.removesuffix("\n    ")
    text = text.split("\n    \n")
    listTriangles = []
    for i in text:
        triangulo = i.split("\n")
        triangulo3d = []
        ponto3d = []
        for i in triangulo:
            ponto = i.split(" ")
            ponto3d.append(float(ponto[0]))
            ponto3d.append(float(ponto[1]))
            ponto3d.append(float(ponto[2]))
            triangulo3d.append(ponto3d)
            ponto3d = []
        listTriangles.append(Triangle3d(triangulo3d, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)))

    return listTriangles
