import os                                                                                                             
import csv
from pathlib import Path
import math
from scipy.stats import rankdata
import sys
from ast import literal_eval
import pandas as pd

def new_rank(data, key):
    return rankdata([float(-1) * data[x][key] for x in range(len(data))], method='average')


only_manual = set()            
modified = dict()
bug_fixes = open("bug-fixes.txt", "r")
lines = bug_fixes.readlines()
for line in lines:
    temp_arr = line.split(";")
    i = 0
    if temp_arr[3][1] == "[":
        bug_temp = [literal_eval(temp_arr[3][1:-1])]
    else:
        bug_temp = literal_eval(temp_arr[3])
    
    if temp_arr[0] in modified:
        if temp_arr[1] in modified[temp_arr[0]]:
            modified[temp_arr[0]][temp_arr[1]][temp_arr[2]] = {"bug": bug_temp, "bug_only_plus": literal_eval(temp_arr[4]) }
        else:
            modified[temp_arr[0]][temp_arr[1]] = {temp_arr[2]: {"bug": bug_temp, "bug_only_plus": literal_eval(temp_arr[4]) }}
    else:
        modified[temp_arr[0]] = {temp_arr[1]: {temp_arr[2]: {"bug": bug_temp, "bug_only_plus": literal_eval(temp_arr[4]) }}}
    if temp_arr[5].strip() == "1":
        only_manual.add(temp_arr[0]+temp_arr[1])
        #print(only_manual)

#print(modified["ansible"]["13"])
#print(modified["ansible"]["1"]["collection.py"]["bug"][0][0])

current_directory = os.getcwd()
os.chdir("..")
parent_directory = os.getcwd()
os.chdir("Analysis")

