# Do NOT use any external libraries

def solve(A, b):
    """A is a m x n matrix, and b is an n x 1 vector.
    returns: x, where x is the solution to the equation Ax = b
    if no solution exists, return -1
    if infinite solutions exist, return -2"""
    x = [0] * len(A[0])
    return x


def det(A):
    """calculates the determinant of A
    if A is not a square matrix, return 0"""
    return 0
