import pandas as pd
from Polygon import myPolygon
import pickle
import json
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MatplotlibPolygon
import matplotlib.colors as mcolors
import random
import os
import sys
import statistics
import numpy as np

def import_polygons_xlsx(file_path, Dataset):
    """import the polygons defined in a xlsx file, where the first column is a primary jey of the polygon and the second and third column are the coordinates of each vertices

    Args:
        file_path (str): path of the xlsx file

    Returns:
        list: list of polygons created with the class myPolygon
    """
    # Read the Excel file into a DataFrame.
    df = pd.read_excel(file_path)

    # Initialize an empty dictionary to store the polygon data.
    polygon_dict = {}
    polygons = []
    polygon_name = ""

    # Iterate through the DataFrame and populate the dictionary.
    for row in df.itertuples(index=False):
        coordinates = (
            row[1],
            row[2],
        )  # Assuming the coordinates are in the second and third columns.
        polygon_name = row[0]

        if polygon_name in polygon_dict.keys():
            polygon_dict[polygon_name].append(coordinates)
        else:
            polygon_dict[polygon_name] = [coordinates]

    id = 0
    # for each list of vertices create the object Polygon
    for name in polygon_dict.keys():
        polygon = myPolygon()
        id += 1
        for vertex in polygon_dict[name]:
            polygon.real_add_point(vertex)

        polygon.set_id(id)
        polygon.set_name(name)
        polygons.append(polygon)
        print(f"{polygon.get_name()}_{polygon.get_id()}.png")
        polygon.save_polygon(Dataset)
    return polygons


def export_polygons(polygons, name):
    """Given a list of objects of the class myPolygon export the objects to a pickle file

    Args:
        polygons (list): list of polygons created with the class myPolygon
        name (str): path of the pickle file
    """
    # writes the objects in the file
    with open(name, "wb") as file:
        pickle.dump(polygons, file)
    print(f"Objects saved with success.\n\n")


def import_polygons(name):
    """Given a pickle file import the polygons at the file

    Args:
        name (str): path of the pickle file

    Returns:
        list: list of polygons created with the class myPolygon
    """
    # read the pickle file
    with open(name, "rb") as file:
        polygons = pickle.load(file)
    print(f"Objects loaded with success.\n\n")
    return polygons


def get_polygon_by_id(polygons, id):
    """Given a list of polygons and an id, returns the polygon with that id

    Args:
        polygons (list): list of polygons created with the class myPolygon
        id (int): the id of a polygon

    Returns:
        myPolygon: the polygon with that id
    """
    # the id of a polygon should be a primary key of the polygon, so there are no two polygons with the same id
    for polygon in polygons:
        # if the id of the polygon is the id stop the loop and return the polygon
        if polygon.get_id() == id:
            return polygon
    print(f"No polygon with id = {id}.\n\n")


def calculate_distance(polygons):
    """Given a list of polygons creates the distance matrix for every two polygons

    Args:
        polygons (list): list of polygons created with the class myPolygon

    Returns:
        list: a list of lits representing the distance matrix of every two polygons
    """
    # the matrix has sie n*n
    n = len(polygons)
    # creates a matrix of the size n*n with only 0 values
    M = [[0 for _ in range(n)] for _ in range(n)]

    # iterates for every two polygons, sorted by id. Notice that the distance is a reflexive relationship
    for id1 in range(1, n + 1):
        polygon1 = get_polygon_by_id(polygons, id1)
        center1 = polygon1.get_center()

        for id2 in range(id1, n + 1):
            polygon2 = get_polygon_by_id(polygons, id2)
            center2 = polygon2.get_center()

            # computes the distance
            delta_x = (center1[0] - center2[0]) ** 2
            delta_y = (center1[1] - center2[1]) ** 2
            distance = (delta_x + delta_y) ** 0.5

            # assign the position on the matrix to the value
            # the matrix should be simetric
            M[id1 - 1][id2 - 1] = round(distance, 2)
            M[id2 - 1][id1 - 1] = round(distance, 2)

    return M


