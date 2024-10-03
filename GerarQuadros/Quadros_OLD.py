import pandas as pd

ficheiro = "Resultados Computacionais2.xlsx"


def drawComputationalResults(Objectives, Instances, Opts, Time_Opts, LRs, Time_RLs, Gap_Opts, Gap_LRs):
    
    n = len(Objectives)
        
    file = open(f"{page}_Tables.txt", "w", encoding = "utf-8")
    
    gap_opt_col = True
    
    #gap_opt_col = False
    #for gap_opt in Gap_Opts:
    #    if gap_opt != "0.0":
    #        gap_opt_col = True
    #        break
    #    else:
    #        continue
    
    file.write("\t\\begin{table}[!htp]\n")
    file.write("\t\t\\begin{adjustwidth}{-5cm}{-5cm}\n")
    file.write("\t\t\\caption{Continuous " + page.lower() + " results}\n")
    file.write("\t\t\\label{tab:Continuous_"+ page + "_Results}\n")
    file.write("\t\t\t\\begin{center}\n")
    if gap_opt_col:
        file.write("\t\t\t\t\\begin{tabular}{cc|c|cc|cc|cc}\n")
        file.write("\t\t\t\t\t\\noalign{\smallskip}\n")
        file.write("\t\t\t\t\t\\multicolumn{2}{c|}{\multirow{2}{*}{\centering Instance}} & \multirow{2}{6em}{\centering Ob. Func.} & \multirow{2}{3em}{\centering Opt.} & \multirow{2}{4em}{\centering Time} & \multirow{2}{3em}{\centering LR} & \multirow{2}{3em}{\centering Time} & \multirow{2}{3em}{\centering Linear Gap} & \multirow{2}{3em}{\centering Final Gap} \\\ & & & & & & & &\\\ \n\n")
    else:
        file.write("\t\t\t\t\\begin{tabular}{cc|c|cc|cc|c}\n")
        file.write("\t\t\t\t\t\\noalign{\smallskip}\n")
        file.write("\t\t\t\t\t\\multicolumn{2}{c|}{\multirow{2}{*}{\centering Instance}} & \multirow{2}{6em}{\centering Ob. Func.} & \multirow{2}{3em}{\centering Opt.} & \multirow{2}{4em}{\centering Time} & \multirow{2}{3em}{\centering LR} & \multirow{2}{3em}{\centering Time} & \multirow{2}{3em}{\centering Linear Gap} \\\ & & & & & & &\\\ \n")
    
    
    instancia_anterior = None
    
    for i in range(n):
        
        if Instances[i] == "Dataset_1 - 125 Conc":
            instancia = "North"
            size = "125"
        elif Instances[i] == "Dataset_2 - 96 Conc":
            instancia = "Center"
            size = "96"
        elif Instances[i] == "Dataset_3 - 57 Conc":
            instancia = "South"
            size = "57"
        elif Instances[i] == "Square_100":
            instancia = "Square"
            size = "100"
            continue
        elif Instances[i] == "Hexagon_127":
            instancia = "Hexagon"
            size = "127"
            continue
        else:
            raise("Error, instance not found.")
        
        if Objectives[i] == "Primeiro Momento Ajustado":
            objective = "First Mom. Adj."
        elif Objectives[i] == "Segundo Momento Ajustado":
            objective = "Second Mom. Adj."
        elif Objectives[i] == "Primeiro Momento":
            objective = "First Mom."
        elif Objectives[i] == "Segundo Momento":
            objective = "Second Mom."
        elif Objectives[i] == "Distância Máxima":
            objective = "Diameter"
        elif Objectives[i] == "Perímetro":
            objective = "Perimeter"
        else:
            raise("Error, objective not found.")
        
        if Gap_Opts[i] == "0.0":
            Gap_Opts[i] = "-"
        
        if instancia_anterior != instancia:
            file.write("\n\t\t\t\t\t\\hline\n")
            file.write("\t\t\t\t\t\\multirow{12}{3em}{\centering " + instancia + "} & \multirow{12}{3em}{\centering " + size + "} & \n")
            file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective + "} & \multirow{2}{6em}{\centering " + Opts[i] + "} & \multirow{2}{4em}{\centering " + Time_Opts[i] +"} & \multirow{2}{6em}{\centering " + LRs[i] +"} & \multirow{2}{3em}{\centering " + Time_RLs[i] +"} &  \multirow{2}{6em}{\centering " + Gap_LRs[i] + "} & \multirow{2}{3em}{\centering " + Gap_Opts[i] + "}\\\ & & & & & & & &\\\& &\n")
        else:
            if float(Time_Opts[i]) >= 10000:
                Time_Opts[i] = Time_Opts[i] + "*"
                Opts[i] = Opts[i] + "*"
            else:
                None
                
            if objective == "Perimeter":
                file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective +"} & \multirow{2}{6em}{\centering " + Opts[i] + "} & \multirow{2}{4em}{\centering " + Time_Opts[i] +"} & \multirow{2}{6em}{\centering " + LRs[i] +"} & \multirow{2}{3em}{\centering " + Time_RLs[i] +"} & \multirow{2}{6em}{\centering " + Gap_LRs[i] + "} & \multirow{2}{3em}{\centering " + Gap_Opts[i] + "}\\\ & & & & & & & &\\\ \n")
            else:
                file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective +"} & \multirow{2}{6em}{\centering " + Opts[i] + "} & \multirow{2}{4em}{\centering " + Time_Opts[i] +"} & \multirow{2}{6em}{\centering " + LRs[i] +"} & \multirow{2}{3em}{\centering " + Time_RLs[i] +"} & \multirow{2}{6em}{\centering " + Gap_LRs[i] + "} & \multirow{2}{3em}{\centering " + Gap_Opts[i] + "}\\\ & & & & & & & &\\\& &\n")
        
                
        instancia_anterior = instancia
        
    file.write("\n\t\t\t\t\t\\hline\n")
    file.write("\t\t\t\t\\end{tabular}\n")
    file.write("\t\t\t\\end{center}\n")
    file.write("\t\t\\end{adjustwidth}\n")
    file.write("\t\\end{table}\n\n\n\n\n\n\n\n\n")
    


    #SEGUNDA TABELA


    
    file.write("\t\\begin{table}[!htp]\n")
    file.write("\t\t\\begin{adjustwidth}{-5cm}{-5cm}\n")
    file.write("\t\t\\caption{Discrete " + page.lower() + " results}\n")
    file.write("\t\t\\label{tab:Discrete_" + page + "_Results}\n")
    file.write("\t\t\t\\begin{center}\n")
    if gap_opt_col:
        file.write("\t\t\t\t\\begin{tabular}{cc|c|cc|cc|cc}\n")
        file.write("\t\t\t\t\t\\noalign{\smallskip}\n")
        file.write("\t\t\t\t\t\\multicolumn{2}{c|}{\multirow{2}{*}{\centering Instance}} & \multirow{2}{6em}{\centering Ob. Func.} & \multirow{2}{3em}{\centering Opt.} & \multirow{2}{4em}{\centering Time} & \multirow{2}{3em}{\centering LR} & \multirow{2}{3em}{\centering Time} & \multirow{2}{3em}{\centering Linear Gap} & \multirow{2}{3em}{\centering Final Gap} \\\ & & & & & & & &\\\ \n\n")
    else:
        file.write("\t\t\t\t\\begin{tabular}{cc|c|cc|cc|c}\n")
        file.write("\t\t\t\t\t\\noalign{\smallskip}\n")
        file.write("\t\t\t\t\t\\multicolumn{2}{c|}{\multirow{2}{*}{\centering Instance}} & \multirow{2}{6em}{\centering Ob. Func.} & \multirow{2}{3em}{\centering Opt.} & \multirow{2}{4em}{\centering Time} & \multirow{2}{3em}{\centering LR} & \multirow{2}{3em}{\centering Time} & \multirow{2}{3em}{\centering Linear Gap} \\\ & & & & & & &\\\ \n")
    
    instancia_anterior = None
    
    for i in range(n):
        
        if Instances[i] == "Dataset_1 - 125 Conc":
            instancia = "North"
            size = "125"
            continue
        elif Instances[i] == "Dataset_2 - 96 Conc":
            instancia = "Center"
            size = "96"
            continue
        elif Instances[i] == "Dataset_3 - 57 Conc":
            instancia = "South"
            size = "57"
            continue
        elif Instances[i] == "Square_100":
            instancia = "Square"
            size = "100"
        elif Instances[i] == "Hexagon_127":
            instancia = "Hexagon"
            size = "127"
        else:
            raise("Error, instance not found.")
        
        if Objectives[i] == "Primeiro Momento Ajustado":
            objective = "First Mom. Adj."
        elif Objectives[i] == "Segundo Momento Ajustado":
            objective = "Second Mom. Adj."
        elif Objectives[i] == "Primeiro Momento":
            objective = "First Mom."
        elif Objectives[i] == "Segundo Momento":
            objective = "Second Mom."
        elif Objectives[i] == "Distância Máxima":
            objective = "Diameter"
        elif Objectives[i] == "Perímetro":
            objective = "Perimeter"
        else:
            raise("Error, objective not found.")
        
        if Gap_Opts[i] == "0.0":
            Gap_Opts[i] = "-"
        
        if instancia_anterior != instancia:
            file.write("\n\t\t\t\t\t\\hline\n")
            file.write("\t\t\t\t\t\\multirow{8}{3em}{\centering " + instancia + "} & \multirow{8}{3em}{\centering " + size + "} & \n")
            file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective + "} & \multirow{2}{6em}{\centering " + Opts[i] + "} & \multirow{2}{4em}{\centering " + Time_Opts[i] +"} & \multirow{2}{6em}{\centering " + LRs[i] +"} & \multirow{2}{3em}{\centering " + Time_RLs[i] +"} &  \multirow{2}{6em}{\centering " + Gap_LRs[i] + "} & \multirow{2}{3em}{\centering " + Gap_Opts[i] + "}\\\ & & & & & & & &\\\& &\n")
        else:
            if float(Time_Opts[i]) >= 10000:
                Time_Opts[i] = Time_Opts[i] + "*"
                Opts[i] = Opts[i] + "*"
            else:
                None
                
            if objective == "Perimeter":
                file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective +"} & \multirow{2}{6em}{\centering " + Opts[i] + "} & \multirow{2}{4em}{\centering " + Time_Opts[i] +"} & \multirow{2}{6em}{\centering " + LRs[i] +"} & \multirow{2}{3em}{\centering " + Time_RLs[i] +"} & \multirow{2}{6em}{\centering " + Gap_LRs[i] + "} & \multirow{2}{3em}{\centering " + Gap_Opts[i] + "}\\\ & & & & & & & &\\\ \n")
            else:
                file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective +"} & \multirow{2}{6em}{\centering " + Opts[i] + "} & \multirow{2}{4em}{\centering " + Time_Opts[i] +"} & \multirow{2}{6em}{\centering " + LRs[i] +"} & \multirow{2}{3em}{\centering " + Time_RLs[i] +"} & \multirow{2}{6em}{\centering " + Gap_LRs[i] + "} & \multirow{2}{3em}{\centering " + Gap_Opts[i] + "}\\\ & & & & & & & &\\\& &\n")
        
                
        instancia_anterior = instancia
        
    file.write("\n\t\t\t\t\t\\hline\n")
    file.write("\t\t\t\t\\end{tabular}\n")
    file.write("\t\t\t\\end{center}\n")
    file.write("\t\t\\end{adjustwidth}\n")
    file.write("\t\\end{table}\n")
    
    
    file.close()
    
    return None 


