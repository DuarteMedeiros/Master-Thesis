from Polygon import myPolygon
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MatplotlibPolygon
import math
from MinimalEnclosingCircle import*

random.seed()


def random_polygons(n):
    file = open(r"Polygon_Examples\\Compactness_by_id.txt", "w", encoding="utf-8")
    file.write(f"Polygon\tArea\tPeri\tMD\trm\tA/P2\tR(A)/P\tA/MD2\tR(A)/MD\tPc/P\tA/r2\n")
    for id in range(1, n + 3):
        print(f"id = {id}")
        vertices = []
        if id == n + 1:
            polygon = myPolygon()
            polygon.add_point((0, 0))
            vertices.append([0,0])
            polygon.add_point((0, 1))
            vertices.append([0,1])
            polygon.add_point((1, 1))
            vertices.append([1,1])
            polygon.add_point((1, 0))
            vertices.append([1,0])
            polygon.set_id(id)
        elif id == n + 2:
            polygon = myPolygon()
            polygon.add_point((1 / 2, 0))
            vertices.append([1 / 2, 0])
            polygon.add_point((3 / 2, 0))
            vertices.append([3 / 2, 0])
            polygon.add_point((2, 3 / 4))
            vertices.append([2, 3 / 4])
            polygon.add_point((3 / 2, 3 / 2))
            vertices.append([3 / 2, 3 / 2])
            polygon.add_point((1 / 2, 3 / 2))
            vertices.append([1 / 2, 3 / 2])
            polygon.add_point((0, 3 / 4))
            vertices.append([0, 3 / 4])
            polygon.set_id(id)
        else:
            polygon = myPolygon()
            n_vertices = random.randint(5, 10)
            for point in range(n_vertices):
                x = random.randint(1, 10)
                y = random.randint(1, 10)
                polygon.add_point((x, y))
                vertices.append([x,y])
                polygon.set_id(id)

        print(vertices)
        
        area = polygon.get_area()
        perimeter = polygon.get_perimeter()
        max_distance = polygon.get_max_distance()
        mec = minimum_enclosing_circle(vertices)
        radious = mec[1]

        polygon.save_polygon()

        compactness1 = 4 * math.pi * area / (perimeter**2)
        compactness2 = 2 * math.sqrt(math.pi * area) / perimeter
        compactness4 = 2 * math.sqrt(area) / (max_distance * math.sqrt(math.pi))
        compactness3 = 4 * area / (math.pi * max_distance**2)
        compactness5 = 2 * math.pi * math.sqrt(area/math.pi) / perimeter
        compactness6 = area / radious**2

        file.write(
            f"{polygon.get_id()}\t{round(area,2)}\t{round(perimeter,2)}\t{round(max_distance,2)}\t{round(radious,2)}\t{round(compactness1,2)}\t{round(compactness2,2)}\t{round(compactness3,2)}\t{round(compactness4,2)}\t{round(compactness5,2)}\t{round(compactness6,2)}\n"
        )
    file.close()


random_polygons(10)

print("end")
