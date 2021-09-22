import os                                                                                                             
import csv

import pandas as pd
from scipy import stats
from statistics import mean, stdev
from math import sqrt
import sys
def cliffsDelta(lst1, lst2, **dull):

    """Returns delta and true if there are more than 'dull' differences"""
    if not dull:
        dull = {'small': 0.147, 'medium': 0.33, 'large': 0.474} # effect sizes from (Hess and Kromrey, 2004)
    m, n = len(lst1), len(lst2)
    lst2 = sorted(lst2)
    j = more = less = 0
    for repeats, x in runs(sorted(lst1)):
        while j <= (n - 1) and lst2[j] < x:
            j += 1
        more += j*repeats
        while j <= (n - 1) and lst2[j] == x:
            j += 1
        less += (n - j)*repeats
    d = (more - less) / (m*n)
    size = lookup_size(d, dull)
    return d, size


def lookup_size(delta: float, dull: dict) -> str:
    """
    :type delta: float
    :type dull: dict, a dictionary of small, medium, large thresholds.
    """
    delta = abs(delta)
    if delta < dull['small']:
        return 'negligible'
    if dull['small'] <= delta < dull['medium']:
        return 'small'
    if dull['medium'] <= delta < dull['large']:
        return 'medium'
    if delta >= dull['large']:
        return 'large'


def runs(lst):
    """Iterator, chunks repeated values"""
    for j, two in enumerate(lst):
        if j == 0:
            one, i = two, 0
        if one != two:
            yield j - i, one
            i = j
        one = two
    yield j - i + 1, two