def drawEvaluation(Objectives, Instances, Gamma_2s, Gamma_4s, Gamma_14s):
    
    n = len(Objectives)
        
    file = open(f"{page}_Tables.txt", "w", encoding = "utf-8")

    
    file.write("\t\\begin{table}[!htp]\n")
    file.write("\t\t\\begin{adjustwidth}{-5cm}{-5cm}\n")
    file.write("\t\t\\caption{Continuous " + page.split("_")[0].lower() + " " + page.split("_")[1].lower() + "}\n")
    file.write("\t\t\\label{tab:Continuous_"+ page + "}\n")
    file.write("\t\t\t\\begin{center}\n")
    file.write("\t\t\t\t\\begin{tabular}{cc|c|ccc}\n")
    file.write("\t\t\t\t\t\\noalign{\smallskip}\n")
    file.write("\t\t\t\t\t\\multicolumn{2}{c|}{\multirow{2}{*}{\centering Instance}} & \multirow{2}{6em}{\centering Ob. Func.} & \multirow{2}{3em}{\centering $\gamma_2$} & \multirow{2}{3em}{\centering $\gamma_4$} & \multirow{2}{3em}{\centering $\gamma_{14}$}\\\ & & & & &\\\ \n")
    
    instancia_anterior = None
    
    for i in range(n):
        
        if Instances[i] == "Dataset_1 - 125 Conc":
            instancia = "North"
            size = "125"
        elif Instances[i] == "Dataset_2 - 96 Conc":
            instancia = "Center"
            size = "96"
        elif Instances[i] == "Dataset_3 - 57 Conc":
            instancia = "South"
            size = "57"
        elif Instances[i] == "Square_100":
            instancia = "Square"
            size = "100"
            continue
        elif Instances[i] == "Hexagon_127":
            instancia = "Hexagon"
            size = "127"
            continue
        else:
            print(Instances[i])
            raise("Error, instance not found.")
        
        if Objectives[i] == "Primeiro Momento Ajustado":
            objective = "First Mom. Adj."
        elif Objectives[i] == "Segundo Momento Ajustado":
            objective = "Second Mom. Adj."
        elif Objectives[i] == "Primeiro Momento":
            objective = "First Mom."
        elif Objectives[i] == "Segundo Momento":
            objective = "Second Mom."
        elif Objectives[i] == "Distância Máxima":
            objective = "Diameter"
        elif Objectives[i] == "Perímetro":
            objective = "Perimeter"
        else:
            raise("Error, objective not found.")
        
        if instancia_anterior != instancia:
            file.write("\n\t\t\t\t\t\\hline\n")
            file.write("\t\t\t\t\t\\multirow{12}{3em}{\centering " + instancia + "} & \multirow{12}{3em}{\centering " + size + "} & \n")
            file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective + "} & \multirow{2}{6em}{\centering " + Gamma_2s[i] + "} & \multirow{2}{3em}{\centering " + Gamma_4s[i] + "} & \multirow{2}{6em}{\centering " + Gamma_14s[i] + "}\\\ & & & & &\\\ & &\n")
        else:
            if objective == "Perimeter":
                file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective + "} & \multirow{2}{6em}{\centering " + Gamma_2s[i] + "} & \multirow{2}{3em}{\centering " + Gamma_4s[i] + "} & \multirow{2}{6em}{\centering " + Gamma_14s[i] + "}\\\ & & & & &\\\ \n")
            else:
                file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective + "} & \multirow{2}{6em}{\centering " + Gamma_2s[i] + "} & \multirow{2}{3em}{\centering " + Gamma_4s[i] + "} & \multirow{2}{6em}{\centering " + Gamma_14s[i] + "}\\\ & & & & &\\\ & &\n")
        
                
        instancia_anterior = instancia
        
    file.write("\n\t\t\t\t\t\\hline\n")
    file.write("\t\t\t\t\\end{tabular}\n")
    file.write("\t\t\t\\end{center}\n")
    file.write("\t\t\\end{adjustwidth}\n")
    file.write("\t\\end{table}\n\n\n\n\n\n\n\n\n")
    


    #SEGUNDA TABELA


    
    file.write("\t\\begin{table}[!htp]\n")
    file.write("\t\t\\begin{adjustwidth}{-5cm}{-5cm}\n")
    file.write("\t\t\\caption{Discrete " + page.split("_")[0].lower() + " " + page.split("_")[1].lower() + "}\n")
    file.write("\t\t\\label{tab:Discrete"+ page + "}\n")
    file.write("\t\t\t\\begin{center}\n")
    file.write("\t\t\t\t\\begin{tabular}{cc|c|ccc}\n")
    file.write("\t\t\t\t\t\\noalign{\smallskip}\n")
    file.write("\t\t\t\t\t\\multicolumn{2}{c|}{\multirow{2}{*}{\centering Instance}} & \multirow{2}{6em}{\centering Ob. Func.} & \multirow{2}{3em}{\centering $\gamma_2$} & \multirow{2}{3em}{\centering $\gamma_4$} & \multirow{2}{3em}{\centering $\gamma_{14}$}\\\ & & & & &\\\ \n")
    
    instancia_anterior = None
    
    for i in range(n):
        
        if Instances[i] == "Dataset_1 - 125 Conc":
            instancia = "North"
            size = "125"
            continue
        elif Instances[i] == "Dataset_2 - 96 Conc":
            instancia = "Center"
            size = "96"
            continue
        elif Instances[i] == "Dataset_3 - 57 Conc":
            instancia = "South"
            size = "57"
            continue
        elif Instances[i] == "Square_100":
            instancia = "Square"
            size = "100"
        elif Instances[i] == "Hexagon_127":
            instancia = "Hexagon"
            size = "127"
        else:
            print(Instances[i])
            raise("Error, instance not found.")
        
        if Objectives[i] == "Primeiro Momento Ajustado":
            objective = "First Mom. Adj."
        elif Objectives[i] == "Segundo Momento Ajustado":
            objective = "Second Mom. Adj."
        elif Objectives[i] == "Primeiro Momento":
            objective = "First Mom."
        elif Objectives[i] == "Segundo Momento":
            objective = "Second Mom."
        elif Objectives[i] == "Distância Máxima":
            objective = "Diameter"
        elif Objectives[i] == "Perímetro":
            objective = "Perimeter"
        else:
            raise("Error, objective not found.")
        
        if instancia_anterior != instancia:
            file.write("\n\t\t\t\t\t\\hline\n")
            file.write("\t\t\t\t\t\\multirow{8}{3em}{\centering " + instancia + "} & \multirow{8}{3em}{\centering " + size + "} & \n")
            file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective + "} & \multirow{2}{6em}{\centering " + Gamma_2s[i] + "} & \multirow{2}{3em}{\centering " + Gamma_4s[i] + "} & \multirow{2}{6em}{\centering " + Gamma_14s[i] + "}\\\ & & & & &\\\ & &\n")
        else:
            if objective == "Perimeter":
                file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective + "} & \multirow{2}{6em}{\centering " + Gamma_2s[i] + "} & \multirow{2}{3em}{\centering " + Gamma_4s[i] + "} & \multirow{2}{6em}{\centering " + Gamma_14s[i] + "}\\\ & & & & &\\\ \n")
            else:
                file.write("\t\t\t\t\t\\multirow{2}{10em}{\centering " + objective + "} & \multirow{2}{6em}{\centering " + Gamma_2s[i] + "} & \multirow{2}{3em}{\centering " + Gamma_4s[i] + "} & \multirow{2}{6em}{\centering " + Gamma_14s[i] + "}\\\ & & & & &\\\ & &\n")
        
                
        instancia_anterior = instancia
        
    file.write("\n\t\t\t\t\t\\hline\n")
    file.write("\t\t\t\t\\end{tabular}\n")
    file.write("\t\t\t\\end{center}\n")
    file.write("\t\t\\end{adjustwidth}\n")
    file.write("\t\\end{table}\n\n\n\n\n\n\n\n\n")
    
    
    file.close()
    
    return None 