def calculate_common_perimeter(polygons):
    """Given a list polygons calculates the common perimeter of every two polygons

    Args:
        polygons (list): list of polygons created with the class myPolygon

    Returns:
        list: list of lists representing the matrix of common perimeter of every two polygons
    """
    # print(f"This function may take a while.")

    # the matrix has size n*n
    n = len(polygons)

    # creates a matrix n*n with 0 for every value
    M = [[0 for _ in range(n)] for _ in range(n)]

    neighbors = polygons_neighbors(polygons)

    # iterates for every two polygons, sorted by id. Notice that the distance is a reflexive relationship
    for polygon1 in polygons:
        id1 = polygon1.get_id()
        adjacent_polygons = neighbors[polygon1]
        for polygon2 in adjacent_polygons:
            id2 = polygon2.get_id()
            common_perimeter = 0
            if id1 <= id2:
                print(
                   f"Computing the common perimeter of the polygons with id {id1} and {id2}."
                )

                if id1 == id2:
                    # if the polygons are the same the common perimeter is equal to the perimeter
                    common_perimeter = polygon1.get_perimeter()
                else:
                    common_perimeter = polygon1.get_common_perimeter(polygon2)

                # assign the position on the matrix to the value
                # the matrix should be simetric
                M[id1 - 1][id2 - 1] = round(common_perimeter, 2)
                M[id2 - 1][id1 - 1] = round(common_perimeter, 2)
            else:
                continue

    return M


def calculate_area(polygons):
    """Given a list of polygons computes the area of each polygon, returns a matrix with the area of each polygon

    Args:
        polygons (list): list of polygons created with the class myPolygon

    Returns:
        list: a list corresponding to a n*1 matrix of the area of each polygon
    """
    # the matrix has size n*1
    n = len(polygons)
    # creates a empty list
    M = []

    # iterates for every polygon by ascending order of id
    for id1 in range(1, n + 1):
        polygon1 = get_polygon_by_id(polygons, id1)
        # rounds the area to 2 decimal cases
        area = round(polygon1.get_area(), 2)
        # adds the area to the matrix
        M.append(area)
    # print(M)
    return M


def calculate_perimeter(polygons):
    """Given a list of polygons computes the perimeter of each polygon, returns a matrix with the area of each polygon

    Args:
        polygons (list): list of polygons created with the class myPolygon

    Returns:
        list: a list corresponding to a n*1 matrix of the perimeter of each polygon
    """
    # the matrix has size n*1
    n = len(polygons)
    # creates a empty list
    M = []

    # iterates for every polygon by ascending order of id
    for id1 in range(1, n + 1):
        polygon1 = get_polygon_by_id(polygons, id1)
        # rounds the area to 2 decimal cases
        perimeter = round(polygon1.get_perimeter(), 2)
        # adds the area to the matrix
        M.append(perimeter)

    return M