def getting_all(df):
    #print(stats.normaltest(df['ochiai_best_best']))
    #print(stats.normaltest(df['tarantula_best_best']))
    #print(stats.normaltest(df['barinel_best_best']))
    #print(stats.normaltest(df['op2_best_best']))
    #print(stats.normaltest(df['dstar_best_best']))
    
    print("EXAM BEST-CASE SCENARIO")
    print("****************************************************************************")
    print("TARANTULA: "+str(mean(df['tarantula_best_best'])))
    print("OCHIAI: "+str(mean(df['ochiai_best_best'])))
    print("OP2: "+str(mean(df['op2_best_best'])))
    print("BARINEL: "+str(mean(df['barinel_best_best'])))
    print("DSTAR: "+str(mean(df['dstar_best_best'])))
    print("****************************************************************************\n")

    
    print("EXAM AVERAGE-CASE SCENARIO")
    print("****************************************************************************")
    print("TARANTULA: "+str(mean(df['tarantula_average_best'])))
    print("OCHIAI: "+str(mean(df['ochiai_average_best'])))
    print("OP2: "+str(mean(df['op2_average_best'])))
    print("BARINEL: "+str(mean(df['barinel_average_best'])))
    print("DSTAR: "+str(mean(df['dstar_average_best'])))
    print("****************************************************************************\n")

    print("EXAM WORST-CASE SCENARIO")
    print("****************************************************************************")
    print("TARANTULA: "+str(mean(df['tarantula_worst_best'])))
    print("OCHIAI: "+str(mean(df['ochiai_worst_best'])))
    print("OP2: "+str(mean(df['op2_worst_best'])))
    print("BARINEL: "+str(mean(df['barinel_worst_best'])))
    print("DSTAR: "+str(mean(df['dstar_worst_best'])))
    print("****************************************************************************\n")
    
    print("TOURNAMENT RANKING BEST-CASE SCENARIO (EXAM)")
    print("****************************************************************************")
    name_flt = ["tarantula_best_best", "ochiai_best_best", "op2_best_best", "barinel_best_best", "dstar_best_best"]
    print_name_flt = ["TARANTULA", "OCHIAI","OP2", "BARINEL", "DSTAR"]
    for i, name_i in enumerate(name_flt):
        win_number = 0
        temp = name_flt.copy()
        del temp[i]
        for j in temp:
            temp_pvalue = stats.ranksums(df[name_i],df[j])
            #print(temp_pvalue)
            if temp_pvalue.pvalue < 0.05:
                if mean(df[name_i]) < mean(df[j]):
                    win_number += 1
        print(print_name_flt[i]+": "+str(win_number))
    print("****************************************************************************\n")
    

    
    print("TOURNAMENT RANKING AVERAGE-CASE SCENARIO (EXAM)")
    print("****************************************************************************")
    name_flt = ["tarantula_average_best", "ochiai_average_best", "op2_average_best", "barinel_average_best", "dstar_average_best"]
    for i, name_i in enumerate(name_flt):
        win_number = 0
        temp = name_flt.copy()
        del temp[i]
        for j in temp:
            temp_pvalue = stats.ranksums(df[name_i],df[j])
            #print(temp_pvalue)
            if temp_pvalue.pvalue < 0.05:
                if mean(df[name_i]) < mean(df[j]):
                    win_number += 1
        print(print_name_flt[i]+": "+str(win_number))
    print("****************************************************************************\n")
    
    print("TOURNAMENT RANKING WORST-CASE SCENARIO (EXAM)")
    print("****************************************************************************")
    name_flt = ["tarantula_worst_best", "ochiai_worst_best", "op2_worst_best", "barinel_worst_best", "dstar_worst_best"]
    for i, name_i in enumerate(name_flt):
        win_number = 0
        temp = name_flt.copy()
        del temp[i]
        for j in temp:
            #temp_pvalue = stats.chisquare(df[name_i],f_exp=df[j])
            temp_pvalue = stats.ranksums(df[name_i],df[j])
            print(temp_pvalue)
            if temp_pvalue.pvalue < 0.05:
                if mean(df[name_i]) < mean(df[j]):
                    win_number += 1
        print(print_name_flt[i]+": "+str(win_number))
    print("****************************************************************************\n")
    
    
    print("FLT RANK BEST-CASE SCENARIO")
    print("****************************************************************************\n")
    print("TARANTULA: "+str(mean(df['tarantula_rank_flt'])))
    print("OCHIAI: "+str(mean(df['ochiai_rank_flt'])))
    print("OP2: "+str(mean(df['op2_rank_flt'])))
    print("BARINEL: "+str(mean(df['barinel_rank_flt'])))
    print("DSTAR: "+str(mean(df['dstar_rank_flt'])))
    print("****************************************************************************\n")
    


    print("TOURNAMENT RANKING BEST-CASE SCENARIO (FLT RANK)")
    print("****************************************************************************")
    name_flt = ["tarantula_rank_flt", "ochiai_rank_flt", "op2_rank_flt", "barinel_rank_flt", "dstar_rank_flt"]
    for i, name_i in enumerate(name_flt):
        win_number = 0
        temp = name_flt.copy()
        del temp[i]
        for j in temp:
            #temp_pvalue = stats.chisquare(df[name_i],f_exp=df[j])
            temp_pvalue = stats.ranksums(df[name_i],df[j])
            print(temp_pvalue)
            if temp_pvalue.pvalue < 0.05:
                if mean(df[name_i]) < mean(df[j]):
                    win_number += 1
        print(print_name_flt[i]+": "+str(win_number))
    print("****************************************************************************\n")
    
    print("TOP-K BEST-CASE SCENARIO (PERCENT)")
    print("****************************************************************************")
    print("TOP 5")
    print("TARANTULA: "+str(len(df[df['tarantula_rank_best']<=5])/len(df['tarantula_rank_best'])))
    print("OCHIAI: "+str(len(df[df['ochiai_rank_best']<=5])/len(df['tarantula_rank_best'])))
    print("OP2: "+str(len(df[df['op2_rank_best']<=5])/len(df['tarantula_rank_best'])))
    print("BARINEL: "+str(len(df[df['barinel_rank_best']<=5])/len(df['tarantula_rank_best'])))
    print("DSTAR: "+str(len(df[df['dstar_rank_best']<=5])/len(df['tarantula_rank_best'])))

    print("\nTOP 10")
    print("TARANTULA: "+str(len(df[df['tarantula_rank_best']<=10])/len(df['tarantula_rank_best'])))
    print("OCHIAI: "+str(len(df[df['ochiai_rank_best']<=10])/len(df['tarantula_rank_best'])))
    print("OP2: "+str(len(df[df['op2_rank_best']<=10])/len(df['tarantula_rank_best'])))
    print("BARINEL: "+str(len(df[df['barinel_rank_best']<=10])/len(df['tarantula_rank_best'])))
    print("DSTAR: "+str(len(df[df['dstar_rank_best']<=10])/len(df['tarantula_rank_best'])))


    print("\nTOP 200")
    print("TARANTULA: "+str(len(df[df['tarantula_rank_best']<=200])/len(df['tarantula_rank_best'])))
    print("OCHIAI: "+str(len(df[df['ochiai_rank_best']<=200])/len(df['tarantula_rank_best'])))
    print("OP2: "+str(len(df[df['op2_rank_best']<=200])/len(df['tarantula_rank_best'])))
    print("BARINEL: "+str(len(df[df['barinel_rank_best']<=200])/len(df['tarantula_rank_best'])))
    print("DSTAR: "+str(len(df[df['dstar_rank_best']<=200])/len(df['tarantula_rank_best'])))

    print("****************************************************************************\n")
    
    print("TOP-K AVERAGE-CASE SCENARIO (PERCENT)")
    print("****************************************************************************")
    print("TOP 5")
    print("TARANTULA: "+str(len(df[df['tarantula_rank_average']<=5])/len(df['tarantula_rank_average'])))
    print("OCHIAI: "+str(len(df[df['ochiai_rank_average']<=5])/len(df['tarantula_rank_average'])))
    print("OP2: "+str(len(df[df['op2_rank_average']<=5])/len(df['tarantula_rank_average'])))
    print("BARINEL: "+str(len(df[df['barinel_rank_average']<=5])/len(df['tarantula_rank_average'])))
    print("DSTAR: "+str(len(df[df['dstar_rank_average']<=5])/len(df['tarantula_rank_average'])))

    print("\nTOP 10")
    print("TARANTULA: "+str(len(df[df['tarantula_rank_average']<=10])/len(df['tarantula_rank_average'])))
    print("OCHIAI: "+str(len(df[df['ochiai_rank_average']<=10])/len(df['tarantula_rank_average'])))
    print("OP2: "+str(len(df[df['op2_rank_average']<=10])/len(df['tarantula_rank_average'])))
    print("BARINEL: "+str(len(df[df['barinel_rank_average']<=10])/len(df['tarantula_rank_average'])))
    print("DSTAR: "+str(len(df[df['dstar_rank_average']<=10])/len(df['tarantula_rank_average'])))

    print("\nTOP 200")
    print("TARANTULA: "+str(len(df[df['tarantula_rank_average']<=200])/len(df['tarantula_rank_average'])))
    print("OCHIAI: "+str(len(df[df['ochiai_rank_average']<=200])/len(df['tarantula_rank_average'])))
    print("OP2: "+str(len(df[df['op2_rank_average']<=200])/len(df['tarantula_rank_average'])))
    print("BARINEL: "+str(len(df[df['barinel_rank_average']<=200])/len(df['tarantula_rank_average'])))
    print("DSTAR: "+str(len(df[df['dstar_rank_average']<=200])/len(df['tarantula_rank_average'])))

    print("****************************************************************************\n")
    
    print("TOP-K WORST-CASE SCENARIO (PERCENT)")
    print("****************************************************************************")
    
    print("TOP 5")
    print("TARANTULA: "+str(len(df[df['tarantula_rank_worst']<=5])/len(df['tarantula_rank_worst'])))
    print("OCHIAI: "+str(len(df[df['ochiai_rank_worst']<=5])/len(df['tarantula_rank_worst'])))
    print("OP2: "+str(len(df[df['op2_rank_worst']<=5])/len(df['tarantula_rank_worst'])))
    print("BARINEL: "+str(len(df[df['barinel_rank_worst']<=5])/len(df['tarantula_rank_worst'])))
    print("DSTAR: "+str(len(df[df['dstar_rank_worst']<=5])/len(df['tarantula_rank_worst'])))

    print("\nTOP 10")
    print("TARANTULA: "+str(len(df[df['tarantula_rank_worst']<=10])/len(df['tarantula_rank_worst'])))
    print("OCHIAI: "+str(len(df[df['ochiai_rank_worst']<=10])/len(df['tarantula_rank_worst'])))
    print("OP2: "+str(len(df[df['op2_rank_worst']<=10])/len(df['tarantula_rank_worst'])))
    print("BARINEL: "+str(len(df[df['barinel_rank_worst']<=10])/len(df['tarantula_rank_worst'])))
    print("DSTAR: "+str(len(df[df['dstar_rank_worst']<=10])/len(df['tarantula_rank_worst'])))


    print("\nTOP 200")
    print("TARANTULA: "+str(len(df[df['tarantula_rank_worst']<=200])/len(df['tarantula_rank_worst'])))
    print("OCHIAI: "+str(len(df[df['ochiai_rank_worst']<=200])/len(df['tarantula_rank_worst'])))
    print("OP2: "+str(len(df[df['op2_rank_worst']<=200])/len(df['tarantula_rank_worst'])))
    print("BARINEL: "+str(len(df[df['barinel_rank_worst']<=200])/len(df['tarantula_rank_worst'])))
    print("DSTAR: "+str(len(df[df['dstar_rank_worst']<=200])/len(df['tarantula_rank_worst'])))
    
    
    print("****************************************************************************\n")
    
    
    for scen in ["best", "average", "worst"]:
        print("TOP-K "+scen+"-CASE SCENARIO SIGNIFICANT TEST AND EFFECT SIZE")
        print("****************************************************************************")
        name_flt = ["tarantula_rank_"+scen, "ochiai_rank_"+scen, "op2_rank_"+scen, "barinel_rank_"+scen, "dstar_rank_"+scen]
        for i, name_i in enumerate(name_flt):
            win_number = 0
            temp = name_flt.copy()
            del temp[i]
            for j in temp:
                #temp_pvalue = stats.chisquare(df[name_i],f_exp=df[j])
                
                print(name_i+" VS "+j)
                for g in [5,10, 200]:
                    print("TOP-"+str(g))
                    new_df = df[(df[name_i]<=g) | (df[j]<=g)]
                    temp_pvalue = stats.ranksums(new_df[name_i],new_df[j])
                    print(temp_pvalue)
                    print(cliffsDelta(new_df[name_i],new_df[j]))
                    if temp_pvalue.pvalue < 0.05:
                        if mean(new_df[name_i]) < mean(new_df[j]):
                            win_number += 1
            print(name_i+"(win): "+str(win_number))
        print("****************************************************************************\n")
    
    
    print("IMPROVEMENT BEST-CASE SCENARIO")
    print("****************************************************************************")
    name_flt = ["tarantula_best_best", "ochiai_best_best", "op2_best_best", "barinel_best_best", "dstar_best_best"]
    temp_value = [0,0,0,0,0,0]
    best_cases_result = {}
    FLT_1 = df['tarantula_rank_best'].tolist()
    FLT_2 = df['ochiai_rank_best'].tolist()
    FLT_3 = df['op2_rank_best'].tolist()
    FLT_4 = df['barinel_rank_best'].tolist()
    FLT_5 = df['dstar_rank_best'].tolist()
    all_flt = {'tarantula': FLT_1, 'ochiai': FLT_2, 'op2':FLT_3, 'barinel':FLT_4, 'dstar':FLT_5}
    for key_i in all_flt:
        temp_value = {'tarantula': [0,0,0,0,0,0], 'ochiai': [0,0,0,0,0,0], 'op2':[0,0,0,0,0,0], 'barinel':[0,0,0,0,0,0], 'dstar':[0,0,0,0,0,0]}
        del temp_value[key_i]
        for key,val in enumerate(all_flt[key_i]):
            if val > 200:
                for loop_second in temp_value:
                    if all_flt[loop_second][key] < 200 and all_flt[loop_second][key] > 10:
                        temp_value[loop_second][0] += 1
                    elif all_flt[loop_second][key] <= 10 and all_flt[loop_second][key] > 5:
                        temp_value[loop_second][1] += 1
                    elif all_flt[loop_second][key] <= 5:
                        temp_value[loop_second][2] += 1
            elif val <= 200 and val > 10:
                for loop_second in temp_value:
                    if all_flt[loop_second][key] <= 10 and all_flt[loop_second][key] > 5:
                        temp_value[loop_second][3] += 1
                    elif all_flt[loop_second][key] <= 5:
                        temp_value[loop_second][4] += 1
            elif val <= 10 and val > 5:
                for loop_second in temp_value:
                    if all_flt[loop_second][key] <= 5:
                        temp_value[loop_second][5] += 1
        print(key_i)
        print(temp_value)
        best_cases_result[key_i] = temp_value
    print("****************************************************************************\n")
    
    print("IMPROVEMENT AVERAGE-CASE SCENARIO")
    print("****************************************************************************")
    FLT_1 = df['tarantula_rank_average'].tolist()
    FLT_2 = df['ochiai_rank_average'].tolist()
    FLT_3 = df['op2_rank_average'].tolist()
    FLT_4 = df['barinel_rank_average'].tolist()
    FLT_5 = df['dstar_rank_average'].tolist()
    all_flt = {'tarantula': FLT_1, 'ochiai': FLT_2, 'op2':FLT_3, 'barinel':FLT_4, 'dstar':FLT_5}
    average_cases_result = {}
    for key_i in all_flt:
        temp_value = best_cases_result[key_i]
        for key,val in enumerate(all_flt[key_i]):
            if val > 200:
                for loop_second in temp_value:
                    if all_flt[loop_second][key] < 200 and all_flt[loop_second][key] > 10:
                        temp_value[loop_second][0] += 1
                    elif all_flt[loop_second][key] <= 10 and all_flt[loop_second][key] > 5:
                        temp_value[loop_second][1] += 1
                    elif all_flt[loop_second][key] <= 5:
                        temp_value[loop_second][2] += 1
            elif val <= 200 and val > 10:
                for loop_second in temp_value:
                    if all_flt[loop_second][key] <= 10 and all_flt[loop_second][key] > 5:
                        temp_value[loop_second][3] += 1
                    elif all_flt[loop_second][key] <= 5:
                        temp_value[loop_second][4] += 1
            elif val <= 10 and val > 5:
                for loop_second in temp_value:
                    if all_flt[loop_second][key] <= 5:
                        temp_value[loop_second][5] += 1
        print(key_i)
        print(temp_value)    
        average_cases_result[key_i] = temp_value
    print("****************************************************************************\n")

    print("IMPROVEMENT WORST-CASE SCENARIO")
    print("****************************************************************************")
    FLT_1 = df['tarantula_rank_worst'].tolist()
    FLT_2 = df['ochiai_rank_worst'].tolist()
    FLT_3 = df['op2_rank_worst'].tolist()
    FLT_4 = df['barinel_rank_worst'].tolist()
    FLT_5 = df['dstar_rank_worst'].tolist()
    all_flt = {'tarantula': FLT_1, 'ochiai': FLT_2, 'op2':FLT_3, 'barinel':FLT_4, 'dstar':FLT_5}
    for key_i in all_flt:
        temp_value = average_cases_result[key_i]
        for key,val in enumerate(all_flt[key_i]):
            if val > 200:
                for loop_second in temp_value:
                    if all_flt[loop_second][key] < 200 and all_flt[loop_second][key] > 10:
                        temp_value[loop_second][0] += 1
                    elif all_flt[loop_second][key] <= 10 and all_flt[loop_second][key] > 5:
                        temp_value[loop_second][1] += 1
                    elif all_flt[loop_second][key] <= 5:
                        temp_value[loop_second][2] += 1
            elif val <= 200 and val > 10:
                for loop_second in temp_value:
                    if all_flt[loop_second][key] <= 10 and all_flt[loop_second][key] > 5:
                        temp_value[loop_second][3] += 1
                    elif all_flt[loop_second][key] <= 5:
                        temp_value[loop_second][4] += 1
            elif val <= 10 and val > 5:
                for loop_second in temp_value:
                    if all_flt[loop_second][key] <= 5:
                        temp_value[loop_second][5] += 1
        print(key_i)
        print(temp_value)
    print("****************************************************************************\n")    

    #for i, name_i in enumerate(name_flt):
    #    win_number = 0
    #    temp = name_flt.copy()
    #    del temp[i]
    #    for j in temp:
    #        temp_pvalue = stats.ranksums(df[name_i],df[j]).pvalue
    #        print(temp_pvalue)
    #        if temp_pvalue < 0.05:
    #            if mean(df[name_i]) < mean(df[j]):
    #                win_number += 1
    #    print(win_number)

    for scen in ["best", "average", "worst"]:
        print("IMPROVEMENT "+scen+"-CASE SCENARIO SIGNIFICANT TEST")
        print("****************************************************************************")
        temp_value = [0,0,0,0,0,0]
        best_cases_result = {}
        FLT_1 = df['tarantula_rank_'+scen].tolist()
        FLT_2 = df['ochiai_rank_'+scen].tolist()
        FLT_3 = df['op2_rank_'+scen].tolist()
        FLT_4 = df['barinel_rank_'+scen].tolist()
        FLT_5 = df['dstar_rank_'+scen].tolist()
        all_flt = {'tarantula': FLT_1, 'ochiai': FLT_2, 'op2':FLT_3, 'barinel':FLT_4, 'dstar':FLT_5}
        for key_i in all_flt:
            temp_value = {'tarantula': [0,0,0,0,0,0], 'ochiai': [0,0,0,0,0,0], 'op2':[0,0,0,0,0,0], 'barinel':[0,0,0,0,0,0], 'dstar':[0,0,0,0,0,0]}
            del temp_value[key_i]
            flt_comp_1 = []
            flt_comp_2 = {'tarantula': [], 'ochiai': [], 'op2':[], 'barinel':[], 'dstar':[]}
            del flt_comp_2[key_i]
            for key,val in enumerate(all_flt[key_i]):
                if val > 200:
                    flt_comp_1.append(val)
                    for loop_second in temp_value:
                        if all_flt[loop_second][key] < 200 and all_flt[loop_second][key] > 10:
                            temp_value[loop_second][0] += 1
                            flt_comp_2[loop_second].append(all_flt[loop_second][key])
                        elif all_flt[loop_second][key] <= 10 and all_flt[loop_second][key] > 5:
                            temp_value[loop_second][1] += 1
                            flt_comp_2[loop_second].append(all_flt[loop_second][key])
                        elif all_flt[loop_second][key] <= 5:
                            temp_value[loop_second][2] += 1
                            flt_comp_2[loop_second].append(all_flt[loop_second][key])
                elif val <= 200 and val > 10:
                    flt_comp_1.append(val)
                    for loop_second in temp_value:
                        if all_flt[loop_second][key] <= 10 and all_flt[loop_second][key] > 5:
                            temp_value[loop_second][3] += 1
                            flt_comp_2[loop_second].append(all_flt[loop_second][key])
                        elif all_flt[loop_second][key] <= 5:
                            temp_value[loop_second][4] += 1
                            flt_comp_2[loop_second].append(all_flt[loop_second][key])
                elif val <= 10 and val > 5:
                    flt_comp_1.append(val)
                    for loop_second in temp_value:
                        if all_flt[loop_second][key] <= 5:
                            temp_value[loop_second][5] += 1
                            flt_comp_2[loop_second].append(all_flt[loop_second][key])
            for loop_second in temp_value:
                print(key_i+" VS "+loop_second)
                print(stats.ranksums(flt_comp_1,flt_comp_2[loop_second]))
                #print(cliffsDelta(flt_comp_1,flt_comp_2[loop_second]))
            print(key_i)
            print(temp_value)
            best_cases_result[key_i] = temp_value
        print("****************************************************************************\n")    





