from ReadPolygons import *
from itertools import combinations
from itertools import product

Dataset = "Hexagon_127"

json_file = r"Auxiliary_Files\\" + Dataset + "_Parameters.json"
pickle_file = r"Auxiliary_Files\\" + Dataset + "_Map.pkl"

polygons = import_polygons(pickle_file)

number_units, Distance, CPerimeter, MaxDistance, Area, Perimeter = import_variables(json_file)


n = len(polygons)
#Distance = [[0 for _ in range(n)] for _ in range(n)]

# iterates for every two polygons, sorted by id. Notice that the distance is a reflexive relationship
#for id1 in range(1, n + 1):
#    polygon1 = get_polygon_by_id(polygons, id1)
#    center1 = polygon1.get_center()
#
#    for id2 in range(id1, n + 1):
#        polygon2 = get_polygon_by_id(polygons, id2)
#        center2 = polygon2.get_center()
#
#        # computes the distance
#        delta_x = (center1[0] - center2[0]) ** 2
#        delta_y = (center1[1] - center2[1]) ** 2
#        distance = (delta_x + delta_y) ** 0.5
#
#        # assign the position on the matrix to the value
#        # the matrix should be simetric
#        Distance[id1 - 1][id2 - 1] = round(distance, 2)
#        Distance[id2 - 1][id1 - 1] = round(distance, 2)

#Area = []
#for id1 in range(1, n + 1):
#        polygon1 = get_polygon_by_id(polygons, id1)
#        # rounds the area to 2 decimal cases
#        area = round(polygon1.get_area(), 2)
#        # adds the area to the matrix
#        Area.append(area)
#    # print(M)
    
#Perimeter = []
#for id1 in range(1, n + 1):
#        polygon1 = get_polygon_by_id(polygons, id1)
#        # rounds the area to 2 decimal cases
#        perimeter = round(polygon1.get_perimeter(), 2)
#        # adds the area to the matrix
#        Perimeter.append(perimeter)
#
#export_variables(number_units, Distance, CPerimeter, MaxDistance, Area, Perimeter, json_file)

# the matrix has size n*n

#number_units, Distance, CPerimeter, M, BB, CC = import_variables(json_file)
# creates a matrix n*n with 0 for every value
Max_Distance = [[0 for _ in range(n)] for _ in range(n)]


# iterates for every two polygons, sorted by id. Notice that the distance is a reflexive relationship
for id1 in range(1,n+1):
    for id2 in range(id1, n+1):
        polygon1 = get_polygon_by_id(polygons, id1)
        polygon2 = get_polygon_by_id(polygons, id2)
        if id1 > -1 or (id1 >= 0 and id2 >= 0):
            max_distance = 0

            vertices1 = polygon1.get_points()
            vertices2 = polygon2.get_points()

            #print(f"Computing the max distance of the polygons with id {id1} and {id2}.")
            for v1 in vertices1:
                for v2 in vertices2:
                    max_distance = max(max_distance, distance(v1, v2))
    
            Max_Distance[id1 - 1][id2 - 1] = round(max_distance, 2)
            Max_Distance[id2 - 1][id1 - 1] = round(max_distance, 2)
            if id1 == 8 and id2 == 10 or id1 == 10 and id2 == 8:
                print(max_distance)
            #print("A guardar ...")
            #export_variables(number_units, Distance, CPerimeter, M, "Area", "Perimeter", json_file)
            #print("Guardado")
        else:
            #print(f"Aborted {id1} and {id2}")
            None

export_variables(number_units, Distance, CPerimeter, Max_Distance, Area, Perimeter, json_file)

#for id1 in range(1, n + 1):
#    print(f"Computing the max distance of the polygon with id {id1} to itself.")
#    polygon = get_polygon_by_id(polygons, id1)
#
#    max_distance = 0
#
#    vertices1 = polygon.get_points()
#    vertices2 = polygon.get_points()
#
#    for v1, v2 in product(vertices1, vertices2):
#        max_distance = max(max_distance, distance(v1, v2))
#
#
#    Max_Distance[id1 - 1][id1 - 1] = round(max_distance, 2)
#    #export_variables(number_units, Distance, CPerimeter, M, "Area", "Perimeter", json_file)
#    print("Guardado")

#for i in Max_Distance:    
#    print(i)