import os                                                                                                             
import csv
from pathlib import Path
import math
from scipy.stats import rankdata
import sys
from ast import literal_eval
import pandas as pd


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
	prev_temp = -10
	print(temp_flt)
	for key, value in temp_flt.items():
		if prev_temp == -10:
			prev_temp = value
		else:
			if prev_temp != value:
				m += 1
			prev_temp = value
		add_to_array[key] = m
		# m += 1
	temp_array.extend(add_to_array)

	sort_flt = {0: temp_tarantula[-1], 1: temp_ochiai[-1], 2: temp_op2[-1], 3: temp_barinel[-1], 4: temp_dstar[-1]}
	temp_flt = {k: v for k, v in sorted(sort_flt.items(), key=lambda item: item[1])}
	m = 1
	add_to_array = [0,0,0,0,0]
	prev_temp = -10
	print(temp_flt)
	for key, value in temp_flt.items():
		if prev_temp == -10:
			prev_temp = value
		else:
			if prev_temp != value:
				m += 1
			prev_temp = value
		add_to_array[key] = m
		# m += 1
	temp_array.extend(add_to_array)
	sort_flt = {0: temp_tarantula[int(len(temp_tarantula_rank)/2)], 1: temp_ochiai[int(len(temp_ochiai_rank)/2)], 2: temp_op2[int(len(temp_op2_rank)/2)], 3: temp_barinel[int(len(temp_barinel_rank)/2)], 4: temp_dstar[int(len(temp_dstar_rank)/2)]}
	temp_flt = {k: v for k, v in sorted(sort_flt.items(), key=lambda item: item[1])}
	m = 1
	add_to_array = [0,0,0,0,0]
	prev_temp = -10
	print(temp_flt)
	for key, value in temp_flt.items():
		if prev_temp == -10:
			prev_temp = value
		else:
			if prev_temp != value:
				m += 1
			prev_temp = value
		add_to_array[key] = m
		# m += 1
	temp_array.extend(add_to_array)
	
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
								