def drawMultipleEvaluation(Objectives, Instances, Gamma_2s, Gamma_4s, Gamma_14s):
    
    n = len(Objectives)
        
    file = open(f"{page}_Tables.txt", "w", encoding = "utf-8")

    
    file.write("\t\\begin{table}[!htp]\n")
    file.write("\t\t\\begin{adjustwidth}{-5cm}{-5cm}\n")
    file.write("\t\t\\caption{Multiple continuous evaluation}\n")
    file.write("\t\t\\label{tab:Continuous_Multiple_Evaluation}\n")
    file.write("\t\t\t\\begin{center}\n")
    file.write("\t\t\t\t\\begin{tabular}{cc|c|ccc|ccc|ccc}\n")
    file.write("\t\t\t\t\t\\noalign{\smallskip}\n")
    file.write("\t\t\t\t\t\\multicolumn{2}{c|}{\multirow{4}{*}{\centering Instance}} & \multirow{4}{*}{\centering Ob. Func.} & \multicolumn{3}{c|}{\multirow{2}{*}{\centering $\gamma_2$}} & \multicolumn{3}{c|}{\multirow{2}{*}{\centering $\gamma_4$}} & \multicolumn{3}{c}{\multirow{2}{*}{\centering $\gamma_{14}$}}\\\ & & & & & & & & & & & \\\ \cline{4-12}	& & & \multirow{2}{*}{\centering Min} & \multirow{2}{*}{\centering Max} & \multirow{2}{*}{\centering Avg.} & \multirow{2}{*}{\centering Min} & \multirow{2}{*}{\centering Max} & \multirow{2}{*}{\centering Avg.} & \multirow{2}{*}{\centering Min} & \multirow{2}{*}{\centering Max} & \multirow{2}{*}{\centering Avg.} \\\ & & & & & & & & & & & \\\ \n")
    
    instancia_anterior = None
    
    for i in range(n):
        
        if Instances[i] == "Dataset_1 - 125 Conc":
            instancia = "North"
            size = "125"
        elif Instances[i] == "Dataset_2 - 96 Conc":
            instancia = "Center"
            size = "96"
        elif Instances[i] == "Dataset_3 - 57 Conc":
            instancia = "South"
            size = "57"
        elif Instances[i] == "Square_100":
            instancia = "Square"
            size = "100"
            continue
        elif Instances[i] == "Hexagon_127":
            instancia = "Hexagon"
            size = "127"
            continue
        else:
            print(Instances[i])
            raise("Error, instance not found.")
        
        if Objectives[i] == "Primeiro Momento Ajustado":
            objective = "First Mom. Adj."
        elif Objectives[i] == "Segundo Momento Ajustado":
            objective = "Second Mom. Adj."
        elif Objectives[i] == "Primeiro Momento":
            objective = "First Mom."
        elif Objectives[i] == "Segundo Momento":
            objective = "Second Mom."
        elif Objectives[i] == "Distância Máxima":
            objective = "Diameter"
        elif Objectives[i] == "Perímetro":
            objective = "Perimeter"
        else:
            raise("Error, objective not found.")
        
        if instancia_anterior != instancia:
            file.write("\n\t\t\t\t\t\\hline\n")
            file.write("\t\t\t\t\t\\multirow{12}{*}{\centering " + instancia + "} & \multirow{12}{*}{\centering " + size + "} & \n")
            file.write("\t\t\t\t\t\\multirow{2}{*}{\centering " + objective + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][2] + "}\\\ & & & & & & & & & & &\\\ & &\n")
        else:
            if objective == "Perimeter":
                file.write("\t\t\t\t\t\\multirow{2}{*}{\centering " + objective + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][2] + "}\\\ & & & & & & & & & & &\\\ \n")
            else:
                file.write("\t\t\t\t\t\\multirow{2}{*}{\centering " + objective + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][2] + "}\\\ & & & & & & & & & & &\\\ & &\n")

        
                
        instancia_anterior = instancia
        
    file.write("\n\t\t\t\t\t\\hline\n")
    file.write("\t\t\t\t\\end{tabular}\n")
    file.write("\t\t\t\\end{center}\n")
    file.write("\t\t\\end{adjustwidth}\n")
    file.write("\t\\end{table}\n\n\n\n\n\n\n\n\n")
    


    #SEGUNDA TABELA


    
    file.write("\t\\begin{table}[!htp]\n")
    file.write("\t\t\\begin{adjustwidth}{-5cm}{-5cm}\n")
    file.write("\t\t\\caption{Discrete continuous evaluation}\n")
    file.write("\t\t\\label{tab:Discrete_Multiple_Evaluation}\n")
    file.write("\t\t\t\\begin{center}\n")
    file.write("\t\t\t\t\\begin{tabular}{cc|c|ccc|ccc|ccc}\n")
    file.write("\t\t\t\t\t\\noalign{\smallskip}\n")
    file.write("\t\t\t\t\t\\multicolumn{2}{c|}{\multirow{4}{*}{\centering Instance}} & \multirow{4}{*}{\centering Ob. Func.} & \multicolumn{3}{c|}{\multirow{2}{*}{\centering $\gamma_2$}} & \multicolumn{3}{c|}{\multirow{2}{*}{\centering $\gamma_4$}} & \multicolumn{3}{c}{\multirow{2}{*}{\centering $\gamma_{14}$}}\\\ & & & & & & & & & & & \\\ \cline{4-12}	& & & \multirow{2}{*}{\centering Min} & \multirow{2}{*}{\centering Max} & \multirow{2}{*}{\centering Avg.} & \multirow{2}{*}{\centering Min} & \multirow{2}{*}{\centering Max} & \multirow{2}{*}{\centering Avg.} & \multirow{2}{*}{\centering Min} & \multirow{2}{*}{\centering Max} & \multirow{2}{*}{\centering Avg.} \\\ & & & & & & & & & & & \\\ \n")
    
    instancia_anterior = None
    
    for i in range(n):
        
        if Instances[i] == "Dataset_1 - 125 Conc":
            instancia = "North"
            size = "125"
            continue
        elif Instances[i] == "Dataset_2 - 96 Conc":
            instancia = "Center"
            size = "96"
            continue
        elif Instances[i] == "Dataset_3 - 57 Conc":
            instancia = "South"
            size = "57"
            continue
        elif Instances[i] == "Square_100":
            instancia = "Square"
            size = "100"
        elif Instances[i] == "Hexagon_127":
            instancia = "Hexagon"
            size = "127"
        else:
            raise("Error, instance not found.")
        
        if Objectives[i] == "Primeiro Momento Ajustado":
            objective = "First Mom. Adj."
        elif Objectives[i] == "Segundo Momento Ajustado":
            objective = "Second Mom. Adj."
        elif Objectives[i] == "Primeiro Momento":
            objective = "First Mom."
        elif Objectives[i] == "Segundo Momento":
            objective = "Second Mom."
        elif Objectives[i] == "Distância Máxima":
            objective = "Diameter"
        elif Objectives[i] == "Perímetro":
            objective = "Perimeter"
        else:
            raise("Error, objective not found.")
        
        if instancia_anterior != instancia:
            file.write("\n\t\t\t\t\t\\hline\n")
            file.write("\t\t\t\t\t\\multirow{8}{*}{\centering " + instancia + "} & \multirow{8}{*}{\centering " + size + "} & \n")
            file.write("\t\t\t\t\t\\multirow{2}{*}{\centering " + objective + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][2] + "}\\\ & & & & & & & & & & &\\\ & &\n")
        else:
            if objective == "Perimeter":
                file.write("\t\t\t\t\t\\multirow{2}{*}{\centering " + objective + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][2] + "}\\\ & & & & & & & & & & &\\\ \n")
            else:
                file.write("\t\t\t\t\t\\multirow{2}{*}{\centering " + objective + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_2s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_4s[i][2] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][0] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][1] + "} & \multirow{2}{*}{\centering " + Gamma_14s[i][2] + "}\\\ & & & & & & & & & & &\\\ & &\n")

        
                
        instancia_anterior = instancia
        
    file.write("\n\t\t\t\t\t\\hline\n")
    file.write("\t\t\t\t\\end{tabular}\n")
    file.write("\t\t\t\\end{center}\n")
    file.write("\t\t\\end{adjustwidth}\n")
    file.write("\t\\end{table}\n\n\n\n\n\n\n\n\n")
    
    
    file.close()
    
    return None 


