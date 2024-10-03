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

CALCULATE_PARAMETERS = False

#Dataset = "Santarem"
#Dataset = "VSousaPaiva2021"
#Dataset = "VSousaPaiva2021_Q1"
#Dataset = "VSousaPaiva2021_Q2"
#Dataset = "VSousaPaiva2021_Q3"
#Dataset = "VSousaPaiva2021_Q4"

size = 8

#Dataset = "Dataset_1 - 125 Conc"
#Dataset = "Dataset_2 - 96 Conc"
#Dataset = "Dataset_3 - 57 Conc"
#Dataset, size = "Square", 100
#Dataset, size = "Hexagon", 127

#Dataset, size = "Square", 25
Dataset, size = "Hexagon", 25

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
if districts == "multiple":
    Objectives = ["d_singular_SEM_AREA","d_singular_SEM_AREA_RL","d_squared_SEM_AREA","d_squared_SEM_AREA_RL","d_singular","d_singular_RL","d_squared","d_squared_RL","diameter","diameter_RL", "perimeter","perimeter_RL", "perimeter_new", "perimeter_new_RL", "diameter_new", "diameter_new_RL"]
    #Objectives = ["d_singular_SEM_AREA","d_singular_SEM_AREA_RL","d_squared_SEM_AREA","d_squared_SEM_AREA_RL","d_singular","d_singular_RL", "d_singularMax","d_singularMax_RL","d_squared","d_squared_RL", "d_squaredMax","d_squaredMax_RL","diameter","diameter_RL", "diameterMax","diameterMax_RL","perimeter","perimeter_RL", "perimeterMax","perimeterMax_RL"]
elif districts == "singular":
    Objectives = ["d_singular_SEM_AREA","d_singular_SEM_AREA_RL","d_squared_SEM_AREA","d_squared_SEM_AREA_RL","d_singular","d_singular_RL","d_squared","d_squared_RL","diameter","diameter_RL", "perimeter","perimeter_RL", "perimeter_new", "perimeter_new_RL", "diameter_new", "diameter_new_RL"]

Objectives =["perimeter_new", "diameter_new"]

#! FIRST TIME
if CALCULATE_PARAMETERS:
    if QGIS or "VSousaPaiva2021" in Dataset:
        load_real_polygons(xlsx_file, pickle_file, json_file, Dataset)
    else:
        load_deterministic_polygon(size, Dataset, pickle_file, json_file)
else:
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



lambda_1 = 0.15
lambda_2 = 0.20


# Create instance folder
if districts != "singular":
    instance_folder = (
        source_folder
        + "Instance_"
        + Dataset + "_" + str(lambda_1*100) + "_" + str(lambda_2*100)
    )
else:
    instance_folder = (
        source_folder
        + "Instance_"
        + Dataset + "_" + str(lambda_1*100) + "_" + str(lambda_2*100)
    )




objective_function = []
problem_values = []
Areas = []



for objective in Objectives:
    print(f"\n\nFUNÇÃO OBJETIVO : {objective}\n")
    model_folder = instance_folder + "\\" + objective
    #os.makedirs(model_folder)

    # Objective
    source_file = source_folder + objective+".mos"
    mosel_file = model_folder + "\\" + objective+".mos"


    output_model = model_folder + f"\\{objective}_out.txt"
    

    
   
    RL = objective.split("_")[-1]
    if RL == "RL":
        continue   
    
    
    try:
        regions = read_output_model(output_model, center = True)
        
        if Dataset in ["Dataset_1 - 125 Conc", "Dataset_2 - 96 Conc", "Dataset_3 - 57 Conc"]:
            regions_QGIS(regions, Dataset, model_folder)
        else:
            None

        for center in regions.keys():
            print(f"\nThe district centered in the basic unit {center} has also the the basic units      {regions[center]}.")

        # Draws the districts selected in the map
        save_deterministic_solution(regions, polygons, model_folder, Dataset, objective, ID=False)
        save_deterministic_solution(regions, polygons, model_folder, Dataset, objective, ID=True)
    except:
        print("\nSomething went wrong. Please check manually.\n\n\n")