if len(sys.argv) > 1:
    filename = sys.argv[1]
    colnames=['project', 'line', 
    'tarantula_best_best', 
    'tarantula_worst_best',
    'tarantula_average_best',
    'ochiai_best_best',
    'ochiai_worst_best',
    'ochiai_average_best',
    'op2_best_best',
    'op2_worst_best',
    'op2_average_best',
    'barinel_best_best',
    'barinel_worst_best',
    'barinel_average_best',
    'dstar_best_best',
    'dstar_worst_best',
    'dstar_average_best',
    'tarantula_rank_best', 'ochiai_rank_best', 'op2_rank_best', 'barinel_rank_best', 'dstar_rank_best',
    'tarantula_rank_average', 'ochiai_rank_average', 'op2_rank_average', 'barinel_rank_average', 'dstar_rank_average',
    'tarantula_rank_worst', 'ochiai_rank_worst', 'op2_rank_worst', 'barinel_rank_worst', 'dstar_rank_worst',
    'tarantula_rank_flt', 'ochiai_rank_flt', 'op2_rank_flt', 'barinel_rank_flt', 'dstar_rank_flt','tarantula_rank_flt_worst', 'ochiai_rank_flt_worst', 'op2_rank_flt_worst', 'barinel_rank_flt_worst', 'dstar_rank_flt_worst',
    'tarantula_rank_flt_average', 'ochiai_rank_flt_average', 'op2_rank_flt_average', 'barinel_rank_flt_average', 'dstar_rank_flt_average']
    df = pd.read_csv(filename,sep=';', names=colnames, header=0) 
