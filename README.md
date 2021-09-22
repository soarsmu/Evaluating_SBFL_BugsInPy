# Real World Projects, Real Faults: Evaluating Spectrum Based Fault Localization Techniques on Python Projects
Spectrum Based Fault Localization (SBFL) is a statistical approach to identify faulty code within a program given program spectra (i.e., records of program elements executed by passing and failing test cases). Several SBFL techniques have been proposed over the years, but most evaluations of those techniques were done only on Java and C programs, and frequently involve artificial faults. Considering the current popularity of Python, indicated by the results of Stack Overflow survey among developers in 2020, it becomes increasingly important to understand how SBFL techniques perform on Python projects. In this work, our objective is to analyze the effectiveness of popular SBFL techniques in real world Python projects

## Requirements
- Python 3

If you want to run BugsInPy on Windows, you need to install:
- Git Bash (run the script through it)

## Steps to set up
Please run './setup.sh' when you clone this repository. This script would be:
1. Clone BugsInPy repository (https://github.com/soarsmu/BugsInPy)
2. Set up the path environment (if you use Windows you can set up it manually by "Edit the system environment variables" and add the framework/bin from BugsInPy repository into the path)
3. Move several scripts into the correct repository (for example, add the bugsinpy-faultloc into the framework/bin)

## BugsInPy Commands
As an additional from the previous commands in BugsInPy, we also have:
Command | Description
--- | ---
faultloc | Run fault localization on specific project that the output is "<project_name>_<buggy_id>_fault_localization.txt"

## Example of BugsInPy command to get the fault localization score
- Checkout a buggy source code version (black, bug 1, buggy version):
    - `bugsinpy-checkout -p black -v 0 -i 1 -w /temp/projects`
- Compile sources and tests from the current directory:
    - `bugsinpy-compile`
- Copy the "SBFL/pytest_pinpoint.py" file into the current directory
- Run the fault localization on the current directory
    - `bugsinpy-faultloc`

## Analysis Results
As running tests and coverage can be very computationally expensive, we also put the SBFL result in this repository folder "Results".
You can combine these results of every project by running `python combine_get_rank.py` in the "Analysis" folder. Then, you can get the analysis results for every RQ in the paper by running `python analyze_results.py > analysis_results.txt` (you can also change the output file name) in the "Analysis" folder.