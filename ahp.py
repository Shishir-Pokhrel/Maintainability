#Script to evaluate pairwise assessment of software quality characterstics
#Shishir Pokhrel shishir.pokhrel@mercedes-benz.com; shishir.pokhrel@student.uni-siegen.de
# January 3


import numpy as np
from scipy.linalg import eig

#Arrage matrix to pairwise assessment and ask for inputs
def create_pairwise_matrix(criteria):
    n = len(criteria)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i == j:
                matrix[i, j] = 1
            if i<j:
                element = float(input(f"Enter the comparison value for {criteria[i]} and {criteria[j]}: "))
                matrix[i, j] = round(element,2)
                matrix[j, i] = 1 / round( element,2)
    return matrix

# calculate the eigenvector
def calculate_eigenvector(matrix):
    _, eigenvectors = eig(matrix)
    normalized_eigenvector = eigenvectors[:, 0] / np.sum(eigenvectors[:, 0])
    
    return normalized_eigenvector
 
   

def main():
    criteria = ["Analysability", "Changeability", "Stability", "Testability"]
    
    # Pairwise Comparison Matrix
    pairwise_matrix = create_pairwise_matrix(criteria)
    print(pairwise_matrix)
    
    # Calculate Eigenvector
    eigenvector = calculate_eigenvector(pairwise_matrix)
    print(eigenvector)

    
    # Print LaTeX Table
    print("\nLaTeX Table:")
    print("\\begin{array}{cccc}")   
    print("\\text{} &", " & ".join(criteria), "\\\\")
    print("\\hline")
    for i, row in enumerate(pairwise_matrix):
        print(criteria[i], end=" & ")
        print(" & ".join(map(lambda x: f"{x:.4f}", row)), "\\\\")
    print("\\end{array}\n")
    
    # Print Eigenvector
    print("\nEigenvector:")
    print(dict(zip(criteria, eigenvector)))
    

if __name__ == "__main__":
    main()
