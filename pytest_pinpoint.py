"""Major section for pytest pinpoint plugin"""

from coverage.data import CoverageData
from scipy.stats import rankdata

import coverage
import os
import sys
import math
import pytest



def pytest_addoption(parser):
    """Create --pinpoint option to run the plugin"""
    group = parser.getgroup("pinpoint")
    group.addoption(
        "--pinpoint",
        action="store_true",
        help="pytest-pinpoint help \n--pinpoint: analyze branch coverage to detect faults, show top three ranked results \n--show_all: show all ranked results \n--show_last_three: show bottom three ranked results",
    )
    group.addoption(
        "--show_all",
        action="store_true",
    )
    group.addoption(
        "--show_last_three",
        action="store_true",
    )


def rank(data, key):
    """Rank function used to rank SBFL scores"""
    ranks = [x+1 for x in range(len(data))]
    return sorted(ranks, reverse=True, key=lambda x:float(data[x-1][key]))
    
def new_rank(data, key):
    return rankdata([float(-1) * data[x][key] for x in range(len(data))], method='dense')
	


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Generate terminal report for pytest-pinpoint"""
    # collect pass fail stats
    terminalreporter.section('Pytest PinPoint')
    failures = [[report.nodeid, [], []]
                for report in terminalreporter.stats.get('failed', [])]
    passes = [[report.nodeid, [], []]
                for report in terminalreporter.stats.get('passed', [])]
    #print("failed ", len(failures), "times", failures)
    #print("passed ", len(passes), "times", passes)
    # connect to the database
    covdb = coverage.CoverageData()
    covdb.read()
    storage = []
    # Collect measured_files
    measured_files = covdb.measured_files()
    for measured_f in measured_files:
      if "/env/" not in measured_f:	   
        #print("MEASURED F", measured_f)
        current_context = covdb.contexts_by_lineno(measured_f)
        #print("CONTEXT BY LINE", current_context)
        # not consider files which are not tested
        if current_context is [] or current_context is None:
            measured_files.remove(measured_f)
        else:
            # store pass/fail stats associated with context and line number
            for key, value in covdb.contexts_by_lineno(measured_f).items():
                if value is not ['']:
                    for context in value:
                        for failed_context in failures:
                            if failed_context[0] in context:
                                failed_context[1].append(abs(key))
                                failed_context[2].append(measured_f)
#                                if measured_f not in failed_context[2]:
#                                    failed_context[2].append(measured_f)
                        for passed_context in passes:
                            if passed_context[0] in context:
                                passed_context[1].append(abs(key))
                                passed_context[2].append(measured_f)
                     #           if measured_f not in passed_context[2]:
                      #              passed_context[2].append(measured_f)
    #print("failures")
    #print(failures)
    #print("passes")
    #print(passes)
    # Link tested files to contexts information
    files = []
    for context in failures:
        file_name = context[0].split('::')[0]
        file_name = file_name.split('test_')[-1]
        if not any(file_name in file for file in files):
            files.append([file_name])
    for context in passes:
        file_name = context[0].split('::')[0]
        file_name = file_name.split('test_')[-1]
        if not any(file_name in file for file in files):
            files.append([file_name])
    #print("FILE", files)
    # Count pass/faill information associated with line
    for file in files:
        for failed_context in failures:
            if file[0] in failed_context[0].split('::')[0]:
                #print("FILE IN FAILURES", file[0], failed_context[0])
                for index, line in enumerate(failed_context[1]):
                    if not any(line_info["line"] == line for line_info in file[1:]):
                        file.append({"file": failed_context[2][index], "line": line, "failed times": 1, "passed times": 0})
                    else:
                        for line_info in file[1:]:
                            if line_info["line"] is line:
                                line_info["failed times"] += 1
    #print("DOOOONEEE")
    for file in files:
        for passed_context in passes:
            if file[0] in passed_context[0].split('::')[0]:
                for index, line in enumerate(passed_context[1]):
                    if not any(line_info["line"] == line for line_info in file[1:]):
                        file.append({"file": passed_context[2][index], "line": line, "failed times": 0, "passed times": 1})
                    else:
                        for line_info in file[1:]:
                            if line_info["line"] is line:
                                line_info["passed times"] += 1
    # Count total numbers of passes and fails
    totalfailed_num = 0
    totalpassed_num = 0
    #print("GEEET")
    for file in files:
        #print(file)
        for line_info in file[1:]:
            totalfailed_num += line_info.get("failed times")
            totalpassed_num += line_info.get("passed times")
    # Calculate SBFL Scores
    #print("DONEEEEEE")
    scores = []
    for file in files:
        #print(file)
        file_scores = []
        
        tes_file=file[0].replace("/", "\\")
        # print("——————————————————————————")
        # Count total executed lines in a file
        for measured_file in measured_files:
            if file[0] in measured_file:
                totalnum = len(covdb.lines(measured_file))
            elif tes_file in measured_file:
                totalnum = len(covdb.lines(measured_file))
        # Calculate scores for each line
        for line_info in file[1:]:
            #print("File:", line_info["file"])
            #print("Line:", line_info["line"])
            total_times = 0
            total_times = line_info["passed times"] + line_info["failed times"]
            #print("Failed:", line_info["failed times"])
            #print("Passed:", line_info["passed times"])
            # print("Tested:", total_times)
            if totalfailed_num == 0 or totalpassed_num == 0:
                Tarantula = 0
            else:
                Tarantula = (line_info["failed times"] / totalfailed_num) / ((line_info["failed times"] / totalfailed_num) + (line_info["passed times"] / totalpassed_num))
            # print("Tarantula Score:", Tarantula)
            if totalfailed_num == 0:
                Ochiai = 0
            else:
                Ochiai = (line_info["failed times"] / math.sqrt(totalfailed_num * total_times))
            # print("Ochiai Score:",Ochiai)
            Op2 = line_info["failed times"] - line_info["passed times"] / (totalpassed_num + 1)
            if Op2 > 0:
                Op2 = Op2
                # print("Op2 Score", Op2)
            else:
                Op2 = 0
                # print("Op2 Score", Op2)
            Barinel = 1 - line_info["passed times"] / total_times
            # print("Barinel Score", Barinel)
            DStar = line_info["failed times"] ** 2 / (line_info["passed times"] + totalfailed_num - line_info["failed times"])
            # print("DStar Score", DStar)
            # print("——————————————————————————")
            file_scores.append({"total": totalnum, "file": line_info["file"], "test": file[0], "line": line_info["line"], "passed times": line_info["passed times"], "failed times": line_info["failed times"], "Tarantula": Tarantula, "Ochiai": Ochiai, "Op2": Op2, "Barinel": Barinel, "DStar": DStar})
        scores.append(file_scores)
    # Rank scores
    cwd = os.getcwd()+"\\Fault_localization.txt"
    f= open(cwd,"w+")
    for file_scores in scores:
        Tarantula_rank = new_rank(file_scores, "Tarantula")
        Ochiai_rank = new_rank(file_scores, "Ochiai")
        #print(Ochiai_rank)
        Op2_rank = new_rank(file_scores, "Op2")
        Barinel_rank = new_rank(file_scores, "Barinel")
        DStar_rank = new_rank(file_scores, "DStar")
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
        if config.getoption("show_all"):
            terminalreporter.section('Pytest PinPoint-Show All')
            f.write("FAULT LOCALIZATION SHOW ALL\n")
            terminalreporter.section(file_scores[0]["test"], sep='-', blue=True, bold=True)
            f.write(file_scores[0]["test"])
            f.write("\n")
            #file_scores.sort(key=file_scores.get("Tarantula"))
            for line_score in file_scores:
                if line_score.get("Ochiai") != 0:
                    print("___________________")
                    print("File:", line_score.get("file"))
                    print("Line:", line_score.get("line"))
                    print("Passed:", line_score.get("passed times"))
                    print("Failed:", line_score.get("failed times"))
                    print("Tarantula_rank num:", line_score.get("Tarantula_rank"))
                    print("Tarantula_exam num:", line_score.get("Tarantula_exam"))
                    print("Tarantula_score num:", line_score.get("Tarantula"))
                    print("Ochiai_rank num:", line_score.get("Ochiai_rank"))
                    print("Ochiai_exam num:", line_score.get("Ochiai_exam"))
                    print("Ochiai_score num:", line_score.get("Ochiai"))
                    print("Op2_rank num:", line_score.get("Op2_rank"))
                    print("Op2_exam num:", line_score.get("Op2_exam"))
                    print("Op2_score num:", line_score.get("Op2"))
                    print("Barinel_rank num:", line_score.get("Barinel_rank"))
                    print("Barinel_exam num:", line_score.get("Barinel_exam"))
                    print("Barinel_score num:", line_score.get("Barinel"))
                    print("DStar_rank num:", line_score.get("DStar_rank"))
                    print("DStar_exam num:", line_score.get("DStar_exam"))
                    print("DStar_score num:", line_score.get("DStar"))

                f.write("___________________\n")
                f.write("File: %s\n" % line_score.get("file"))
                f.write("Line: %d\n" % line_score.get("line"))
                f.write("Passed: %d\n" % line_score.get("passed times"))
                f.write("Failed: %d\n" % line_score.get("failed times"))
                f.write("Tarantula_rank num: %d\n" % line_score.get("Tarantula_rank"))
                f.write("Tarantula_exam num: %f\n" % line_score.get("Tarantula_exam"))
                f.write("Tarantula_score num: %f\n" % line_score.get("Tarantula"))
                f.write("Ochiai_rank num: %d\n" % line_score.get("Ochiai_rank"))
                f.write("Ochiai_exam num: %f\n" % line_score.get("Ochiai_exam"))
                f.write("Ochiai_score num: %f\n" % line_score.get("Ochiai"))
                f.write("Op2_rank num: %d\n" % line_score.get("Op2_rank"))
                f.write("Op2_exam num: %f\n" % line_score.get("Op2_exam"))
                f.write("Op2_score num: %f\n" % line_score.get("Op2"))
                f.write("Barinel_rank num: %d\n" % line_score.get("Barinel_rank"))
                f.write("Barinel_exam num: %f\n" % line_score.get("Barinel_exam"))
                f.write("Barinel_score num: %f\n" % line_score.get("Barinel"))
                f.write("Dstar_rank num: %d\n" % line_score.get("DStar_rank"))
                f.write("Dstar_exam num: %f\n" % line_score.get("DStar_exam"))
                f.write("Dstar_score num: %f\n" % line_score.get("DStar"))
            
        else:
            terminalreporter.section('Pytest PinPoint-Show Top Three')
            for line_score in file_scores:
                rank_list = [line_score.get("Tarantula_rank"), line_score.get("Ochiai_rank"), line_score.get("Op2_rank"),
                            line_score.get("Barinel_rank"), line_score.get("DStar_rank")]
                if any(rank in (1, 2, 3) for rank in rank_list):
                    print("___________________")
                    print("File:", line_score.get("file"))
                    print("Line:", line_score.get("line"))
                    print("Tarantula_rank num:", line_score.get("Tarantula_rank"))
                    print("Tarantula_exam num:", line_score.get("Tarantula_exam"))
                    print("Ochiai_rank num:", line_score.get("Ochiai_rank"))
                    print("Ochiai_exam num:", line_score.get("Ochiai_exam"))
                    print("Op2_rank num:", line_score.get("Op2_rank"))
                    print("Op2_exam num:", line_score.get("Op2_exam"))
                    print("Barinel_rank num:", line_score.get("Barinel_rank"))
                    print("Barinel_exam num:", line_score.get("Barinel_exam"))
                    print("DStar_rank num:", line_score.get("DStar_rank"))
                    print("DStar_exam num:", line_score.get("DStar_exam"))
            if config.getoption("show_last_three"):
                terminalreporter.section('Pytest PinPoint-Show Bottom Three')
                for line_score in file_scores:
                    rank_list = [line_score.get("Tarantula_rank"), line_score.get("Ochiai_rank"), line_score.get("Op2_rank"),
                                line_score.get("Barinel_rank"), line_score.get("DStar_rank")]
                    if any(rank in (count - 3, count - 2, count - 1) for rank in rank_list):
                        print("___________________")
                        print("File:", line_score.get("file"))
                        print("Line:", line_score.get("line"))
                        print("Tarantula_rank num:", line_score.get("Tarantula_rank"))
                        print("Tarantula_exam num:", line_score.get("Tarantula_exam"))
                        print("Ochiai_rank num:", line_score.get("Ochiai_rank"))
                        print("Ochiai_exam num:", line_score.get("Ochiai_exam"))
                        print("Op2_rank num:", line_score.get("Op2_rank"))
                        print("Op2_exam num:", line_score.get("Op2_exam"))
                        print("Barinel_rank num:", line_score.get("Barinel_rank"))
                        print("Barinel_exam num:", line_score.get("Barinel_exam"))
                        print("DStar_rank num:", line_score.get("DStar_rank"))
                        print("DStar_exam num:", line_score.get("DStar_exam"))
    f.close()     
