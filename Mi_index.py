

#To Calculate Maintianbility by regression
# Shishir Pokhrel
# shishir.pokhrel@mercedes-benz.com | shishir.pokhrel@student.uni-siegen.de
# December 14 2023

import os
import re
import math
from collections import defaultdict

# store results
hv_results = []
loc_results = []
cc_results = []
source_file = []
file_count = 1

#CYCLOMATIC COMPLEXITY
def calculate_cyclomatic_complexity(code):
    # Count control flow keywords (if, while, for, switch, case)
    control_flow_keywords = re.findall(r'\b(if|while|for|switch|case|break|&&|\|\|)\b', code)
    return len(control_flow_keywords) + 1  # Number of edges + 1

#Lines of code
def count_lines_of_code(file_path):
     with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines_count = file.readlines()
        return len(lines_count)

#Calculate Volume
def calculate_halstead_volume(code):
    # Regex to find operatands and operators
    operand_pattern = r'\b[A-Za-z_][A-Za-z0-9_]*\b'
    operator_pattern = r'[+\-*/%=<>!&|^~]'

    operators = re.findall(operator_pattern, code)
    operands = re.findall(operand_pattern, code)

    # distinct operators and operands
    distinct_operators = set(operators)
    distinct_operands = set(operands)

    # total operators and operands
    total_operators = len(operators)
    total_operands = len(operands)

    # Halstead values
    n1 = len(distinct_operators)
    n2 = len(distinct_operands)
    N1 = total_operators
    N2 = total_operands

    #  Halstead volume
    volumee = (N1 + N2) * (math.log2(n1 + n2))
    volume = round(volumee,2)
     #  math domain error by checking if logarithm is negativ
    if n1 + n2 == 0 or N1 + N2 == 0:
        #print("here is debug- at n1+n2=0 or N12=0")
        volume = 0
    else:
        # Calculate Halstead volume
        volume = (N1 + N2) * (math.log2(n1 + n2))
    try:
        # ... (same as before)
        volume = (N1 + N2) * (math.log2(n1 + n2))
        #print("here is debug-- with log ")

    except (ValueError, ZeroDivisionError):
        # Handle math domain errors by setting volume to 0
        volume = 0
        #print("HERE IS DEBUGGGG")
    return volume


#go through each files to measure metrics
def process_directory(directory_path):
    results = defaultdict(lambda: {'Halstead_volume': 0, 'Cyclomatic_complexity': 0, 'Lines_of_code': 0})
    file_count = 1
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                volume = calculate_halstead_volume(file_path)
                complexity = calculate_cyclomatic_complexity(file_path)
                loc = count_lines_of_code(file_path)

                # Extract package name from the directory
                package_name = root.split(os.path.sep)[6]
                package_category = root.split(os.path.sep)[5]
                results[package_name]['Module'] = package_category   
                results[package_name]['Halstead_volume'] += round(volume,2)
                results[package_name]['Cyclomatic_complexity'] += complexity
                results[package_name]['Lines_of_code'] += loc
                file_count += 1
            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    print(file_count)
    return results

#PRint results in the console
def print_pretty_table(results):
    print("{:<15} {:<15} {:<20} {:<25} {:<15}".format('Module' , 'Package_name', 'Halstead_volume', 'Cyclomatic_complexity', 'Lines_of_code'))

#Generate Latex Table to present
def generate_latex_table(results):
    latex_table = "\\begin{tabular}{|c|c|c|c|c|}\n"
    latex_table += "\\hline\n"
    latex_table += "Module & Package\_name & Halstead\_volume & Cyclomatic\_complexity & Lines\_of\_code \\\\\n"
    latex_table += "\\hline\n"

    for package_name, metrics in results.items():
        latex_table += "{} & {} & {} & {} & {} \\\\\n".format(metrics['Module'], package_name, metrics['Halstead_volume'], metrics['Cyclomatic_complexity'], metrics['Lines_of_code'])

    latex_table += "\\hline\n\\end{tabular}\n"
    return latex_table

if __name__ == "__main__":
    import math
    directory_path = '/work/AGL/pike/source_imageMinimal/dev_tools/Python'
    results = process_directory(directory_path)
    print("Pretty Table:")
    print_pretty_table(results)

    print("\nLaTeX Table:")
    latex_table = generate_latex_table(results)
    print(f"-----------------------totalFile: {file_count}----------------------------------------------------------------------")
    print(latex_table)
