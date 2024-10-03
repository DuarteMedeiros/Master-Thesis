#@Compactness
from math import sqrt
from math import pi
from ReadPolygons import *


def Calculate_Inertia(vertices):
    x_g = 0
    y_g = 0
    A = 0
    I_g = 0

    for i in range(len(vertices)):
        if i == len(vertices)-1:
            j = 0
        else:
            j = i+1

        a_i_T = (vertices[j][0]-vertices[i][0])*(vertices[j][1]-vertices[i][1]) / 2 
        a_i_R = (vertices[j][0]-vertices[i][0])*vertices[i][1]

        x_i_g_T = (vertices[i][0] + 2*vertices[j][0]) / 3
        y_i_g_T = (2*vertices[i][1] + vertices[j][1]) / 3    

        x_i_g_R = (vertices[i][0] + vertices[j][0]) / 2
        y_i_g_R = (vertices[i][1]) / 2

        I_i_T = a_i_T / 18 * ((vertices[j][0] - vertices[i][0])**2 + (vertices[j][1] - vertices[i][1])**2)
        I_i_R = a_i_R / 12 * ((vertices[j][0] - vertices[i][0])**2 + vertices[i][1]**2)

        A += a_i_T + a_i_R

        x_g += x_i_g_R*a_i_R + x_i_g_T*a_i_T
        y_g += y_i_g_R*a_i_R + y_i_g_T*a_i_T

    x_g = x_g / A
    y_g = y_g / A

    #print(f"x = {x_g}, y = {y_g}")

    for i in range(len(vertices)):
        if i == len(vertices)-1:
            j = 0
        else:
            j = i+1

        a_i_T = (vertices[j][0]-vertices[i][0])*(vertices[j][1]-vertices[i][1]) / 2 
        a_i_R = (vertices[j][0]-vertices[i][0])*vertices[i][1]

        x_i_g_T = (vertices[i][0] + 2*vertices[j][0]) / 3
        y_i_g_T = (2*vertices[i][1] + vertices[j][1]) / 3

        x_i_g_R = (vertices[i][0] + vertices[j][0]) / 2
        y_i_g_R = (vertices[i][1]) / 2

        I_i_T = a_i_T / 18 * ((vertices[j][0] - vertices[i][0])**2 + (vertices[j][1] - vertices[i][1])**2)
        I_i_R = a_i_R / 12 * ((vertices[j][0] - vertices[i][0])**2 + vertices[i][1]**2)

        d_i_T_g = (x_i_g_T - x_g)**2 + (y_i_g_T - y_g)**2
        d_i_R_g = (x_i_g_R - x_g)**2 + (y_i_g_R - y_g)**2

        I_g += I_i_T + d_i_T_g*a_i_T + I_i_R +d_i_R_g*a_i_R

    Comp = A**2/(2*3.14*I_g)

    #print(f"I_g = {I_g}")
    #print(f"Compactness = {A**2/(2*pi*I_g)}\n")
    
    return I_g, x_g, y_g, A

def Inertia_Add_Polygon(Inertia_p, Inertia_u):
    
    I_g_p, x_g_p, y_g_p, A_p = Inertia_p
    I_g_u, x_g_u, y_g_u, A_u = Inertia_u
    
    A_p_u = A_p + A_u
    
    x_g_p_u = (A_p*x_g_p + A_u*x_g_u)/A_p_u
    y_g_p_u = (A_p*y_g_p + A_u*y_g_u)/A_p_u
    
    d_2_p_p_u = (x_g_p - x_g_p_u)**2 + (y_g_p - y_g_p_u)**2
    d_2_p_u_u = (x_g_p_u - x_g_u)**2 + (y_g_p_u - y_g_u)**2
    
    I_p_u = I_g_p + I_g_u + A_p*d_2_p_p_u + A_u*d_2_p_u_u
    
    Comp = A_p_u**2/(2*3.14*I_p_u)

    #print(f"I_g = {I_p_u}")
    #print(f"Compactness = {Comp}\n")
    
    return I_p_u, x_g_p_u, y_g_p_u, A_p_u

def Inertia_Remove_Polygon(Inertia_p, Inertia_u):
    
    I_g_p, x_g_p, y_g_p, A_p = Inertia_p
    I_g_u, x_g_u, y_g_u, A_u = Inertia_u
    
    A_p_u = A_p - A_u
    
    x_g_p_u = (A_p * x_g_p - A_u * x_g_u)/A_p_u
    y_g_p_u = (A_p * y_g_p - A_u * y_g_u)/A_p_u
    
    d_2_p_u_p = (x_g_p_u - x_g_p)**2 + (y_g_p_u - y_g_p)**2
    d_2_u_p = (x_g_u - x_g_p)**2 + (y_g_u - y_g_p)**2
    
    I_p_u = I_g_p - I_g_u - A_p_u * d_2_p_u_p - A_u * d_2_u_p
    
    Comp = A_p_u**2/(2*3.14*I_p_u)

    print(f"I_g = {I_p_u}")
    print(f"Compactness = {Comp}\n")
    
    return I_p_u, x_g_p_u, y_g_p_u, A_p_u


