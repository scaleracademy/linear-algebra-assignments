# Do NOT use any external libraries

def pldu(M):
    """M: a non-singular matrix
        returns: (P, L, D, U) such that M = PLDU
        where
            P is a row permutation matrix,
            L is a unit lower triangular matrix, 
            D is a diagonal matrix, 
            U is an unit upper triangular matrix"""
    P = L = D = U = M
    return P, L, D, U