sbfl_res = dict()
for p in modified:
    #if p == "pandas":
        sbfl_res_p = dict()
        for n in modified[p]:
            #if n == "42":
                not_continue = False
                totalpassed_num = 0
                totalfailed_num = 0
                file_fault = parent_directory+"/Results/"+p+"/"+p+"_"+n+"_buggy-fault_localization.txt"
                if not Path(file_fault).is_file():
                    not_continue = True
                if not not_continue:
                    print(file_fault)
                    text_file = open(file_fault, "r")
                    lines = text_file.readlines()
                    #print(lines)
                    print(len(lines))
                    text_file.close()
                    sbfl_res_n = dict()
                    i = 0
                    done = False
                    dict_with_file = dict()
                    while i < len(lines):
                        i += 1
                        temp_dict = dict()
                        temp_total_num_all = 0
                        while i < len(lines) and "___________________" not in lines[i]:
                            # print(lines[i])
                            temp = lines[i].rstrip().split(": ")
                            if "File" == temp[0]:
                                #print("MASUKKK")
                                file_name = temp[-1]
                            elif "Line" == temp[0]:
                                line_num = temp[-1]
                            elif "Passed" == temp[0]:
                                temp_dict["passed"] = int(temp[-1])
                                totalpassed_num += int(temp[-1])
                            elif "Failed" == temp[0]:
                                temp_dict["failed"] = int(temp[-1])
                                totalfailed_num += int(temp[-1])
                            elif "Tarantula_rank num" == temp[0]:
                                temp_dict["tarantula_rank"] = temp[-1]
                            elif "Tarantula_exam num" == temp[0]:
                                temp_dict["tarantula_exam"] = temp[-1]
                            elif "Tarantula_score num" == temp[0]:
                                temp_dict["tarantula_score"] = temp[-1]
                            elif "Ochiai_rank num" == temp[0]:
                                temp_dict["ochiai_rank"] = temp[-1]
                            elif "Ochiai_exam num" == temp[0]:
                                temp_dict["ochiai_exam"] = temp[-1]
                            elif "Ochiai_score num" == temp[0]:
                                temp_dict["ochiai_score"] = temp[-1]
                            elif "Op2_rank num" == temp[0]:
                                temp_dict["op2_rank"] = temp[-1]
                            elif "Op2_exam num" == temp[0]:
                                temp_dict["op2_exam"] = temp[-1]
                            elif "Op2_score num" == temp[0]:
                                temp_dict["op2_score"] = temp[-1]
                            elif "Barinel_rank num" == temp[0]:
                                temp_dict["barinel_rank"] = temp[-1]
                            elif "Barinel_exam num" == temp[0]:
                                temp_dict["barinel_exam"] = temp[-1]
                            elif "Barinel_score num" == temp[0]:
                                temp_dict["barinel_score"] = temp[-1]
                            elif "Dstar_rank num" == temp[0]:
                                temp_dict["dstar_rank"] = temp[-1]
                            elif "Dstar_exam num" == temp[0]:
                                temp_dict["dstar_exam"] = temp[-1]
                            elif "Dstar_score num" == temp[0]:
                                temp_dict["dstar_score"] = temp[-1]
                            elif "TEMP_NUM" == temp[0]:
                                temp_dict["temp_num"] = temp[-1]
                            elif "TOTAL_NUM_ALL" == temp[0]:
                                temp_dict["total_num_all"] = int(temp[-1])
                                temp_total_num_all = int(temp[-1])
                            elif "TOTAL_PER_ERROR:" in lines[i]:
                                temp_dict["total_per_error"] = temp[-1]
                            elif "TOTAL_PER_ERROR" in lines[i]:
                                temp = lines[i].rstrip().split(" ")
                                temp_dict["total_per_error"] = temp[-1]

                            i += 1

                        name_file_temp = file_name.split("/")[-1].rstrip()
                        # print(name_file_temp)
                        if ("test_" not in name_file_temp and  "_test" not in name_file_temp and "tests_" not in name_file_temp and "_tests" not in name_file_temp) or (p=="pandas" and n == "42"):
                            if file_name in dict_with_file:
                                if line_num in dict_with_file[file_name]:
                                    dict_with_file[file_name][line_num]["passed"] += temp_dict["passed"]
                                    dict_with_file[file_name][line_num]["failed"] += temp_dict["failed"]
                                else:
                                    dict_with_file[file_name][line_num] = temp_dict
                            else:
                                dict_with_file[file_name] = {}
                                dict_with_file[file_name][line_num] = temp_dict
                if not not_continue:
                    sbfl_res_p[n]=dict_with_file
        if bool(sbfl_res_p):
            sbfl_res[p] = sbfl_res_p
        
with open("all_sbfl.txt",'w', newline='', encoding='utf-8') as output:
    writer = csv.writer(output, delimiter=';')
    for p in sbfl_res:
        for n in sbfl_res[p]:
            for fn in sbfl_res[p][n]:
                for ln in sbfl_res[p][n][fn]:
                    arr_temp = [p,n,"a",fn,ln]
                    another = list(sbfl_res[p][n][fn][ln].values())
                    writer.writerow(arr_temp+another)
