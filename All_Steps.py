from ReadPolygons import *
import statistics
import pickle
import json
import random
import os
import shutil
import subprocess
import xpress as xp
import time
import sys
from tabulate import tabulate


#Dataset = "Santarem"
#Dataset = "VSousaPaiva2021"
#Dataset = "VSousaPaiva2021_Q1"
#Dataset = "VSousaPaiva2021_Q2"
#Dataset = "VSousaPaiva2021_Q3"
#Dataset = "VSousaPaiva2021_Q4"
#Dataset = "Dataset_1 - 125 Conc"
#Dataset = "Dataset_2 - 96 Conc"  # > 9h
#Dataset = "Dataset_3 - 57 Conc" > 9h
Dataset = "Square"
#Dataset = "Hexagon"

size = 30


#districts = "singular"
districts = "multiple"





if Dataset in ["Square", "Hexagon"]:
    QGIS = False
elif Dataset in [
    "Dataset_1 - 125 Conc",
    "Dataset_2 - 96 Conc",
    "Dataset_3 - 57 Conc",
    "Santarem",
]:
    QGIS = True
elif Dataset in [
    "VSousaPaiva2021",
    "VSousaPaiva2021_Q1",
    "VSousaPaiva2021_Q2",
    "VSousaPaiva2021_Q3",
    "VSousaPaiva2021_Q4",
]:
    QGIS = False

xlsx_file = r"DataSets\\Vertices_" + Dataset + ".xlsx"
if Dataset == "Square" or Dataset == "Hexagon":
    pickle_file = r"Auxiliary_Files\\" + Dataset + "_" + str(size) + "_Map.pkl"
    json_file = r"Auxiliary_Files\\" + Dataset + "_" + str(size) + "_Parameters.json"
else:
    pickle_file = r"Auxiliary_Files\\" + Dataset + "_Map.pkl"
    json_file = r"Auxiliary_Files\\" + Dataset + "_Parameters.json"
main_folder = r"C:\Users\ADMIN\OneDrive - Universidade de Lisboa\Documents\Faculdade\Mestrado\Estatística e Investigação Operacional\2º ano\Dissertação"

# User data
Objectives = ["d_singular","d_singular_RL", "d_singularMax","d_singularMax_RL","d_squared","d_squared_RL", "d_squaredMax","d_squaredMax_RL","diameter","diameter_RL", "diameterMax","diameterMax_RL","perimeter","perimeter_RL", "perimeterMax","perimeterMax_RL"]


#! FIRST TIME
#if QGIS or "VSousaPaiva2021" in Dataset:
#    load_real_polygons(xlsx_file, pickle_file, json_file, Dataset)
#else:
#    load_deterministic_polygon(size, Dataset, pickle_file, json_file)



# Import the polygons from a .pkl file
polygons = import_polygons(pickle_file)


#! SPLIT DATASET
# split_dataset(Dataset, polygons, method2=True)


# Import variables from a json
number_units, Distance, CPerimeter, MDistance, Area, Perimeter = import_variables(
    json_file
)


# !Pick the Model

# number of districts
if districts == "singular":
    n_districts = 1
    source_folder = main_folder + "\Modelos\\" + "Mod1_Singular\\"
elif districts == "multiple":
    n_districts = random.randint(2, 4)
    source_folder = main_folder + "\Modelos\\" + "Mod1_Multiple\\"


# Definição de Parâmetros
max_units = random.randint(4, 10)
min_area_inf = round(sum(Area) / (4 * n_districts))
min_area_sup = round(sum(Area) / (2 * n_districts))
max_area_inf = round(sum(Area) / (2 * n_districts))
max_area_sup = round(sum(Area) / (n_districts))
min_area = random.randint(min_area_inf, min_area_sup)
max_area = random.randint(max_area_inf, max_area_sup)

if QGIS:
    min_area = round(min_area / 1000000)
    max_area = round(max_area / 1000000)

# Create instance folder
if districts != "singular":
    instance_folder = (
        source_folder
        + "Instance_"
        + Dataset
        + "_"
        + str(max_units)
        + "_"
        + str(min_area)
        + "_"
        + str(max_area)
    )
else:
    instance_folder = (
        source_folder
        + "Instance_"
        + Dataset
        + "_"
        + str(min_area)
        + "_"
        + str(max_area)
    )

# Create instance folder
os.makedirs(instance_folder)
#print(f"Instance Folder Created {instance_folder}")

# Create the map pictures and saves it in the instance folder
if QGIS:
    draw_map(polygons, instance_folder + "\\" + Dataset + "_Map.png")
else:
    draw_map(polygons, instance_folder + "\\" + Dataset + "_" + str(size) + "_Map.png")



objective_function = []
problem_values = []
Areas = []