def write_data(
    number_units,
    Distance,
    CPerimeter,
    MDistance,
    Area,
    Perimeter,
    n,
    m,
    min_area,
    max_area,
    name,
    QGIS=True,
):
    """Writes the parameters calculated in a .dat file for the Xpress IVE

    Args:
        number_units (int): number of polygons
        Distance (list): the distance between every two polygons
        CPerimeter (list): the common perimeter of every two polygons
        Area (list): the area of every polygon
        Perimeter (list): the perimeter of every polygon
        name (str): name of the file where the data should be written
    """
    # creates the file
    file = open(name, "w")
    
    # NUMBER OF UNITS
    file.write(f"N_UNITS : {number_units}\n\n")

    # N
    file.write(f"N : {n}\n\n")

    # M
    file.write(f"M : {m}\n\n")

    # MIN AREA
    file.write(f"MIN_AREA : {min_area}\n\n")

    # MAX AREA
    file.write(f"MAX_AREA : {max_area}\n\n")

    # DISTANCE MATRIX
    file.write(f"DISTANCE : [")
    for line in Distance:
        for value in line:
            if QGIS:
                file.write(f"\t{round(value/1000)}")
            else:
                file.write(f"\t{value}")
        file.write(f"\n\t\t\t")
    file.write(f"]\n\n")
    print(f"Saved DISTANCE MATRIX successfully.")

    # DISTANCE MATRIX
    #file.write(f"DISTANCE : [")
    #for i in range(len(Distance)):
    #    for j in range(len(Distance[i])):
    #        value = Distance[i][j]
    #        if value != 0 and j >= i:
    #            file.write(f"\t({i+1} {j+1})")
    #            if QGIS:
    #                file.write(f" {round(value/1000)}\t")
    #            else:
    #                file.write(f" {value}\t")
    #    file.write(f"\n")
    #file.write(f"]\n\n")

    # COMMON PERIMETER MATRIX
    #file.write(f"CPERIMETER : [")
    #for line in CPerimeter:
    #    for value in line:
    #        if QGIS:
    #            file.write(f"\t{round(value/1000)}")
    #        else:
    #            file.write(f"\t{value}")
    #    file.write(f"\n\t\t\t")
    #file.write(f"]\n\n")
    #print(f"Saved COMMON PERIMETER MATRIX successfully.")

    # COMMON PERIMETER MATRIX
    file.write(f"CPERIMETER : [")
    for i in range(len(CPerimeter)):
        for j in range(len(CPerimeter[0])):
            value = CPerimeter[i][j]
            if value != 0 and j >= i:
                file.write(f"\t({i+1} {j+1})")
                if QGIS:
                    file.write(f" {round(value/1000)}\t")
                else:
                    file.write(f" {value}\t")
        file.write(f"\n")
    file.write(f"]\n\n")
    print(f"Saved COMMON PERIMETER MATRIX successfully.")

    # MAX DISTCANCE MATRIX
    #file.write(f"MDISTANCE : [")
    #for line in MDistance:
    #    for value in line:
    #        if QGIS:
    #            file.write(f"\t{round(value/1000)}")
    #        else:
    #            file.write(f"\t{value}")
    #    file.write(f"\n\t\t\t")
    #file.write(f"]\n\n")
    #print(f"Saved MAX DISTANCE MATRIX successfully.")

    # MAX DISTCANCE MATRIX
    file.write(f"MDISTANCE : [")
    for i in range(len(MDistance)):
        for j in range(len(MDistance[i])):
            value = MDistance[i][j]
            if value != 0 and j >= i:
                file.write(f"\t({i+1} {j+1})")
                if QGIS:
                    file.write(f" {round(value/1000)}\t")
                else:
                    file.write(f" {value}\t")
        file.write(f"\n")
    file.write(f"]\n\n")

    # AREA MATRIX
    file.write(f"AREA : [")
    for value in Area:
        if QGIS:
            file.write(f"\t{round(value/1000000)}")
        else:
            file.write(f"\t{value}")
    file.write(f"\t]\n\n")
    print(f"Saved AREA MATRIX successfully.")

    # PERIMETER MATRIX
    file.write(f"PERIMETER : [")
    for value in Perimeter:
        if QGIS:
            file.write(f"\t{round(value/1000)}")
        else:
            file.write(f"\t{value}")

    file.write(f"\t]\n\n")
    print(f"Saved PERIMETER MATRIX successfully.")

    # Close and save the file
    file.close()


def export_variables(
    number_units, Distance, CPerimeter, MDistance, Area, Perimeter, name
):
    """Export the matrices Distance, CPerimeter, Area, Perimeter to a json file, so we may not compute them again

    Args:
        Distance (list): the distance between every two polygons
        CPerimeter (list): the common perimeter of every two polygons
        Area (list): the area of every polygon
        Perimeter (list): the perimeter of every polygon
        name (str): name of the file where the data should be written
    """
    # creates a dictionary where the keys are variables names and the values are the values of the variables
    my_variables = {}
    my_variables["number_units"] = number_units
    my_variables["Distance"] = Distance
    my_variables["CPerimeter"] = CPerimeter
    my_variables["MDistance"] = MDistance
    my_variables["Area"] = Area
    my_variables["Perimeter"] = Perimeter

    # Dump the dictionary into the json file
    with open(name, "w") as json_file:
        json.dump(my_variables, json_file)


def import_variables(name):
    """Imports the matrices Distance, CPerimeter, Area, Perimeter to a json file.

    Args:
        name (str): name of the file where the data is written

    Returns:
        tuple: the Distance matrix, the CPerimeter MAtrix, the Area Matrix an Perimeter Matrix
    """
    # loads the dictionary from the json file
    with open(name, "r") as json_file:
        my_variables = json.load(json_file)

    # assigns the values to each variable
    number_units = my_variables["number_units"]
    Distance = my_variables["Distance"]
    CPerimeter = my_variables["CPerimeter"]
    MDistance = my_variables["MDistance"]
    Area = my_variables["Area"]
    Perimeter = my_variables["Perimeter"]

    return number_units, Distance, CPerimeter, MDistance, Area, Perimeter