def readCOmputationalResults(file_path, sheet_name):
    """reads the time series in the xlsx file

    Args:
        file_path (str): path of the xlsx file

    Returns:
        tuple: lista com o tempo e com o valor 
    """

    Objectives = []
    Instances = []
    Opts = []
    Time_Opts = []
    LRs = []
    Time_RLs = []
    Gap_Opts = []
    Gap_LRs = []

    # Read the Excel file into a DataFrame.
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    for linha in df.itertuples(index=False):
        objective = str(linha[0]) #Coluna 1
        Objectives.append(objective)
        instance = str(linha[3]) #Coluna 4
        Instances.append(instance)
        opt = str(format(float(linha[7]), ".1f")) #Coluna 8
        Opts.append(opt)
        time_opt = str(format(float(linha[8]), ".2f")) #Coluna 9
        Time_Opts.append(time_opt)
        lr = str(format(float(linha[9]), ".1f")) #Coluna 10
        LRs.append(lr)
        time_lr = str(format(float(linha[10]), ".2f")) #Coluna 11
        Time_RLs.append(time_lr)
        if sheet_name == "Single":
            gap_opt = "0.0"
        else:
            gap_opt = str(format(float(linha[11]), ".1f")) #Coluna 12
        Gap_Opts.append(gap_opt)
        gap_lr = str(format(float(linha[12]), ".1f")) #Coluna 13
        Gap_LRs.append(gap_lr)

    return Objectives, Instances, Opts, Time_Opts, LRs, Time_RLs, Gap_Opts, Gap_LRs


