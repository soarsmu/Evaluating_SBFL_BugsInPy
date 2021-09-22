"""Major section for pytest pinpoint plugin"""

from coverage.data import CoverageData
from scipy.stats import rankdata

import coverage
import os
import sys
import math
import pytest
import time
from tqdm import tqdm



def pytest_addoption(parser):
    group = parser.getgroup("pinpoint")
    group.addoption(
        "--pinpoint",
        action="store_true",
        help="pytest-pinpoint help \n--pinpoint: run SBFL techniques to localize bug",
    )



def new_rank(data, key):
    return rankdata([float(-1) * data[x][key] for x in range(len(data))], method='average')
    


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    # collect pass fail stats
    #print(terminalreporter.stats.values())
    print("PART 1 - COLLECT FILES")
    start_time = time.time()
    terminalreporter.section('Pytest PinPoint')
    failures = {}
    for report in terminalreporter.stats.get('failed', []):
        failures[report.nodeid] = [[], []]
    passes = {}
    for report in terminalreporter.stats.get('passed', []):
        passes[report.nodeid] = [[], []]


    f = open("bugsinpy-sbfl-failures.txt", "w")
    f.write(str(list(failures.keys())))
    f.close()

    f = open("bugsinpy-sbfl-passes.txt", "w")
    f.write(str(list(passes.keys())))
    f.close()
    
    # connect to the database
    covdb = coverage.CoverageData()
    covdb.read()
    storage = []
    # Collect measured_files
    print("--- %.2f seconds ---" % (time.time() - start_time))
    start_time = time.time()
    
    total_exc_all = 0
    measured_files = covdb.measured_files()
    print("PART 2 - GET THE COVERAGE")

    start_time = time.time()
    print(len(measured_files))
    for measured_f in tqdm(measured_files):
      if "/env/" not in measured_f:    
        current_context = covdb.contexts_by_lineno(measured_f)
        # not consider files which are not tested
        if current_context is [] or current_context is None:
            measured_files.remove(measured_f)
        else:
            total_exc_all += len(covdb.lines(measured_f))
            # store pass/fail stats associated with context and line number
            for key, value in covdb.contexts_by_lineno(measured_f).items():
                if value is not ['']:
                    for context in value:
                        temp_context = context.split("|")
                        if temp_context[0] in failures:
                            failures[temp_context[0]][0].append(abs(key))
                            failures[temp_context[0]][1].append(measured_f)
                        if temp_context[0] in passes:
                            passes[temp_context[0]][0].append(abs(key))
                            passes[temp_context[0]][1].append(measured_f)
    print("--- %.2f seconds ---" % (time.time() - start_time))
    
    files = {}

    print("PART 3 - COUNT THE PASS AND FAIL")

    start_time = time.time()
    totalfailed_num = 0
    totalpassed_num = 0
    # Count pass/faill information associated with line
    for failed_context in failures:
        for index, line in enumerate(failures[failed_context][0]):
            totalfailed_num += 1
            if failures[failed_context][1][index] in files:
                if line in files[failures[failed_context][1][index]]:
                    files[failures[failed_context][1][index]][line]["failed"] += 1
                else:
                    files[failures[failed_context][1][index]][line] = {"failed": 1, "passed":0}
            else:
               files[failures[failed_context][1][index]] = {line: {"failed": 1, "passed": 0}}

    for passed_context in passes:
        for index, line in enumerate(passes[passed_context][0]):
            totalpassed_num += 1
            if passes[passed_context][1][index] in files:
                if line in files[passes[passed_context][1][index]]:
                    files[passes[passed_context][1][index]][line]["passed"] += 1
                else:
                    files[passes[passed_context][1][index]][line] = {"failed": 0, "passed":1}
            else:
               files[passes[passed_context][1][index]] = {line: {"failed": 0, "passed": 1}}
               
    # Count total numbers of passes and fails
    print("--- %.2f seconds ---" % (time.time() - start_time))
    
    start_time = time.time()
    print("PART 4 - SBFL TECHNIQUES")
    file_scores = []
    for key in files:
        for line in files[key]:
            line_info = files[key][line]
            if totalfailed_num == 0 or totalpassed_num == 0:
                new_tarantula = 0
            else:
                new_tarantula = (line_info["failed"] / totalfailed_num) / ((line_info["failed"] / totalfailed_num) + (line_info["passed"] / totalpassed_num))
            if totalfailed_num == 0:
                new_ochiai = 0
            else:
                new_ochiai = (line_info["failed"] / math.sqrt(totalfailed_num * (line_info["failed"] + line_info["passed"])))
            new_op2 = line_info["failed"] - (line_info["passed"] / (totalpassed_num + 1))
            if new_op2 < 0:
                new_op2 = 0
            new_barinel = 1 - (line_info["passed"] / (line_info["failed"] + line_info["passed"]))
            new_dstar = line_info["failed"] ** 2 / (line_info["passed"] + (totalfailed_num - line_info["failed"]))
            file_scores.append({"file":key,"line":line,"passed":line_info["passed"],"failed":line_info["failed"],"total":total_exc_all,"new_tarantula":new_tarantula,"new_ochiai":new_ochiai,"new_op2":new_op2,"new_barinel":new_barinel,"new_dstar":new_dstar})
    # print(file_scores)
    del files

    print("--- %.2f seconds ---" % (time.time() - start_time))
    print("PART 5 - WRITE IN FILE")

    start_time = time.time()
    cwd = os.getcwd()+"-fault_localization.txt"
    f= open(cwd,"w+")
    Tarantula_rank = new_rank(file_scores, "new_tarantula")
    Ochiai_rank = new_rank(file_scores, "new_ochiai")
    Op2_rank = new_rank(file_scores, "new_op2")
    Barinel_rank = new_rank(file_scores, "new_barinel")
    DStar_rank = new_rank(file_scores, "new_dstar")
    for count, line_score in enumerate(file_scores):
        line_score["Tarantula_rank"] = Tarantula_rank[count]
        line_score["Tarantula_exam"] = Tarantula_rank[count] / line_score["total"]
        line_score["Ochiai_rank"] = Ochiai_rank[count]
        line_score["Ochiai_exam"] = Ochiai_rank[count] / line_score["total"]
        line_score["Op2_rank"] = Op2_rank[count]
        line_score["Op2_exam"] = Op2_rank[count] / line_score["total"]
        line_score["Barinel_rank"] = Barinel_rank[count]
        line_score["Barinel_exam"] = Barinel_rank[count] / line_score["total"]
        line_score["DStar_rank"] = DStar_rank[count]
        line_score["DStar_exam"] = DStar_rank[count] / line_score["total"]

    #terminalreporter.section('Pytest PinPoint-Show All')
    #f.write("FAULT LOCALIZATION SHOW ALL\n")
    for line_score in file_scores:
        f.write("___________________\n")
        f.write("File: %s\n" % line_score.get("file"))
        f.write("Line: %d\n" % line_score.get("line"))
        f.write("TOTAL_NUM_ALL: %d\n" % total_exc_all)
        f.write("Tarantula_rank num: %d\n" % line_score.get("Tarantula_rank"))
        f.write("Tarantula_exam num: %f\n" % line_score.get("Tarantula_exam"))
        f.write("Ochiai_rank num: %d\n" % line_score.get("Ochiai_rank"))
        f.write("Ochiai_exam num: %f\n" % line_score.get("Ochiai_exam"))
        f.write("Op2_rank num: %d\n" % line_score.get("Op2_rank"))
        f.write("Op2_exam num: %f\n" % line_score.get("Op2_exam"))
        f.write("Barinel_rank num: %d\n" % line_score.get("Barinel_rank"))
        f.write("Barinel_exam num: %f\n" % line_score.get("Barinel_exam"))
        f.write("Dstar_rank num: %d\n" % line_score.get("DStar_rank"))
        f.write("Dstar_exam num: %f\n" % line_score.get("DStar_exam"))
    f.close()     
    print("--- %.2f seconds ---" % (time.time() - start_time))