def read_output_model(name, center = True):
    """Given a list of polygons and a path to the output file of a Xpress IVE model, writes the set of polygons, the names and the ids, that identify each region

    Args:
        polygons (list): list of polygons created with the class myPolygon
        name (_type_): path of the output file of the Xpress IVE
    """
    # open file
    file = open(name, "r")

    # identify each region
    regions = {}

    # iterate over the lines of the file
    for line in file.readlines():
        list_line = line[:-1].split(" ")

        # if the line starts with the decision variable x
        if list_line[0] == "x(":
            
            if center:
                # identify the center of the region
                center = list_line[1]
                # identify one basic unit of the region
                unit_selected = list_line[3]
            else:
                center = 0
                unit_selected = list_line[1]

            # This is for the qgz map
            # if QGIS:
            #    polygon_name = polygon.get_name()
            # else:
            #    polygon_name = int(unit_selected)

            polygon_name = int(unit_selected)

            # if the center is a new center
            if center not in regions.keys():
                # if so, start the region with that unit
                regions[center] = [polygon_name]
            else:
                # if not append the unit id to the region
                regions[center].append(polygon_name)

    # close the file
    file.close()

    return regions


def get_stats_problem(name):
    """given a path to a txt file gets the state of the problem
    Args:
        polygons (list): list of polygons created with the class myPolygon
        name (_type_): path of the output file of the Xpress IVE
    """
    # open file
    file = open(name, "r")

    # iterate over the lines of the file
    lines = file.readlines()
    state = lines[0][:-1].split(" ")[-1]
    value = lines[3][:-1].split(" ")[-1]
    time = lines[4][:-1].split(" ")[-1]
    return state, value, time


def get_areas_problem(name):
    # open file
    file = open(name, "r")

    Areas = []

    for line in file.readlines():
        list_line = line[:-1].split(" ")

        if list_line[0] == "The":
            area = float(list_line[-1][0])
            #print(f"Area = {area}")
            Areas.append(area)
    return statistics.mean(Areas)


def save_real_solutions(regions, qgz_path, output_png, dataset, objective):
    number_region = 0
    for conselhos_to_keep in regions.values():
        # print(conselhos_to_keep)
        number_region += 1
        see_solution(
            conselhos_to_keep, number_region, qgz_path, output_png, dataset, objective
        )


def see_solution(
    conselhos_to_keep, number_region, qgz_path, main_folder, dataset, objective
):
    # Load the QGZ map data
    gdf = gpd.read_file(qgz_path)

    # Filter the data
    filtered_gdf = gdf[gdf["Concelho"].isin(conselhos_to_keep)]
    # Create a map plot
    filtered_gdf.plot()
    # plt.title("Solution")
    plt.axis("off")
    # Save the map as a PNG file
    output_png = (
        main_folder
        + "\\"
        + str(dataset)
        + "_"
        + str(objective)
        + "_Region_"
        + str(number_region)
        + ".png"
    )
    plt.savefig(output_png)

    # Optionally, export the filtered data as a shapefile
    filtered_gdf.to_file(main_folder + "\Region_" + str(number_region) + ".qgz")

    # Display the map plot (optional)
    # plt.show()
    plt.close("all")

    print(f"Map saved with success.\n\n\n")


def calculate_max_distance(polygons):
    # the matrix has size n*n
    n = len(polygons)

    # creates a matrix n*n with 0 for every value
    M = [[0 for _ in range(n)] for _ in range(n)]

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
                            else:
                                continue
                        else:
                            continue
            else:
                continue

    return M


def distance(v1, v2):
    x1, y1 = v1
    x2, y2 = v2
    delta_x = (x2 - x1) ** 2
    delta_y = (y2 - y1) ** 2
    distance = (delta_x + delta_y) ** 0.5
    return distance


