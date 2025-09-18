import math
'''
    We have to find cases where the matrices cannot be multiplied
    The error to be raised are of two types:-
    TypeErrrors:-
    1. The matrices are not in the form of a list
    2. The rows in the matrices are not lists.
    3. The length of each row are not equal.

    ValueErrors:-
    1. The cells have NaN or infinite values.
    2. They are not compatible
    3. The matrices are empty.
    4. The cells are not of the type int, float or complex.
    5. They contain boolean values as bool passes as int in the second condition.
    '''
def matrix_multiply(matrix1, matrix2):

    def check_matrix(matrix):
    # TypeErrors
        if not isinstance(matrix, list):
            raise TypeError("Input is not in the form of a list")

        if not matrix:
            raise ValueError("Matrix is empty")

        if not all(isinstance(row, list) for row in matrix):
            raise TypeError("Rows are not in the form of a list")

        a = len(matrix[0])
        if any(len(row) != a for row in matrix):
            raise TypeError("The list is not in the form of a matrix")

        #Errors in each value of the cells
        for row in matrix:
            for x in row:
                if isinstance(x, bool):
                    raise TypeError("Boolean value detected")

                if not isinstance(x, (int, float, complex)):
                    raise TypeError("The cells are not of types: int or float")
                
                if not isinstance(x, complex) and not math.isfinite(x):
                    raise ValueError("Infinit value detected")

    check_matrix(matrix1)
    check_matrix(matrix2)

    r1, c1 = len(matrix1), len(matrix1[0])
    r2, c2 = len(matrix2), len(matrix2[0])

    if c1 != r2:
        raise ValueError("The matrices are not compatible for matrix_mul")

    res = []
    for i in range(r1):
        row = []
        for j in range(c2):
            sum = 0
            for k in range(c1):
                sum += matrix1[i][k] * matrix2[k][j]
            row.append(sum)
        res.append(row)

    return res