size = 1

Dataset = "Dataset_1 - 125 Conc"
Dataset = "Dataset_2 - 96 Conc"
Dataset = "Dataset_3 - 57 Conc"
Dataset, size = "Square", 100
Dataset, size = "Hexagon", 127


#districts = "singular"
districts = "multiple"

lambda_1 = 0.15
lambda_2 = 0.20

INDIVIDUAL_MI = False
MULTIPLE_MI = True

Objectives = ["d_singular_SEM_AREA","d_squared_SEM_AREA", "d_singular", "d_squared", "diameter_new","perimeter_new"]
#Objectives = ["perimeter_new"]

if Dataset == "Square" or Dataset == "Hexagon":
    pickle_file = r"Auxiliary_Files\\" + Dataset + "_" + str(size) + "_Map.pkl"
    json_file = r"Auxiliary_Files\\" + Dataset + "_" + str(size) + "_Parameters.json"
else:
    pickle_file = r"Auxiliary_Files\\" + Dataset + "_Map.pkl"
    json_file = r"Auxiliary_Files\\" + Dataset + "_Parameters.json"
main_folder = r"C:\Users\ADMIN\OneDrive - Universidade de Lisboa\Documents\Faculdade\Mestrado\Estatística e Investigação Operacional\2º ano\Dissertação"
#print(f"Main Folder = {os.path.exists(main_folder)}")
#print(f"{main_folder}\n\n")


if districts == "singular":
    n_districts = 1
    source_folder = main_folder + "\\Modelos\\" + "Mod1_Singular\\"
elif districts == "multiple":
    n_districts = random.randint(2, 4)
    source_folder = main_folder + "\Modelos\\" + "Mod1_Multiple\\"

#print(f"Source Folder = {os.path.exists(source_folder)}")
#print(f"{source_folder}\n\n")

instance_folder = source_folder + "Instance_" + Dataset + "_" + str(lambda_1*100) + "_" + str(lambda_2*100)
#print(f"Instance Folder = {os.path.exists(instance_folder)}")
#print(f"{instance_folder}\n\n")

polygons = import_polygons(pickle_file)

if INDIVIDUAL_MI:

    MI = [0 for i in range(len(polygons))]

    for polygon in polygons:
        vertices = polygon.get_points()
        id = polygon.get_id()
        MI[id-1] = Calculate_Inertia(vertices)
        #print(f"id = {polygon.get_id()}")
        #Calculate_Inertia(vertices)

    file = open(r"Auxiliary_Files\\"+Dataset+"_MI.json", "w")
    json.dump(MI, file)
    file.close()



if MULTIPLE_MI:
    file = open(f"{Dataset}_{districts}_Compactness_MI.txt", "w")
    file.write(f"Instance: {Dataset}\n\n\n")
    for objective in Objectives:
        print(f"\n\nFUNÇÃO OBJETIVO : {objective}\n")
        model_folder = instance_folder + "\\" + objective
        output_model = model_folder + f"\\{objective}_out.txt"
        try:
            if objective in ["perimeter_new", "diameter_new"] and districts == "singular"   :
                regions = read_output_model(output_model, False)
            else:
                regions = read_output_model(output_model)
        except:
            continue
        #print(regions)
        
        Compactness_by_District = {}
        
        for i in range(len(regions)):
            region = list(regions.values())[i]
            center = list(regions.keys())[i]
            #print(region)
            #print(center)
            
            #Square Vertices[::-1]
            #Hexagon Vertices[::-1]
            
            initial_id = region[0]
            #print(f"\n\ninitial id = {initial_id}")
            initial_polygon = get_polygon_by_id(polygons, initial_id)
            #print(f"initial polygon = {initial_polygon.get_points()[::-1]}")
            if Dataset in ["Square", "Hexagon"]:
                current_inertia = Calculate_Inertia(initial_polygon.get_points()[::-1])
            else:
                current_inertia = Calculate_Inertia(initial_polygon.get_points())
            #print(f"initial inertia = {current_inertia}\n\n")
            for id in region[1:]:
                polygon = get_polygon_by_id(polygons, id)
                #print(f"\n\nid = {id}")
                if Dataset in ["Square", "Hexagon"]:
                    polygon_inertia = Calculate_Inertia(polygon.get_points()[::-1])
                else:
                    polygon_inertia = Calculate_Inertia(polygon.get_points())
                #print(f"polygon = {polygon.get_points()[::-1]}")
                current_inertia = Inertia_Add_Polygon(current_inertia, polygon_inertia)
                #print(f"joined inertia = {current_inertia}\n\n")
            I_p_u, x_g_p_u, y_g_p_u, A_p_u = current_inertia
            Comp = round(A_p_u**2/(2*pi*I_p_u), 2)
            Compactness_by_District[center] = Comp
        
        print(Compactness_by_District)
        
        file.write(f"Obective Function: {objective}\n")
        file.write(f"Center\tCompactness\n")
        for i in range(len(Compactness_by_District)):
            file.write(f"   {list(Compactness_by_District.keys())[i]}       {list(Compactness_by_District.values())[i]}\n")
        file.write("\n\n")
    file.close()
        
        