def save_deterministic_solution(
    regions,
    polygons,
    model_folder,
    dataset,
    objective, ID = True
):
    # Get a list of all Matplotlib supported colors
    supported_colors = list(mcolors.CSS4_COLORS)

    random.seed(86128)

    # generate a list with random colours
    random_colors = random.sample(supported_colors, len(regions))

    # make sure whtie or black are not picked
    while "white" in random_colors or "black" in random_colors:
        random_colors = random.sample(supported_colors, len(regions))

    fig, ax = plt.subplots()

    # draws the polygons according to the regions selected
    for polygon in polygons:
        id = polygon.get_id()

        # if it was already added to the graph
        condicao = False

        # verify if the polygon is not in any region
        # if so, draws with a color selected randomly
        # else,the backgound is white
        for index in range(len(regions.values())):
            # each region of the solution
            region = list(regions.values())[index]

            # if the id of the polygon is in region adds the polygon with a specific colour
            if id in region:
                poly = MatplotlibPolygon(
                    polygon.get_points(),
                    edgecolor="black",
                    facecolor=random_colors[index],
                )
                ax.add_patch(poly)

                if ID:
                    # adds the id to the center of the polygon
                    center_x, center_y = polygon.get_center()
                    ax.text(
                        center_x, center_y, str(id), ha="center", va="center", fontsize=12)
                condicao = True
            else:
                continue

        if not condicao: #Se ID desenha apenas o distrito
            poly = MatplotlibPolygon(
                polygon.get_points(), edgecolor="black", facecolor="white"
            )
            ax.add_patch(poly)

            # adds the id to the center of the polygon
            if ID:
                center_x, center_y = polygon.get_center()
                ax.text(center_x, center_y, str(id), ha="center", va="center", fontsize=12)
            else:
                continue

    # Automatically adjust the axis limits
    ax.autoscale()

    # Set equal aspect ratio to make squares appear as squares
    ax.set_aspect("equal")

    # Remove the axis
    ax.axis("off")

    if ID == False:
        filename = (
            model_folder + "\Solution_" + str(dataset) + "_" + str(objective) + ".png"
        )
    else:
         filename = (
            model_folder + "\Solution_" + str(dataset) + "_" + str(objective) + "_ID.png"
        )

    # Save the image as a PNG file
    plt.savefig(filename, dpi=300, bbox_inches="tight")


def polygons_neighbors(polygons):
    adjacent_polygons = {}

    # Iterate through the polygons and check for adjacency
    for polygon1 in polygons:
        adjacent_polygons[polygon1] = [polygon1]
        for polygon2 in polygons:
            if polygon1 != polygon2:  # Avoid self-comparison
                common_points = set(polygon1.points) & set(polygon2.points)
                if common_points:
                    adjacent_polygons[polygon1].append(polygon2)
    return adjacent_polygons


def draw_map(polygons, filename="polygon_map.png", write_id=True):
    fig, ax = plt.subplots()

    for polygon in polygons:
        poly = MatplotlibPolygon(
            polygon.get_points(),
            edgecolor="black",
            facecolor="white",
        )

        ax.add_patch(poly)

        if write_id:
            center_x, center_y = polygon.get_center()
            id = polygon.get_id()
            ax.text(center_x, center_y, str(id), ha="center", va="center", fontsize=12)

    # Automatically adjust the axis limits
    ax.autoscale()

    # Set equal aspect ratio to make squares appear as squares
    ax.set_aspect("equal")

    # Remove the axis
    ax.axis("off")

    # Save the image as a PNG file
    plt.savefig(filename, dpi=300, bbox_inches="tight")

    # Show the plygon
    #plt.show()


