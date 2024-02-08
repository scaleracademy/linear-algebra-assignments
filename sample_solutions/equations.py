import numpy as np

print('\n\u001B[41m\u001B[30m',
      '========== using the sample solution for EQUATIONS - this is not the student solution ==========',
      '\n\u001b[43m\u001B[30m')


def solve(A, b):
    """A is a m x n matrix, and b is an n x 1 vector.
    returns: x, where x is the solution to the equation Ax = b
    if no solution exists, return -1
    if infinite solutions exist, return -2"""
    A = np.array(A, dtype=np.double)
    b = np.array(b, dtype=np.double)
    n, m = A.shape

    Ab = np.hstack((A, b))
    rank_A = np.linalg.matrix_rank(A)
    rank_Ab = np.linalg.matrix_rank(Ab)
    if rank_A != rank_Ab:
        return -1
    if rank_A < n:
        return -2
    return np.linalg.solve(A, b)


def det(A):
    """calculates the determinant of A
    if A is not a square matrix, return 0"""
    return np.linalg.det(A)