else:
    filename = "combine-cur.txt"
    colnames=['project', 'line', 
    'tarantula_best_best', 'tarantula_best_average', 'tarantula_best_worst', 
    'tarantula_worst_best','tarantula_worst_worst','tarantula_worst_average',
    'tarantula_average_best','tarantula_average_worst','tarantula_average_average',
    'ochiai_best_best', 'ochiai_best_average', 'ochiai_best_worst', 
    'ochiai_worst_best','ochiai_worst_worst','ochiai_worst_average',
    'ochiai_average_best','ochiai_average_worst','ochiai_average_average',
    'op2_best_best', 'op2_best_average', 'op2_best_worst', 
    'op2_worst_best','op2_worst_worst','op2_worst_average',
    'op2_average_best','op2_average_worst','op2_average_average',
    'barinel_best_best', 'barinel_best_average', 'barinel_best_worst', 
    'barinel_worst_best','barinel_worst_worst','barinel_worst_average',
    'barinel_average_best','barinel_average_worst','barinel_average_average',
    'dstar_best_best', 'dstar_best_average', 'dstar_best_worst', 
    'dstar_worst_best','dstar_worst_worst','dstar_worst_average',
    'dstar_average_best','dstar_average_worst','dstar_average_average',
    'tarantula_rank_best', 'ochiai_rank_best', 'op2_rank_best', 'barinel_rank_best', 'dstar_rank_best',
    'tarantula_rank_average', 'ochiai_rank_average', 'op2_rank_average', 'barinel_rank_average', 'dstar_rank_average',
    'tarantula_rank_worst', 'ochiai_rank_worst', 'op2_rank_worst', 'barinel_rank_worst', 'dstar_rank_worst',
    'tarantula_rank_flt', 'ochiai_rank_flt', 'op2_rank_flt', 'barinel_rank_flt', 'dstar_rank_flt',
    ] 
    df = pd.read_csv(filename,sep=';', names=colnames, header=None) 

