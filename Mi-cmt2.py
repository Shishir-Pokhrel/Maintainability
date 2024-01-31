import re
import math
import os



#go through the directory where the files are 

def process_directory(directory_path):
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)

            # Read the code from the file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                code = file.read()
  
           
            # Filter comments from the code
            code_without_comments = remove_comments(code)
           
            # Calculate cyclomatic complexity
            complexity = calculate_cyclomatic_complexity(code_without_comments)

            # Calculate Halstead volume and metrics
            V =  calculate_halstead_volume(code_without_comments)

            # Count lines of code
            line_count = count_lines_of_code(file_path)

            # Count comments and calculate pCM
            comments = count_comments(code)
            pCM = (comments / line_count) * 100

            # Print the file information
            print(f"{os.path.basename(file_path)}:\n")
            print(f"Module: {filename}")
            print(f"Cyclomatic Complexity: {complexity}")
            print(f"Halstead Volume: {V}")
            print(f"Lines of Code: {line_count}")
            print(f"Comments Percent (pCM): {pCM:.2f}\n")


def remove_comments(code):
    # Regular expression to remove comments
    #comment_regex = r'(//.*?\n)|(/\*.*?\*/)'
    comment_regex = r'(//.*?\n)|(#.*?\n)|(/\*(?:(.|\n)*?)?\*/)'

    # Remove comments from the code
    filtered_code = re.sub(comment_regex, '', code)

    return filtered_code

def count_comments(code):
    # Regular expression to count comments
    comment_regex = r'(//.*?\n)|(/\*.*?\*/)'

    # Count comments
    comments = len(re.findall(comment_regex, code))

    return comments

def calculate_cyclomatic_complexity(code):
    # Count control flow keywords (if, while, for, switch, case, etc.)
    control_flow_keywords = re.findall(r'\b(if|while|for|switch|case|break|&&|\|\|)\b', code)

    # Return cyclomatic complexity (number of edges + 1)
    return len(control_flow_keywords) + 1



def calculate_halstead_volume(code):
    # Regex to find operands and operators
    operand_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
    operator_pattern = r'[+\-*/%=<>!&|^~]'

    # Extract operands and operators from the code
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
        
    return volume

def count_lines_of_code(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines_count = file.readlines()
        return len(lines_count)


if __name__ == "__main__":
    import math
 
    #directory_path = '/work/AGL/pike/source_imagedemo/'
    directory_path = '/work/AGL/pike/source_imageMinimal'
    directory_path = '/work/AGL/pike/source_imageMinimal/dev_tools/dbus-1.14.8/dbus/'
    results = process_directory(directory_path)












