import numpy as np
from fractions import Fraction
from sympy import Matrix

def get_matrix_from_user():
    rows = int(input("Inserisci il numero di righe: "))
    cols = int(input("Inserisci il numero di colonne: "))
    matrix = []
    print("Inserisci la matrice riga per riga (elementi separati da spazio):")
    for _ in range(rows):
        row = list(map(Fraction, input().split()))
        matrix.append(row)
    return np.array(matrix, dtype=Fraction)

def is_row_echelon(matrix):
    rows, cols = matrix.shape
    lead = 0
    for r in range(rows):
        if lead >= cols:
            return True
        i = r
        while matrix[i, lead] == 0:
            i += 1
            if i == rows:
                i = r
                lead += 1
                if cols == lead:
                    return True
        if i != r:
            return False
        lead += 1
    return True

def row_echelon(matrix):
    def swap_rows(mat, i, j):
        mat[[i, j]] = mat[[j, i]]
        operations.append(f"R{i + 1} <--> R{j + 1}")
    
    def subtract_rows(mat, src_row, dest_row, factor):
        mat[dest_row] -= factor * mat[src_row]
        operations.append(f"R{dest_row + 1} - {factor}R{src_row + 1}")
    
    def add_rows(mat, src_row, dest_row, factor):
        mat[dest_row] += factor * mat[src_row]
        operations.append(f"R{dest_row + 1} + {factor}R{src_row + 1}")
    
    rows, cols = matrix.shape
    lead = 0
    operations = []
    
    for r in range(rows):
        if lead >= cols:
            break
        i = r
        while matrix[i, lead] == 0:
            i += 1
            if i == rows:
                i = r
                lead += 1
                if lead == cols:
                    break
        if i != r:
            swap_rows(matrix, i, r)
        for i in range(r + 1, rows):
            lv = matrix[i, lead]
            if lv != 0:
                factor = lv / matrix[r, lead]
                subtract_rows(matrix, r, i, factor)
        lead += 1
    
    return matrix, operations

def matrix_inverse(matrix):
    n = len(matrix)
    identity = np.eye(n, dtype=Fraction)
    augmented_matrix = np.hstack((matrix, identity))
    operations = []

    for i in range(n):
        if augmented_matrix[i, i] == 0:
            for j in range(i + 1, n):
                if augmented_matrix[j, i] != 0:
                    augmented_matrix[[i, j]] = augmented_matrix[[j, i]]
                    operations.append(f"R{i + 1} <--> R{j + 1}")
                    break
        pivot = augmented_matrix[i, i]
        augmented_matrix[i] = augmented_matrix[i] / pivot
        operations.append(f"R{i + 1} / {pivot} --> R{i + 1}")
        
        for j in range(n):
            if i != j:
                factor = augmented_matrix[j, i]
                augmented_matrix[j] -= factor * augmented_matrix[i]
                operations.append(f"R{j + 1} - {factor}R{i + 1} --> R{j + 1}")

    inverse_matrix = augmented_matrix[:, n:]
    return inverse_matrix, operations

def matrix_basis(matrix):
    sympy_matrix = Matrix(matrix)
    rref_matrix, pivot_columns = sympy_matrix.T.rref()
    basis = [matrix[:, i] for i in pivot_columns]
    return np.array(basis, dtype=object).T

def matrix_to_latex(matrix):
    latex_str = "$$\n\\begin{bmatrix}\n"
    for row in matrix:
        latex_str += " & ".join(str(element) for element in row) + " \\\\\n"
    latex_str += "\\end{bmatrix}\n$$"
    return latex_str

def main():
    matrix = get_matrix_from_user()
    
    print("Matrice originale:")
    print(matrix)
    print(matrix_to_latex(matrix))
    
    if is_row_echelon(matrix):
        print("La matrice è già in forma a scala.")
    else:
        matrix_echelon, operations = row_echelon(matrix.copy())
        print("Matrice trasformata in forma a scala:")
        print(matrix_echelon)
        print(matrix_to_latex(matrix_echelon))
        print("Operazioni elementari eseguite:")
        for op in operations:
            print(op)
    
    calc_inverse = input("Vuoi calcolare l'inversa della matrice? (s/n): ").strip().lower()
    if calc_inverse == 's':
        try:
            inverse_matrix, inverse_operations = matrix_inverse(matrix.copy())
            print("Matrice inversa:")
            print(inverse_matrix)
            print(matrix_to_latex(inverse_matrix))
            print("Operazioni per calcolare l'inversa:")
            for op in inverse_operations:
                print(op)
        except np.linalg.LinAlgError:
            print("La matrice non è invertibile.")
    
    calc_transpose = input("Vuoi calcolare la trasposta della matrice? (s/n): ").strip().lower()
    if calc_transpose == 's':
        transpose_matrix = matrix.T
        print("Matrice trasposta:")
        print(transpose_matrix)
        print(matrix_to_latex(transpose_matrix))

    calc_basis = input("Vuoi calcolare la base della matrice? (s/n): ").strip().lower()
    if calc_basis == 's':
        basis_matrix = matrix_basis(matrix)
        print("Base della matrice:")
        print(basis_matrix)
        print(matrix_to_latex(basis_matrix))

if __name__ == "__main__":
    main()