def hexagoned_map(number):
    """Fpr each center of a hexagon, calculates the centers of all the hexagons with border intersection, until the input of hexagons is reached. Finally calculates the vertices of every hexagon.

    Args:
        number (_type_): _description_

    Returns:
        _type_: _description_
    """
    ids = [1]
    polygons = []

    centers = [(1, round(1.7320508 / 2, 7))]
    deltas = [(3/2, np.sqrt(3)/2), (3/2, -np.sqrt(3)/2), (0, -np.sqrt(3)), (-3/2, -np.sqrt(3)/2), (-3/2, np.sqrt(3)/2), (0, np.sqrt(3))]
    while len(centers) < number:
        new_centers = []
        for center in centers:
            for delta in deltas:
                new_center = (round(center[0] + delta[0], 7), round(center[1] + delta[1], 7))
                if new_center not in centers and new_center not in new_centers:
                    new_centers.append(new_center)
                    ids.append(ids[-1] + 1)
        centers.extend(new_centers)
            

    i = 0
    for x, y in centers:
        polygon = myPolygon()
        polygon.add_point((x + 1, round(y, 7)))
        polygon.add_point((x + 1 / 2, round(y + np.sqrt(3)/2, 7)))
        polygon.add_point((x - 1 / 2, round(y + np.sqrt(3)/2, 7)))
        polygon.add_point((x - 1, round(y, 7)))
        polygon.add_point((x - 1 / 2, round(y - np.sqrt(3)/2, 7)))
        polygon.add_point((x + 1 / 2, round(y - np.sqrt(3)/2, 7)))
        polygons.append(polygon)
        polygon.set_id(ids[i])
        i += 1
        # polygon.get_points()

    # List of objects of the class Polygon
    return polygons


def squared_map(number):
    ids = [1]
    polygons = []
    centers = [(0, 0)]
    while len(centers) < number:
        for x, y in centers:
            if (x + 1, y) not in centers and len(centers) < number:
                centers.append((x + 1, y))
                ids.append(ids[-1] + 1)
            if (x + 1, y + 1) not in centers and len(centers) < number:
                centers.append((x + 1, y + 1))
                ids.append(ids[-1] + 1)
            if (x, y + 1) not in centers and len(centers) < number:
                centers.append((x, y + 1))
                ids.append(ids[-1] + 1)

    i = 0
    for x, y in centers:
        polygon = myPolygon()
        polygon.add_point((x, y))
        polygon.add_point((x + 1, y))
        polygon.add_point((x + 1, y + 1))
        polygon.add_point((x, y + 1))
        polygons.append(polygon)
        # polygon.get_points()
        polygon.set_id(ids[i])
        i += 1

    # List of objects of the class Polygon
    return polygons


def split_points(polygons):
    max_x = -float("inf")
    min_x = float("inf")
    max_y = -float("inf")
    min_y = float("inf")
    for polygon in polygons:
        for vertex in polygon.get_points():
            x, y = vertex
            if x < min_x:
                min_x = x
            elif x > max_x:
                max_x = x
            if y < min_y:
                min_y = y
            elif y > max_y:
                max_y = y

    limite_y = round((max_y + min_y) / 2, 0)
    limite_x = round((max_x + min_x) / 2, 0)

    # print(f"x = {limite_x}  y = {limite_y}")

    return limite_x, limite_y


def split_polygons(polygons):
    x, y = split_points(polygons)

    regiao_1 = []
    regioes_2_3_4 = []
    for polygon in polygons:
        condicao = True
        for vertex in polygon.get_points():
            vx, vy = vertex
            if not (vx <= x) and not (vy <= y):
                regiao_1.append(polygon)
                condicao = False
                break
        if condicao:
            regioes_2_3_4.append(polygon)

    regiao_3 = []
    regioes_2_4 = []
    for polygon in regioes_2_3_4:
        condicao = True
        for vertex in polygon.get_points():
            vx, vy = vertex
            if vx <= x and vy <= y:
                regiao_3.append(polygon)
                condicao = False
                break
        if condicao:
            regioes_2_4.append(polygon)

    regiao_2 = []
    regiao_4 = []
    for polygon in regioes_2_4:
        condicao = True
        for vertex in polygon.get_points():
            vx, vy = vertex
            if not (vx <= x) and vy <= y:
                regiao_4.append(polygon)
                condicao = False
                break
        if condicao:
            regiao_2.append(polygon)

    id = 1
    for polygon in regiao_1:
        polygon.set_id(id)
        id += 1

    id = 1
    for polygon in regiao_2:
        polygon.set_id(id)
        id += 1

    id = 1
    for polygon in regiao_3:
        polygon.set_id(id)
        id += 1

    id = 1
    for polygon in regiao_4:
        polygon.set_id(id)
        id += 1

    return regiao_1, regiao_2, regiao_3, regiao_4


