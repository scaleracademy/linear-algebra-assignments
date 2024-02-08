import numpy as np

print('\n\u001B[41m\u001B[30m',
      '========== using the sample solution for PLDU - this is not the student solution ==========',
      '\n\u001b[43m\u001B[30m')


def pldu(M):
    """M: a non-singular matrix
        returns: (P, L, D, U) such that M = PLDU
        where
            P is a row permutation matrix,
            L is a unit lower triangular matrix, 
            D is a diagonal matrix, 
            U is an unit upper triangular matrix"""
    M = np.array(M, dtype=np.double)
    n, m = M.shape

    P = np.eye(n, dtype=np.double)
    L = np.eye(n, dtype=np.double)
    U = M.copy()

    for i in range(min(n, m) - 1):
        if U[i, i] == 0:
            pivot = np.argmax([(0 if x == 0 else 1) for x in U[i:, i]]) + i
            if U[pivot, i] == 0:
                continue
            # Swap the rows in U to move the pivot element to the diagonal
            U[[i, pivot], i:] = U[[pivot, i], i:]
            # Swap the rows in P and L to maintain the equivalence
            P[[i, pivot], :] = P[[pivot, i], :]
            L[[i, pivot], :i] = L[[pivot, i], :i]

        # Perform the elimination below the pivot
        for j in range(i + 1, n):
            if U[j, i] == 0: continue
            L[j, i] = U[j, i] / U[i, i]
            U[j, i:] -= L[j, i] * U[i, i:]

    # take P to the right hand side
    P_inv = np.linalg.inv(P)
    # extract the diagonal form U
    D = np.eye(n)
    for i in range(min(n, m)):
        if U[i, i] == 0:
            continue
        D[i, i] = U[i, i]
        U[i, :] /= U[i, i]

    # ensure U is upper triangular - needed because of numerical imprecision in the U[i,:] /= U[i,i] step
    U -= np.tril(U, -1)

    # M = P_inv.L.D.U
    return P_inv, L, D, U


if __name__ == '__main__':
    A = [
        [-6, 1, 2],
        [0, 0, -1],
        [2, -3, 0]
    ]
    P, L, D, U = pldu(A)
    print(P)
    print(L)
    print(D)
    print(U)
    print(np.allclose(np.array(A), P @ L @ D @ U))
