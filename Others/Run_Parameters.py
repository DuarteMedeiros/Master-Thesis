from ReadPolygons import *

Dataset = "Dataset_2 - 96 Conc"

json_file = r"Auxiliary_Files\\" + Dataset + "_Parameters.json"
pickle_file = r"Auxiliary_Files\\" + Dataset + "_Map.pkl"

polygons = import_polygons(pickle_file)


def calculate_max_distance2(polygons, json_file):
    
    number_units, Distance, CPerimeter, M, CC, DD = import_variables(json_file)
    
    n = len(polygons)
    
    # M = [[0 for _ in range(n)] for _ in range(n)]
    
    
    # iterates for every two polygons, sorted by id. Notice that the distance is a reflexive relationship
    for id1 in range(1, n + 1):
        polygon1 = get_polygon_by_id(polygons, id1)

        for id2 in range(id1, n + 1):
            polygon2 = get_polygon_by_id(polygons, id2)

            if id1 <= id2:
                max_distance = 0
                print(
                   f"Computing the max distance of the polygons with id {id1} and {id2}."
                )

                vertices1 = polygon1.get_points()
                vertices2 = polygon2.get_points()
                for i in range(len(vertices1)):
                    v1 = vertices1[i]
                    for j in range(len(vertices2)):
                        v2 = vertices2[j]

                        # We don't need the verify all vertices, since comparing the vertices A and B is the same to compare vertices B and A. Furthermore, the distance between A and A is always 0
                        if i < j:
                            v1_v2_distance = distance(v1, v2)
                            # print(f"The distance betwwen {v1} e {v2} is : {v1_v2_distance} the actual max distance is {max_distance}.")
                            if v1_v2_distance > max_distance:
                                # assign the position on the matrix to the value
                                # the matrix should be simetric
                                max_distance = v1_v2_distance
                                # print(f"That is the max distance.")
                                M[id1 - 1][id2 - 1] = round(v1_v2_distance, 2)
                                M[id2 - 1][id1 - 1] = round(v1_v2_distance, 2)
                                export_variables(number_units, Distance, CPerimeter, M, "Area", "Perimeter", json_file
)
                            else:
                                continue
                        else:
                            continue
            else:
                continue
    return M


#Number of polygons
#number_units = len(polygons)

# Compute the parameters needed
#Distance = calculate_distance(polygons)
# Export variables to a json, so it's no necessary to run the functions every time
#export_variables(
#    number_units, Distance, "CPerimeter", "MDistance", "Area", "Perimeter", json_file
#)

number_units, Distance, CPerimeter, BB, CC, DD = import_variables(json_file)

#CPerimeter = calculate_common_perimeter(polygons)
# Export variables to a json, so it's no necessary to run the functions every time
#export_variables(
#    number_units, Distance, CPerimeter, "MDistance", "Area", "Perimeter", json_file
#)

#number_units, Distance, CPerimeter, AA, BB, CC = import_variables(json_file)


MDistance = calculate_max_distance2(polygons,json_file)
# Export variables to a json, so it's no necessary to run the functions every time
export_variables(
    number_units, Distance, CPerimeter, MDistance, "Area", "Perimeter", json_file
)

number_units, Distance, CPerimeter, MDistance, AA, BB = import_variables(json_file)

Area = calculate_area(polygons)
# Export variables to a json, so it's no necessary to run the functions every time
export_variables(
    number_units, Distance, CPerimeter, MDistance, Area, "Perimeter", json_file
)

number_units, Distance, CPerimeter, MDistance, Area, AA = import_variables(json_file)

Perimeter = calculate_perimeter(polygons)
# Export variables to a json, so it's no necessary to run the functions every time
export_variables(
    number_units, Distance, CPerimeter, MDistance, Area, Perimeter, json_file
)