def split_dataset(Dataset, polygons, method2=True):
    """Given a big dataset splits it in 4, in 2 two different ways, the user can choose.

    Args:
        Dataset (str): the dataset of the polygons
        polygons (list): list of objects of the class MyPolygon
        aleatorio (bool, optional): If the 4-split is random or not. Defaults to True.
    """
    if not (method2):
        regiao_1, regiao_2, regiao_3, regiao_4 = split_polygons(polygons)
        tipo = "M1"  # Not Random
    else:
        regiao_1, regiao_2, regiao_3, regiao_4 = split_polygons_2(polygons)
        tipo = "M2"  # Random

    # The 4 splits
    Quadrantes = [regiao_1, regiao_2, regiao_3, regiao_4]

    # for each split
    for k in range(len(Quadrantes)):
        # the polygons are th epolygons in that split
        polygons = Quadrantes[k]

        # File of the polygons
        pickle_file = r"Auxiliary_Files\\" + f"{Dataset}_Q{k+1}{tipo}" + "_Map.pkl"
        # File of the parameters
        json_file = (
            r"Auxiliary_Files\\" + f"{Dataset}_Q{k+1}{tipo}" + "_Parameters.json"
        )

        # Export the polygons to a .pkl file
        export_polygons(polygons, pickle_file)

        # Number of polygons
        number_units = len(polygons)

        # Compute the parameters needed
        Distance = calculate_distance(polygons)
        CPerimeter = calculate_common_perimeter(polygons)
        MDistance = calculate_max_distance(polygons)
        Area = calculate_area(polygons)
        Perimeter = calculate_perimeter(polygons)

        # Export variables to a json, so it's no necessary to run the functions every time
        export_variables(
            number_units, Distance, CPerimeter, MDistance, Area, Perimeter, json_file
        )

    # Leave the script
    sys.exit()


def load_real_polygons(xlsx_file, pickle_file, json_file, Dataset):
    """Creates a map polygons from a xlsx file

    Args:
        size (int): number of polygons
        Dataset (str): name of the dataset
        pickle_file (path): path to the file where polygons are saved
        json_file (path): path to the file where the parameters are saved
    """
    ## Read the Vertices
    polygons = import_polygons_xlsx(xlsx_file, Dataset)
    
    # Export the polygons to a .pkl file
    export_polygons(polygons, pickle_file)

    # Number of polygons
    number_units = len(polygons)
    
    # Compute the parameters needed
    Distance = calculate_distance(polygons)
    CPerimeter = calculate_common_perimeter(polygons)
    
    MDistance = ""
    Area = ""
    Perimeter = ""
    export_variables(
        number_units, Distance, CPerimeter, MDistance, Area, Perimeter, json_file
    )
    
    MDistance = calculate_max_distance(polygons)
    Area = calculate_area(polygons)
    Perimeter = calculate_perimeter(polygons)

    # Export variables to a json, so it's no necessary to run the functions every time
    export_variables(
        number_units, Distance, CPerimeter, MDistance, Area, Perimeter, json_file
    )


def load_deterministic_polygon(size, Dataset, pickle_file, json_file):
    """Creates a map polygons with squares or hexagons of the sixe size.

    Args:
        size (int): number of polygons
        Dataset (str): name of the dataset
        pickle_file (path): path to the file where polygons are saved
        json_file (path): path to the file where the parameters are saved
    """
    if Dataset == "Square":
        polygons = squared_map(size)
        # draw_map(polygons, "Auxiliary_Files\\Squared_Map_" + str(size) + ".png")
    elif Dataset == "Hexagon":
        polygons = hexagoned_map(size)
        # draw_map(polygons, "Auxiliary_Files\\Hexagoned_Map_" + str(size) + ".png")

    # Export the polygons to a .pkl file
    export_polygons(polygons, pickle_file)

    # Number of polygons
    number_units = len(polygons)

    
    # Compute the parameters needed
    Distance = calculate_distance(polygons)
    CPerimeter = calculate_common_perimeter(polygons)
    MDistance = calculate_max_distance(polygons)
    Area = calculate_area(polygons)
    Perimeter = calculate_perimeter(polygons)

    # Export variables to a json, so it's no necessary to run the functions every time
    export_variables(
        number_units, Distance, CPerimeter, MDistance, Area, Perimeter, json_file
    )


