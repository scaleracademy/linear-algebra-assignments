import numpy as np
from scipy.optimize import linprog

print('\n\u001B[41m\u001B[30m',
      '========== using the sample solution for SIMPLEX - this is not the student solution ==========',
      '\n\u001b[43m\u001B[30m')


def simplex(A, b, c):
    """solves a LPP problem given in standard form
        maximize c.x subject to Ax <= b and x >= 0
        returns: the vector x"""

    A = np.array(A, dtype=np.double)
    b = np.array(b, dtype=np.double)
    c = np.array(c, dtype=np.double)

    result = linprog(-c, A_ub=A, b_ub=b, bounds=(0, None))
    return result.x