for filter in [2,6,10,14,15,17,18,23]:
    i = df[((df.project == 'black') & ( df.line == filter))].index
    df = df.drop(i)

single = pd.read_csv('single_line_without omission.txt', sep=' ')
multi_without = pd.read_csv('multiple_line_without_omission.txt', sep=' ')

d4j = pd.read_csv('Defects4j_results/combine_exam_sbfl.txt',sep='\t')
bugsinpy_loop = ['_best_best', '_average_best', '_worst_best']
d4j_loop = ['exam_best_case_f', 'exam_average_case_f', 'exam_worst_case_f']
print_d4j_loop = ["EXAM BEST-CASE SCENARIO", "EXAM AVERAGE-CASE SCENARIO", "EXAM WORST-CASE SCENARIO"]

print("----------------------------------------------------------------")
print("RQ-1")

for na, b_loop in enumerate(bugsinpy_loop):
    print(print_d4j_loop[na])
    print("****************************************************************************")
    print("OCHIAI BUGSINPY vs DEFECTS4J")    
    print(stats.ranksums(df['ochiai'+b_loop],d4j[d4j.formula == 'ochiai'][d4j_loop[na]]))
    print(cliffsDelta(df['ochiai'+b_loop],d4j[d4j.formula == 'ochiai'][d4j_loop[na]]))
    print("Tarantula BUGSINPY vs DEFECT4J")
    print(stats.ranksums(df['tarantula'+b_loop],d4j[d4j.formula == 'tarantula'][d4j_loop[na]]))
    print(cliffsDelta(df['tarantula'+b_loop],d4j[d4j.formula == 'tarantula'][d4j_loop[na]]))
    print("Barinel BUGSINPY vs DEFECT4J")
    print(stats.ranksums(df['barinel'+b_loop],d4j[d4j.formula == 'barinel'][d4j_loop[na]]))
    print(cliffsDelta(df['barinel'+b_loop],d4j[d4j.formula == 'barinel'][d4j_loop[na]]))
    print("OP2 BUGSINPY vs DEFECT4J")
    print(stats.ranksums(df['op2'+b_loop],d4j[d4j.formula == 'opt2'][d4j_loop[na]]))
    print(cliffsDelta(df['op2'+b_loop],d4j[d4j.formula == 'opt2'][d4j_loop[na]]))
    print("DSTAR BUGSINPY vs DEFECT4J")
    print(stats.ranksums(df['dstar'+b_loop],d4j[d4j.formula == 'dstar2'][d4j_loop[na]]))
    print(cliffsDelta(df['dstar'+b_loop],d4j[d4j.formula == 'dstar2'][d4j_loop[na]]))
    print("****************************************************************************\n")