def split_polygons_2(polygons):
    """splits the set of polygons in 4  randomly

    Args:
        polygons (list): list of objects of the class MyPolygon

    Returns:
        tuple: the 4 regions with all the polygons in polygons
    """
    # where to divide each region
    x, y = split_points(polygons)

    # regions start as empty lists
    regiao_1 = []
    regiao_2 = []
    regiao_3 = []
    regiao_4 = []

    # For each polygon in polygons
    for polygon in polygons:
        # First vertex
        vx, vy = polygon.get_points()[0]

        # if vertex in each region
        if vx >= x and vy >= y:
            regiao_1.append(polygon)
        elif vx <= x and vy >= y:
            regiao_2.append(polygon)
        elif vx <= x and vy <= y:
            regiao_3.append(polygon)
        elif vx >= x and vy <= y:
            regiao_4.append(polygon)

    # resets the id of each region
    id = 1
    for polygon in regiao_1:
        polygon.set_id(id)
        id += 1

    # resets the id of each region
    id = 1
    for polygon in regiao_2:
        polygon.set_id(id)
        id += 1

    # resets the id of each region
    id = 1
    for polygon in regiao_3:
        polygon.set_id(id)
        id += 1

    # rests the id of esch region
    id = 1
    for polygon in regiao_4:
        polygon.set_id(id)
        id += 1

    return regiao_1, regiao_2, regiao_3, regiao_4


def get_border(polygons):

    n = len(polygons[0].get_points())
    if n == 4:
        tipo = "squared"
    elif n == 6: 
        tipo = "hexagoned"

    adjacent = {}
    
    Edges = []
    for polygon in polygons:
        Edges += polygon.get_edges()
        for point in polygon.get_points():
            try:
                adjacent[point] += 1
            except:
                adjacent[point] = 1
    #print(adjacent)
    
    #print(f"Edges = {Edges}")
    
    fronteira = myPolygon()
    for point in adjacent.keys():
        if tipo == "squared":
            if adjacent[point] <= 3:
                fronteira.add_point(point)
            else:
                continue
        elif tipo == "hexagoned":
            if adjacent[point] <= 2:
                fronteira.add_point(point)
            else:
                continue
    
    #print(fronteira.get_points())
    #print(len(fronteira.get_points()))
    for indice in range(1,len(fronteira.get_points())):
        #print(indice)
        point = fronteira.get_points()[indice]
        edge = [fronteira.get_points()[indice-1], point]
        #print(edge)
        j = indice
        if edge not in Edges:
            while edge not in Edges:
                #print(f"\nEntrei")
                j += 1
                point = fronteira.get_points()[j]
                edge = [fronteira.get_points()[indice-1], point]
                #print(edge)
            fronteira.get_points().pop(j)
            fronteira.get_points().insert(indice, point)
            #print(fronteira.get_points()[indice-2::])
            #print("\n")
        else:
            continue
            
    
    return fronteira


def draw_border(fronteira, filename="border_map.png"):
    fig, ax = plt.subplots()

    poly = MatplotlibPolygon(
        fronteira.get_points(),
        edgecolor="red",
        facecolor="white",
        )

    ax.add_patch(poly)

    # Automatically adjust the axis limits
    ax.autoscale()

    # Set equal aspect ratio to make squares appear as squares
    ax.set_aspect("equal")

    # Remove the axis
    ax.axis("off")

    # Save the image as a PNG file
    plt.savefig(filename, dpi=300, bbox_inches="tight")

    # Show the plygon
    plt.show()


def regions_QGIS(regions, dataset, model_folder):

    local_id_to_portugal_id_file = dataset + "_dic.pkl"
    
    with open("Auxiliary_Files\\" + local_id_to_portugal_id_file, 'rb') as f:
        local_id_to_portugal_id = pickle.load(f)
        
    distritos_txt = open(model_folder + "\\Distritos.txt", "w")
    
    for center in regions.keys():
        distritos_txt.write('"fid" IN (')
        distritos_txt.write(f"'{local_id_to_portugal_id[str(regions[center][0])]}'")
        for id in regions[center][1:]:
            distritos_txt.write(f", '{local_id_to_portugal_id[str(id)]}'")
        distritos_txt.write(")\n\n")
    
    distritos_txt.close()
    
    return None