with open("exam_results.txt",'w', newline='', encoding='utf-8') as output:
    writer = csv.writer(output, delimiter=';')
    writer.writerow(["project","bug","file","bug-fixes","sloc", "tarantula_rank", "tarantula_exam", "ochiai_rank", "ochiai_exam", "op2_rank", "op2_exam", "barinel_rank", "barinel_exam", "dstar_rank", "dstar_exam"])
    for p in modified:
        #if p == "pandas":
            for n in modified[p]:
                #if n == "42":
                        if p+n in only_manual:
                            for f in modified[p][n]:
                                for arr in modified[p][n][f]["bug"]:
                                    op2_rank = sys.maxsize
                                    tarantula_rank = sys.maxsize
                                    ochiai_rank = sys.maxsize
                                    barinel_rank = sys.maxsize
                                    dstar_rank = sys.maxsize
                                    op2_file = ""
                                    tarantula_file = ""
                                    ochiai_file = ""
                                    barinel_file = ""
                                    dstar_file = ""
                                    op2_num_bug = ""
                                    tarantula_num_bug = ""
                                    ochiai_num_bug = ""
                                    barinel_num_bug = ""
                                    dstar_num_bug = ""
                                    for bug in arr:
                                        if p in sbfl_res and n in sbfl_res[p]:
                                            for file_long in sbfl_res[p][n]:
                                                # print(f)
                                                # print(file_long)
                                                if f in file_long:
                                                    if str(bug) in sbfl_res[p][n][file_long]:
                                                        if int(sbfl_res[p][n][file_long][str(bug)]['op2_rank']) < int(op2_rank):
                                                            op2_rank = sbfl_res[p][n][file_long][str(bug)]['op2_rank']
                                                            op2_file = file_long
                                                            op2_num_bug = str(bug)
                                                        if int(sbfl_res[p][n][file_long][str(bug)]['tarantula_rank']) < int(tarantula_rank):
                                                            tarantula_rank = sbfl_res[p][n][file_long][str(bug)]['tarantula_rank']
                                                            tarantula_file = file_long
                                                            tarantula_num_bug = str(bug)
                                                        if int(sbfl_res[p][n][file_long][str(bug)]['ochiai_rank']) < int(ochiai_rank):
                                                            ochiai_rank = sbfl_res[p][n][file_long][str(bug)]['ochiai_rank']
                                                            ochiai_file = file_long
                                                            ochiai_num_bug = str(bug)
                                                        if int(sbfl_res[p][n][file_long][str(bug)]['barinel_rank']) < int(barinel_rank):
                                                            barinel_rank = sbfl_res[p][n][file_long][str(bug)]['barinel_rank']
                                                            barinel_file = file_long
                                                            barinel_num_bug = str(bug)
                                                        if int(sbfl_res[p][n][file_long][str(bug)]['dstar_rank']) < int(dstar_rank):
                                                            dstar_rank = sbfl_res[p][n][file_long][str(bug)]['dstar_rank']
                                                            dstar_file = file_long
                                                            dstar_num_bug = str(bug)
                                    if op2_file != "":
                                        another = [sbfl_res[p][n][tarantula_file][tarantula_num_bug]["total_num_all"],tarantula_rank,sbfl_res[p][n][tarantula_file][tarantula_num_bug]["tarantula_exam"],ochiai_rank,sbfl_res[p][n][ochiai_file][ochiai_num_bug]["ochiai_exam"],op2_rank,sbfl_res[p][n][op2_file][op2_num_bug]["op2_exam"],barinel_rank,sbfl_res[p][n][barinel_file][barinel_num_bug]["barinel_exam"],dstar_rank,sbfl_res[p][n][dstar_file][dstar_num_bug]["dstar_exam"]]
                                        arr_temp = [p,n,f,tarantula_num_bug]
                                        writer.writerow(arr_temp+another)
                                    else:
                                        print("NOT FOUND "+str(p)+" "+str(n)+" "+str(f))
                                        print(arr)
                                        size = 0
                                        total_all = 0
                                        check_name = ""
                                        check_bug = ""
                                        for file_long in sbfl_res[p][n]:
                                            size += len(sbfl_res[p][n][file_long])
                                            check_name = file_long
                                        for b in sbfl_res[p][n][check_name]:
                                            if "total_num_all" not in sbfl_res[p][n][file_long][b]:
                                                not_record = True
                                            else: 
                                                total_all = int(sbfl_res[p][n][file_long][b]["total_num_all"])
                                                check_bug = b
                                                break
                                        if not not_record:
                                            if total_all == 0:
                                                temp = 1
                                            else:
                                                temp = float(size/total_all)

                                            temp_worst = 1
                                            if "total_per_error" not in sbfl_res[p][n][file_long][b]:
                                                sbfl_res[p][n][file_long][b]["total_per_error"] = -1
                                            another = [sbfl_res[p][n][file_long][b]["total_num_all"],size,temp,size,temp,size,temp,size,temp,size,temp]
                                            arr_temp = [p,n,f,arr[0]]
                                            writer.writerow(arr_temp+another)
                                            print("ADDED")

                        else:
                            for f in modified[p][n]:
                                for bug in modified[p][n][f]["bug"]:
                                    arr_temp = [p,n,f,bug]
                                    another = ["NOT FOUND"]
                                    save_f = ""
                                    save_b = ""

                                    not_record = False
                                    if p in sbfl_res and n in sbfl_res[p]:
                                            for file_long in sbfl_res[p][n]:
                                                if f in file_long:
                                                    if str(bug) in sbfl_res[p][n][file_long]:
                                                        #print("MASUKKK SINIII")
                                                        save_b = str(bug)
                                                        save_f = file_long
                                                        
                                                        another = [sbfl_res[p][n][file_long][str(bug)]["total_num_all"],sbfl_res[p][n][file_long][str(bug)]["tarantula_rank"],sbfl_res[p][n][file_long][str(bug)]["tarantula_exam"],sbfl_res[p][n][file_long][str(bug)]["ochiai_rank"],sbfl_res[p][n][file_long][str(bug)]["ochiai_exam"],sbfl_res[p][n][file_long][str(bug)]["op2_rank"],sbfl_res[p][n][file_long][str(bug)]["op2_exam"],sbfl_res[p][n][file_long][str(bug)]["barinel_rank"],sbfl_res[p][n][file_long][str(bug)]["barinel_exam"],sbfl_res[p][n][file_long][str(bug)]["dstar_rank"],sbfl_res[p][n][file_long][str(bug)]["dstar_exam"]]
                                        
                                                        break


                                            if another[0] == "NOT FOUND":
                                                size = 0
                                                total_all = 0
                                                check_name = ""
                                                check_bug = ""
                                                for file_long in sbfl_res[p][n]:
                                                    size += len(sbfl_res[p][n][file_long])
                                                    check_name = file_long
                                                for b in sbfl_res[p][n][check_name]:
                                                    if "total_num_all" not in sbfl_res[p][n][file_long][b]:
                                                        not_record = True
                                                    else: 
                                                        total_all = int(sbfl_res[p][n][file_long][b]["total_num_all"])
                                                        check_bug = b
                                                        break
                                                if not not_record:
                                                    if total_all == 0:
                                                        temp = 1
                                                    else:
                                                        temp = float(size/total_all)

                                                    temp_worst = 1
                                                    if "total_per_error" not in sbfl_res[p][n][file_long][b]:
                                                        sbfl_res[p][n][file_long][b]["total_per_error"] = -1
                                                    another = [sbfl_res[p][n][file_long][b]["total_num_all"],size,temp,size,temp,size,temp,size,temp,size,temp]
                                            
                                            if not not_record:
                                                writer.writerow(arr_temp+another)
                                set_bug_only_plus = set(modified[p][n][f]["bug_only_plus"])
                                for bug in set_bug_only_plus:
                                    arr_temp = [p,n,f,bug]
                                    another = ["NOT FOUND"]
                                    save_f = ""
                                    save_b = ""

                                    not_record = False
                                    if p in sbfl_res and n in sbfl_res[p]:
                                            for file_long in sbfl_res[p][n]:
                                                if f in file_long:
                                                    
                                                    if str(bug) in sbfl_res[p][n][file_long]:
                                                        #print("MASUKKK SINIII")
                                                        save_b = str(bug)
                                                        save_f = file_long
                                                        
                                                        another = [sbfl_res[p][n][file_long][str(bug)]["total_num_all"],sbfl_res[p][n][file_long][str(bug)]["tarantula_rank"],sbfl_res[p][n][file_long][str(bug)]["tarantula_exam"],sbfl_res[p][n][file_long][str(bug)]["ochiai_rank"],sbfl_res[p][n][file_long][str(bug)]["ochiai_exam"],sbfl_res[p][n][file_long][str(bug)]["op2_rank"],sbfl_res[p][n][file_long][str(bug)]["op2_exam"],sbfl_res[p][n][file_long][str(bug)]["barinel_rank"],sbfl_res[p][n][file_long][str(bug)]["barinel_exam"],sbfl_res[p][n][file_long][str(bug)]["dstar_rank"],sbfl_res[p][n][file_long][str(bug)]["dstar_exam"]]
                                        
                                                        break


                                            if another[0] == "NOT FOUND":
                                                
                                                size = 0
                                                total_all = 0
                                                check_name = ""
                                                check_bug = ""
                                                for file_long in sbfl_res[p][n]:
                                                    size += len(sbfl_res[p][n][file_long])
                                                    check_name = file_long
                                                for b in sbfl_res[p][n][check_name]:
                                                    if "total_num_all" not in sbfl_res[p][n][file_long][b]:
                                                        not_record = True
                                                    else: 
                                                        total_all = int(sbfl_res[p][n][file_long][b]["total_num_all"])
                                                        check_bug = b
                                                        break
                                                if not not_record:
                                                    if total_all == 0:
                                                        temp = 1
                                                    else:
                                                        temp = float(size/total_all)

                                                    temp_worst = 1
                                                    if "total_per_error" not in sbfl_res[p][n][file_long][b]:
                                                        sbfl_res[p][n][file_long][b]["total_per_error"] = -1
                                                    another = [sbfl_res[p][n][file_long][b]["total_num_all"],size,temp,size,temp,size,temp,size,temp,size,temp]
                                            
                                            if not not_record:
                                                writer.writerow(arr_temp+another)
                                                