d4j = pd.read_csv('Defects4j_results/combine_sbfl.txt',sep='\t')
bugsinpy_loop = ['_rank_best', '_rank_average', '_rank_worst']
d4j_loop = ['rank_best_case', 'rank_average_case', 'rank_worst_case']
print_d4j_loop = ["TOP-K BEST-CASE SCENARIO", "TOP-K AVERAGE-CASE SCENARIO", "TOP-K WORST-CASE SCENARIO"]
for na, b_loop in enumerate(bugsinpy_loop):
    print(print_d4j_loop[na])
    print("****************************************************************************")
    print("OCHIAI BUGSINPY vs DEFECTS4J")    
    print(stats.ranksums(df['ochiai'+b_loop],d4j[d4j.formula == 'ochiai'][d4j_loop[na]]))
    print(cliffsDelta(df['ochiai'+b_loop],d4j[d4j.formula == 'ochiai'][d4j_loop[na]]))
    print("Tarantula BUGSINPY vs DEFECT4J")
    print(stats.ranksums(df['tarantula'+b_loop],d4j[d4j.formula == 'tarantula'][d4j_loop[na]]))
    print(cliffsDelta(df['tarantula'+b_loop],d4j[d4j.formula == 'tarantula'][d4j_loop[na]]))
    print("barinel BUGSINPY vs DEFECT4J")
    print(stats.ranksums(df['barinel'+b_loop],d4j[d4j.formula == 'barinel'][d4j_loop[na]]))
    print(cliffsDelta(df['barinel'+b_loop],d4j[d4j.formula == 'barinel'][d4j_loop[na]]))
    print("OP2 BUGSINPY vs DEFECT4J")
    print(stats.ranksums(df['op2'+b_loop],d4j[d4j.formula == 'opt2'][d4j_loop[na]]))
    print(cliffsDelta(df['op2'+b_loop],d4j[d4j.formula == 'opt2'][d4j_loop[na]]))
    print("DSTAR BUGSINPY vs DEFECT4J")
    print(stats.ranksums(df['dstar'+b_loop],d4j[d4j.formula == 'dstar2'][d4j_loop[na]]))
    print(cliffsDelta(df['dstar'+b_loop],d4j[d4j.formula == 'dstar2'][d4j_loop[na]]))
    print("****************************************************************************\n")
