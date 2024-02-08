# Do NOT use any external libraries

def simplex(A, b, c):
    """solves a LPP problem given in standard form
        maximize c.x subject to Ax <= b and x >= 0
        returns: the vector x"""
    return [0] * len(c)