df = pd.read_csv('exam_results.txt',sep=';') 
data = df.to_numpy()
all_result = [['project', 'line', 
'tarantula_best', 
'tarantula_worst',
'tarantula_average',
'ochiai_best', 
'ochiai_worst',
'ochiai_average',
'op2_best', 
'op2_worst',
'op2_average',
'barinel_best', 
'barinel_worst',
'barinel_average',
'dstar_best', 
'dstar_worst',
'dstar_average',
'tarantula_rank_best', 'ochiai_rank_best', 'op2_rank_best', 'barinel_rank_best', 'dstar_rank_best',
'tarantula_rank_average', 'ochiai_rank_average', 'op2_rank_average', 'barinel_rank_average', 'dstar_rank_average',
'tarantula_rank_worst', 'ochiai_rank_worst', 'op2_rank_worst', 'barinel_rank_worst', 'dstar_rank_worst',
'tarantula_rank_flt_best', 'ochiai_rank_flt_best', 'op2_rank_flt_best', 'barinel_rank_flt_best', 'dstar_rank_flt_best',
'tarantula_rank_flt_worst', 'ochiai_rank_flt_worst', 'op2_rank_flt_worst', 'barinel_rank_flt_worst', 'dstar_rank_flt_worst',
'tarantula_rank_flt_average', 'ochiai_rank_flt_average', 'op2_rank_flt_average', 'barinel_rank_flt_average', 'dstar_rank_flt_average']]
i = 0
tarantula = 0
tarantula_worst = 0
ochiai = 0
ochiai_worst = 0
op2 = 0
op2_worst = 0
barinel = 0
barinel_worst = 0
dstar = 0
dstar_worst = 0
worst_scenario_rank = []
average_scenario_rank = []
while i < len(data):
    #print(data[i])
    project = df['project'][i]
    bug = df['bug'][i]
    temp_tarantula = []
    temp_ochiai = []
    temp_op2 = []
    temp_barinel = []
    temp_dstar = []

    temp_tarantula_rank = []
    temp_ochiai_rank = []
    temp_op2_rank = []
    temp_barinel_rank = []
    temp_dstar_rank = []

    while i < len(data) and df['project'][i] == project and df['bug'][i] == bug:
        temp_tarantula.append(float(df['tarantula_exam'][i]))
        temp_ochiai.append(float(df['ochiai_exam'][i]))
        temp_op2.append(float(df['op2_exam'][i]))
        temp_barinel.append(df['barinel_exam'][i])
        temp_dstar.append(df['dstar_exam'][i])
        
        temp_tarantula_rank.append(float(df['tarantula_rank'][i]))
        temp_ochiai_rank.append(float(df['ochiai_rank'][i]))
        temp_op2_rank.append(float(df['op2_rank'][i]))
        temp_barinel_rank.append(df['barinel_rank'][i])
        temp_dstar_rank.append(df['dstar_rank'][i])

        i += 1
    #cek ulang bagian sortingnya
    temp_tarantula.sort()
    temp_ochiai.sort()
    temp_op2.sort()
    temp_barinel.sort()
    temp_dstar.sort()
    
    temp_tarantula_rank.sort()
    temp_ochiai_rank.sort()
    temp_op2_rank.sort()
    temp_barinel_rank.sort()
    temp_dstar_rank.sort()


    #print(temp_tarantula)
    size = len(temp_tarantula)
    if size == 1:
        half_size = 1
    else:
        half_size = int(size / 2)
    temp_array = [project, bug] 
    temp_array.extend([temp_tarantula[0],float(sum(temp_tarantula) / len(temp_tarantula)),float(sum(temp_tarantula[:half_size]) / len(temp_tarantula[:half_size])) ]  )
    temp_array.extend([temp_ochiai[0], float(sum(temp_ochiai) / len(temp_ochiai)),float(sum(temp_ochiai[:half_size]) / len(temp_ochiai[:half_size]))  ]  )
    temp_array.extend([temp_op2[0], float(sum(temp_op2) / len(temp_op2)),float(sum(temp_op2[:half_size]) / len(temp_op2[:half_size]))  ]  )
    temp_array.extend([temp_barinel[0], float(sum(temp_barinel) / len(temp_barinel)),float(sum(temp_barinel[:half_size]) / len(temp_barinel[:half_size]))  ]  )
    temp_array.extend([temp_dstar[0], float(sum(temp_dstar) / len(temp_dstar)),float(sum(temp_dstar[:half_size]) / len(temp_dstar[:half_size])) ]  )

    temp_array.extend([temp_tarantula_rank[0], temp_ochiai_rank[0],temp_op2_rank[0],temp_barinel_rank[0],temp_dstar_rank[0]])
    temp_array.extend([temp_tarantula_rank[int(len(temp_tarantula_rank)/2)], temp_ochiai_rank[int(len(temp_ochiai_rank)/2)],temp_op2_rank[int(len(temp_op2_rank)/2)],temp_barinel_rank[int(len(temp_barinel_rank)/2)],temp_dstar_rank[int(len(temp_dstar_rank)/2)]])
    temp_array.extend([temp_tarantula_rank[-1], temp_ochiai_rank[-1],temp_op2_rank[-1],temp_barinel_rank[-1],temp_dstar_rank[-1]])
    
    sort_flt = {0: temp_tarantula[0], 1: temp_ochiai[0], 2: temp_op2[0], 3: temp_barinel[0], 4: temp_dstar[0]}
    temp_flt = {k: v for k, v in sorted(sort_flt.items(), key=lambda item: item[1])}
    m = 1
    add_to_array = [0,0,0,0,0]
    rank_save = dict()
    prev_temp = -10
    # print(temp_flt)
    for key, value in temp_flt.items():
        if prev_temp == -10:
            prev_temp = value
        else:
            if prev_temp != value:
                m += 1
            prev_temp = value
        add_to_array[key] = m
        if m in rank_save:
            rank_save[m] += 1
        else:
            rank_save[m] = 1
        # m += 1
    #update the rank. Example: the rank before (1,1,1,1,1) -> after (2.5,2.5,2.5,2.5,2.5),    
    update_rank = dict()
    curr_rank = 0
    for rank_idx in [1,2,3,4,5]:
        if rank_idx in rank_save:
            if rank_save[rank_idx] > 1:
                update_rank[rank_idx] = curr_rank + (rank_save[rank_idx]/2)
                curr_rank += rank_save[rank_idx]
            else:
                curr_rank += 1
                update_rank[rank_idx] = curr_rank
    add_to_array_updated = []
    for add_arr_val in add_to_array:
        add_to_array_updated.append(update_rank[add_arr_val])


    temp_array.extend(add_to_array_updated)

    sort_flt = {0: temp_tarantula[-1], 1: temp_ochiai[-1], 2: temp_op2[-1], 3: temp_barinel[-1], 4: temp_dstar[-1]}
    temp_flt = {k: v for k, v in sorted(sort_flt.items(), key=lambda item: item[1])}
    m = 1
    add_to_array = [0,0,0,0,0]
    rank_save = dict()
    prev_temp = -10
    # print(temp_flt)
    for key, value in temp_flt.items():
        if prev_temp == -10:
            prev_temp = value
        else:
            if prev_temp != value:
                m += 1
            prev_temp = value
        add_to_array[key] = m
        if m in rank_save:
            rank_save[m] += 1
        else:
            rank_save[m] = 1
    
    update_rank = dict()
    curr_rank = 0
    for rank_idx in [1,2,3,4,5]:
        if rank_idx in rank_save:
            if rank_save[rank_idx] > 1:
                update_rank[rank_idx] = curr_rank + (rank_save[rank_idx]/2)
                curr_rank += rank_save[rank_idx]
            else:
                curr_rank += 1
                update_rank[rank_idx] = curr_rank
    add_to_array_updated = []
    for add_arr_val in add_to_array:
        add_to_array_updated.append(update_rank[add_arr_val])

    temp_array.extend(add_to_array_updated)

    sort_flt = {0: temp_tarantula[int(len(temp_tarantula_rank)/2)], 1: temp_ochiai[int(len(temp_ochiai_rank)/2)], 2: temp_op2[int(len(temp_op2_rank)/2)], 3: temp_barinel[int(len(temp_barinel_rank)/2)], 4: temp_dstar[int(len(temp_dstar_rank)/2)]}
    temp_flt = {k: v for k, v in sorted(sort_flt.items(), key=lambda item: item[1])}
    m = 1
    add_to_array = [0,0,0,0,0]
    rank_save = dict()
    prev_temp = -10
    for key, value in temp_flt.items():
        if prev_temp == -10:
            prev_temp = value
        else:
            if prev_temp != value:
                m += 1
            prev_temp = value
        add_to_array[key] = m
        if m in rank_save:
            rank_save[m] += 1
        else:
            rank_save[m] = 1
    
    update_rank = dict()
    curr_rank = 0
    for rank_idx in [1,2,3,4,5]:
        if rank_idx in rank_save:
            if rank_save[rank_idx] > 1:
                update_rank[rank_idx] = curr_rank + (rank_save[rank_idx]/2)
                curr_rank += rank_save[rank_idx]
            else:
                curr_rank += 1
                update_rank[rank_idx] = curr_rank
    add_to_array_updated = []
    for add_arr_val in add_to_array:
        add_to_array_updated.append(update_rank[add_arr_val])

    temp_array.extend(add_to_array_updated)
    
    tarantula += temp_tarantula[0]
    ochiai += temp_ochiai[0]
    op2 += temp_op2[0]
    barinel += temp_barinel[0]
    dstar += temp_dstar[0]
    all_result.append(temp_array)

size_all = len(all_result) -1
#print(tarantula)
print(size_all)
print("BEST CASE")
print(tarantula/size_all)
print(ochiai/size_all)
print(op2/size_all)
print(barinel/size_all)
print(dstar/size_all)


output_name = "combine.txt"
if len(sys.argv) >=2:
    output_name = sys.argv[2]
with open(output_name,'w', newline='', encoding='utf-8') as output:
    writer = csv.writer(output, delimiter=';')
    for i in all_result:
        writer.writerow(i)
                                