print("----------------------------------------------------------------\n\n")


print("----------------------------------------------------------------")
print("RQ-2")
print("ALL")
getting_all(df)

keys = list(single.columns.values)
i1 = df.set_index(keys).index
i2 = single.set_index(keys).index
single_line = df[i1.isin(i2)]
multiple_line = df[~i1.isin(i2)]
keys = list(multi_without.columns.values)
i1 = df.set_index(keys).index
i2 = multi_without.set_index(keys).index
multiple_line_without = df[i1.isin(i2)]

# print(single_line)
# print(multiple_line)
# print(multiple_line_without)
print("\n\n TYPE OF FAULTS")
print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
print("SINGLE-LINE WITHOUT OMISSION")
getting_all(single_line)

print("MULTIPLE-LINE WITHOUT OMISSION")
getting_all(multiple_line_without)

print("MULTIPLE-LINE WITH OMISSION")
getting_all(multiple_line)
print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")







    
    
print("----------------------------------------------------------------\n\n")


print("----------------------------------------------------------------")
print("RQ-3")
print("EXAM BEST-CASE SCENARIO")
print("****************************************************************************")
print("OCHIAI > TARANTULA")
print(stats.ranksums(df['ochiai_best_best'],df['tarantula_best_best']))
print(cliffsDelta(df['ochiai_best_best'],df['tarantula_best_best']))
print("BARINEL > OCHIAI")
print(stats.ranksums(df['barinel_best_best'],df['ochiai_best_best']))
print(cliffsDelta(df['barinel_best_best'],df['ochiai_best_best']))
print("BARINEL > TARANTULA")
print(stats.ranksums(df['barinel_best_best'],df['tarantula_best_best']))
print(cliffsDelta(df['barinel_best_best'],df['tarantula_best_best']))
print("OP2 > OCHIAI")
print(stats.ranksums(df['op2_best_best'],df['ochiai_best_best']))
print(cliffsDelta(df['op2_best_best'],df['ochiai_best_best']))
print("OP2 > TARANTULA")
print(stats.ranksums(df['op2_best_best'],df['tarantula_best_best']))
print(cliffsDelta(df['op2_best_best'],df['tarantula_best_best']))
print("DSTAR > OCHIAI")
print(stats.ranksums(df['dstar_best_best'],df['ochiai_best_best']))
print(cliffsDelta(df['dstar_best_best'],df['ochiai_best_best']))
print("DSTAR > TARANTULA")
print(stats.ranksums(df['dstar_best_best'],df['tarantula_best_best']))
print(cliffsDelta(df['dstar_best_best'],df['tarantula_best_best']))
print("****************************************************************************\n")