def readEvaluation(file_path, sheet_name):
    """reads the time series in the xlsx file

    Args:
        file_path (str): path of the xlsx file

    Returns:
        tuple: lista com o tempo e com o valor 
    """

    Objectives = []
    Instances = []
    Gamma_2s = []
    Gamma_4s = []
    Gamma_14s = []

    # Read the Excel file into a DataFrame.
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    
    first = True
    for linha in df.itertuples(index=False):
        
        if sheet_name == "Single_Compactness":
            objective = str(linha[0]) #Coluna 1
            Objectives.append(objective)
            instance = str(linha[3]) #Coluna 4
            Instances.append(instance)
            gamma_2 = str(format(float(linha[4]), ".2f")) #Coluna 5
            Gamma_2s.append(gamma_2)
            gamma_4 = str(format(float(linha[5]), ".2f")) #Coluna 6
            Gamma_4s.append(gamma_4)
            gamma_14 = str(format(float(linha[6]), ".2f")) #Coluna 7
            Gamma_14s.append(gamma_14)
        elif sheet_name == "Multiple_Compactness":
            if first:
                first = False
                continue
            else:
                objective = str(linha[0]) #Coluna 1
                Objectives.append(objective)
                instance = str(linha[3]) #Coluna 4
                Instances.append(instance)
                
                gamma_2 = [str(format(float(linha[22]), ".2f")), str(format(float(linha[23]), ".2f")), str(format(float(linha[24]), ".2f"))] #Coluna min 23, max 24, avg 25
                #gamma_2 = str(format(float(linha[24]), ".2f"))
                Gamma_2s.append(gamma_2)
                
                gamma_4 = [str(format(float(linha[25]), ".2f")), str(format(float(linha[26]), ".2f")), str(format(float(linha[27]), ".2f"))] #Coluna min 26, max 27, avg 28
                #gamma_4 = str(format(float(linha[27]), ".2f"))
                Gamma_4s.append(gamma_4)
                
                gamma_14 = [str(format(float(linha[28]), ".2f")), str(format(float(linha[29]), ".2f")), str(format(float(linha[30]), ".2f"))] #Coluna min 29, max 30, avg 31
                #gamma_14 = str(format(float(linha[30]), ".2f"))
                Gamma_14s.append(gamma_14)

    return Objectives, Instances, Gamma_2s, Gamma_4s, Gamma_14s

page = "Single"
Objectives, Instances, Opts, Time_Opts, LRs, Time_RLs, Gap_Opts, Gap_LRs = readCOmputationalResults(ficheiro, page)
drawComputationalResults(Objectives, Instances, Opts, Time_Opts, LRs, Time_RLs, Gap_Opts, Gap_LRs)

page = "Multiple"
Objectives, Instances, Opts, Time_Opts, LRs, Time_RLs, Gap_Opts, Gap_LRs = readCOmputationalResults(ficheiro, page)
drawComputationalResults(Objectives, Instances, Opts, Time_Opts, LRs, Time_RLs, Gap_Opts, Gap_LRs)

page = "Single_Compactness"
Objectives, Instances, Gamma_2s, Gamma_4s, Gamma_14s = readEvaluation(ficheiro, page)
drawEvaluation(Objectives, Instances, Gamma_2s, Gamma_4s, Gamma_14s)

page = "Multiple_Compactness"
Objectives, Instances, Gamma_2s, Gamma_4s, Gamma_14s = readEvaluation(ficheiro, page)
drawMultipleEvaluation(Objectives, Instances, Gamma_2s, Gamma_4s, Gamma_14s)