for objective in Objectives:
    print(f"\n\nFUNÇÃO OBJETIVO : {objective}\n")
    model_folder = instance_folder + "\\" + objective
    os.makedirs(model_folder)

    # Objective
    if objective == "d_squared":
        source_file = source_folder + "d_squared.mos"
        mosel_file = model_folder + "\d_squared.mos"
    elif objective == "d_singular":
        source_file = source_folder + "d_singular.mos"
        mosel_file = model_folder + "\d_singular.mos"
    elif objective == "perimeter":
        source_file = source_folder + "perimeter.mos"
        mosel_file = model_folder + "\perimeter.mos"
    elif objective == "diameter":
        source_file = source_folder + "diameter.mos"
        mosel_file = model_folder + "\diameter.mos"
    elif objective == "d_squared_RL":
        source_file = source_folder + "d_squared_RL.mos"
        mosel_file = model_folder + "\d_squared_RL.mos"
    elif objective == "d_singular_RL":
        source_file = source_folder + "d_singular_RL.mos"
        mosel_file = model_folder + "\d_singular_RL.mos"
    elif objective == "perimeter_RL":
        source_file = source_folder + "perimeter_RL.mos"
        mosel_file = model_folder + "\perimeter_RL.mos"
    elif objective == "diameter_RL":
        source_file = source_folder + "diameter_RL.mos"
        mosel_file = model_folder + "\diameter_RL.mos"
    else:
        source_file = source_folder + objective+".mos"
        mosel_file = model_folder + "\\" + objective+".mos"

    # copy mos file
    shutil.copy(source_file, model_folder)
    data_file = model_folder + "\Instance_Data.dat"

    # Write the .dat file
    write_data(
        number_units,
        Distance,
        CPerimeter,
        MDistance,
        Area,
        Perimeter,
        n_districts,
        max_units,
        min_area,
        max_area,
        data_file,
        QGIS,
    )

    # !OPEN THE FILE
    # Replace "XpressIVE.exe" with the actual path to the Xpress IVE executable
    xpress_ive_executable = r"C:\xpressmp\bin\IVE.exe"
    # Launch Xpress IVE and load your .mos file
    try:
        subprocess.run([xpress_ive_executable, mosel_file], check=True)
        print("\nModel executed successfully in Xpress IVE.")
    except subprocess.CalledProcessError:
        print("\nError occurred while executing the model in Xpress IVE.")

    # k = input("Please run the model.")

    # !RUN THE MODEL
    ## Create an Xpress problem object
    # prob = xp.problem()
    #
    ## Load the .mos file (replace with the path to your .mos file)
    # prob.read(file=mosel_file)
    #
    ## Optimization of  the model
    # prob.optimize()

    # Outout file from mosel
    output_model = model_folder + f"\\{objective}_out.txt"


    state, value, run_time = get_stats_problem(output_model)
    
   
    if state == "infeasible":
        value = "-"
        run_time = "-"
    elif state == "unfinished":
        value = value + "*"

    run_time = str(round(float(run_time), 2))

    problem_values.append((value, run_time))
    if len(problem_values) == 2:
        objective_function.append(problem_values)
        problem_values = []

    RL = objective.split("_")[-1]
    if RL == "RL":
        continue
    else:
        avg_area = get_areas_problem(output_model)
        Areas.append([avg_area])
    
    try:
        regions = read_output_model(output_model)

        for center in regions.keys():
            print(f"\nThe district centered in the basic unit {center} has also the the basic units      {regions[center]}.")

        # Draws the districts selected in the map
        save_deterministic_solution(regions, polygons, model_folder, Dataset, objective)
    except:
        print("\nSomething went wrong. Please check manually.\n\n\n")

if Dataset == "Square" or Dataset == "Hexagon":
    file = open(f"Results_Table_{Dataset}_{size}_{districts}.txt", "w", encoding="utf-8")
else:
    file = open(f"Results_Table_{Dataset}_{districts}.txt", "w", encoding="utf-8")
table = tabulate(objective_function, headers = ["IV Time", "LR Time"])
file.write(table)
file.write("\n\n")
table = tabulate(Areas, headers = ["Avg Area"])
file.write(table)
file.close()


    #if QGIS:
    #    try:
    #        regions = read_output_model(output_model)
    #
    #        for center in regions.keys():
    #            print(
    #                f"\nThe district centered in the basic unit {center} has also the the basic units      {regions[center]}."
    #            )
    #
    #        ## Define the QGZ file path
    #        # qgz_path = main_folder + "\QGIS\Santarém.shp"
    #        # save_real_solutions(regions, qgz_path, model_folder, Dataset, objective)
    #
    #        # Draws the districts selected in the map
    #        save_deterministic_solution(
    #            regions, polygons, model_folder, Dataset, objective
    #        )
    #    except:
    #        print("\nSomething went wrong. Please check manually.\n\n\n")
    #else:
    #    try:
    #        regions = read_output_model(polygons, output_model, QGIS)
    #
    #        for center in regions.keys():
    #            print(
    #                f"\nThe district centered in the basic unit {center} has also the the basic units {regions[center]}."
    #            )
    #
    #        # Draws the districts selected in the map
    #        save_deterministic_solution(
    #            regions, polygons, model_folder, Dataset, objective
    #        )
    #    except:
    #        print("\nSomething went wrong. Please check manually.\n\n\n")