print("EXAM AVERAGE-CASE SCENARIO")
print("****************************************************************************")
print("OCHIAI > TARANTULA")
print(stats.ranksums(df['ochiai_average_best'],df['tarantula_average_best']))
print(cliffsDelta(df['ochiai_average_best'],df['tarantula_average_best']))
print("BARINEL > OCHIAI")
print(stats.ranksums(df['barinel_average_best'],df['ochiai_average_best']))
print(cliffsDelta(df['barinel_average_best'],df['ochiai_average_best']))
print("BARINEL > TARANTULA")
print(stats.ranksums(df['barinel_average_best'],df['tarantula_average_best']))
print(cliffsDelta(df['barinel_average_best'],df['tarantula_average_best']))
print("OP2 > OCHIAI")
print(stats.ranksums(df['op2_average_best'],df['ochiai_average_best']))
print(cliffsDelta(df['op2_average_best'],df['ochiai_average_best']))
print("OP2 > TARANTULA")
print(stats.ranksums(df['op2_average_best'],df['tarantula_average_best']))
print(cliffsDelta(df['op2_average_best'],df['tarantula_average_best']))
print("DSTAR > OCHIAI")
print(stats.ranksums(df['dstar_average_best'],df['ochiai_average_best']))
print(cliffsDelta(df['dstar_average_best'],df['ochiai_average_best']))
print("DSTAR > TARANTULA")
print(stats.ranksums(df['dstar_average_best'],df['tarantula_average_best']))
print(cliffsDelta(df['dstar_average_best'],df['tarantula_average_best']))
print("****************************************************************************\n")

print("EXAM WORST-CASE SCENARIO")
print("****************************************************************************")
print("OCHIAI > TARANTULA")
print(stats.ranksums(df['ochiai_worst_best'],df['tarantula_worst_best']))
print(cliffsDelta(df['ochiai_worst_best'],df['tarantula_worst_best']))
print("BARINEL > OCHIAI")
print(stats.ranksums(df['barinel_worst_best'],df['ochiai_worst_best']))
print(cliffsDelta(df['barinel_worst_best'],df['ochiai_worst_best']))
print("BARINEL > TARANTULA")
print(stats.ranksums(df['barinel_worst_best'],df['tarantula_worst_best']))
print(cliffsDelta(df['barinel_worst_best'],df['tarantula_worst_best']))
print("OP2 > OCHIAI")
print(stats.ranksums(df['op2_worst_best'],df['ochiai_worst_best']))
print(cliffsDelta(df['op2_worst_best'],df['ochiai_worst_best']))
print("OP2 > TARANTULA")
print(stats.ranksums(df['op2_worst_best'],df['tarantula_worst_best']))
print(cliffsDelta(df['op2_worst_best'],df['tarantula_worst_best']))
print("DSTAR > OCHIAI")
print(stats.ranksums(df['dstar_worst_best'],df['ochiai_worst_best']))
print(cliffsDelta(df['dstar_worst_best'],df['ochiai_worst_best']))
print("DSTAR > TARANTULA")
print(stats.ranksums(df['dstar_worst_best'],df['tarantula_worst_best']))
print(cliffsDelta(df['dstar_worst_best'],df['tarantula_worst_best']))
print("****************************************************************************\n")
print("----------------------------------------------------------------\n\n")

