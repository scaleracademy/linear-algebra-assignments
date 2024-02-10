from contextlib import contextmanager
from copy import deepcopy

import numpy as np
from scipy.optimize import linprog

import solutions

TAB = '\t'
num_tests = 10000


def close(x, y):
    return np.allclose(x, y, 5e-2, 5e-2, True)


@contextmanager
def debug():
    print('\n\u001b[41m\u001B[30m', end='')
    yield
    print('\033[0m')


@contextmanager
def info():
    print('\u001b[43m\u001B[30m', end='')
    yield
    print('\033[0m', end='')


def _generate_matrix(n, m, rank, max=3):
    # generate matrix of given dimensions and rank using A=UPV
    while True:
        U = np.random.randint(-1, max, (n, n))
        V = np.random.randint(-1, max, (m, m))
        P = np.eye(n, m)
        P[rank:, rank:] = 0
        A = U @ P @ V

        # sort the rows so that the leftmost 0's are pulled to the top
        # this way, if the matrix is singular, the row reductions require row swaps
        A = sorted([list(map(float, row)) for row in A])
        if np.linalg.matrix_rank(A) == rank:
            return A


def _generate_vector(n, max=3):
    return list(map(float, list(np.random.randint(-1, max, (n, 1)))))


def generate_non_singular_matrix(max=3):
    n = np.random.randint(2, 5)
    return _generate_matrix(n, n, n, max=max)


def generate_singular_matrix(max=3):
    n = np.random.randint(2, 5)
    m = np.random.randint(2, 5)
    rank = np.random.randint(1, min(n, m))
    return _generate_matrix(n, m, rank, max=max)


def test_pldu():
    def test(A):
        try:
            P, L, D, U = solutions.pldu.pldu(deepcopy(A))
        except Exception:
            raise
        try:
            A = np.array(A, dtype=np.double)
            P = np.array(P, dtype=np.double)
            L = np.array(L, dtype=np.double)
            D = np.array(D, dtype=np.double)
            U = np.array(U, dtype=np.double)
            n, m = A.shape
            assert P.shape == (n, n), 'Shape of P is incorrect'
            assert L.shape == (n, n), 'Shape of L is incorrect'
            assert D.shape == (n, n), 'Shape of D is incorrect'
            assert U.shape == (n, m), 'Shape of U is incorrect'
            if np.max(np.max(np.abs(L))) < 1e5 and np.max(np.max(np.abs(D))) < 1e5:
                assert close(A, P @ L @ D @ U), 'Incorrect decomposition'
            assert close(np.array(sorted(map(list, P), reverse=True), dtype=np.double),
                         np.eye(n, dtype=np.double)), 'P is not a permutation matrix'
            assert close(L, np.tril(L, -1) + np.eye(n)), 'L is not a lower triangular matrix with unit diagonal'
            assert close(D, np.diag(np.diag(D))), 'D is not a diagonal matrix'
            assert np.max(np.abs(np.diag(U))) <= 1.1, 'U has not been normalized to have unit diagonal'
            # don't expect students to be able to fix this themselves, hence won't check for upper-triangular-ness of U
            # assert close(U, U - np.tril(U, -1)), 'U is not an upper triangular matrix with unit diagonal'
        except KeyboardInterrupt:
            raise
        except Exception as e:
            with debug():
                print('Verdict:', e)
                print('A')
                print(A.round(2))
                print('P')
                print(P.round(2))
                print('L')
                print(L.round(2))
                print('D')
                print(D.round(2))
                print('U')
                print(U.round(2))
                print('reconstruction')
                print((P @ L @ D @ U).round(2))
            return False
        return True

    marks = 0
    with info():
        print('-' * 80)
        print('Testing PLDU')
        print(TAB, 'non-singular matrix:', end=' ')
    for _ in range(num_tests):
        A = generate_non_singular_matrix()
        result = test(A)
        if not result:
            with info():
                print(TAB, 'Failed')
            break
    else:
        marks += 6
        with info():
            print(TAB, 'Success!')
            print(TAB, 'bonus: singular matrix:', end=' ')
        for _ in range(num_tests):
            A = generate_non_singular_matrix()
            result = test(A)
            if not result:
                with info():
                    print(TAB, 'Failed')
                break
        else:
            marks += 2
            with info():
                print('Success! (2 bonus marks)')
    with info():
        print(TAB, 'Final Marks for PLDU:', marks, '/ 6')


def test_equations():
    def test_solve(A, b):
        try:
            x = solutions.equations.solve(deepcopy(A), deepcopy(b))
        except Exception:
            raise

        A = np.array(A, dtype=np.double)
        n, m = A.shape
        b = np.array(b, dtype=np.double)
        Ab = np.hstack((A, b.reshape(-1, 1)))
        rank_A = np.linalg.matrix_rank(A)
        rank_Ab = np.linalg.matrix_rank(Ab)
        try:
            x = np.array(x, dtype=np.double)
            if rank_A != rank_Ab:
                assert x == -1, 'Incorrect result for Inconsistent system of equations'
            elif rank_A < n:
                assert x == -2, 'Incorrect result for Infinite solutions'
            else:
                assert close(A @ x, b), 'Incorrect result for Ax = b'
        except KeyboardInterrupt:
            raise
        except Exception as e:
            with debug():
                print('Verdict:', e)
                print('A')
                print(A.round(2))
                print('b')
                print(b.round(2))
                print('returned answer')
                print(x.round(2))
                print('correct answer')
                print(np.linalg.solve(A, b).round(2))
            return False
        return True

    def test_det(A):
        try:
            d = solutions.equations.det(deepcopy(A))
        except Exception:
            raise
        A = np.array(A, dtype=np.double)
        n, m = A.shape
        try:
            if n != m:
                assert d == 0, 'Incorrect result for non-square matrix'
            else:
                assert close(d, np.linalg.det(A)), 'Incorrect result for determinant'
        except KeyboardInterrupt:
            raise
        except Exception as e:
            with debug():
                print('Verdict:', e)
                print('A')
                print(A.round(2))
                print('returned answer')
                print(d)
                print('correct answer')
                print(np.linalg.det(A))
            return False
        return True

    marks = 0
    with info():
        print('-' * 80)
        print('Testing Equations')
        print(TAB, 'solve Ax=b:', end=' ')
    for _ in range(num_tests):
        A = generate_non_singular_matrix()
        b = _generate_vector(len(A))
        result = test_solve(A, b)
        if not result:
            with info():
                print(TAB, 'Failed')
            break
    else:
        marks += 3
        with info():
            print(TAB, 'Success!')
    with info():
        print(TAB, 'determinant:', end=' ')
    for _ in range(num_tests):
        A = generate_non_singular_matrix()
        result = test_det(A)
        if not result:
            with info():
                print(TAB, 'Failed')
            break
    else:
        marks += 3
        with info():
            print(TAB, 'Success!')
    with info():
        print(TAB, 'Final Marks for Equations:', marks, '/ 6')


def test_simplex():
    def test(A, b, c):
        try:
            x = solutions.simplex.simplex(deepcopy(A), deepcopy(b), deepcopy(c))
        except Exception:
            raise
        try:
            A = np.array(A, dtype=np.double)
            b = np.array(b, dtype=np.double)
            c = np.array(c, dtype=np.double)
            x = np.array(x, dtype=np.double)

            value = np.dot(c.T, x)

            result = linprog(-c, A_ub=A, b_ub=b, bounds=(0, None))
            if result.x is None:
                return True  # infeasible, so no need to check the result
            assert close(value, -result.fun), 'Suboptimal result for Simplex'
        except KeyboardInterrupt:
            raise
        except Exception as e:
            with debug():
                print('Verdict:', e)
                print('A')
                print(A.round(2))
                print('b')
                print(b.round(2))
                print('c')
                print(c.round(2))
                print('returned answer')
                print(x.round(2))
                print('correct answer')
                print(result.x.round(2))
                print('correct optimal value')
                print(-result.fun)
            return False
        return True

    marks = 0
    with info():
        print('-' * 80)
        print('Testing Simplex: ', end=' ')
    for _ in range(num_tests):
        A = generate_singular_matrix()
        b = [max(0, x) for x in _generate_vector(len(A), max=1000)]
        c = _generate_vector(len(A[0]))
        result = test(A, b, c)
        if not result:
            with info():
                print(TAB, 'Failed')
            break
    else:
        marks += 6
        with info():
            print(TAB, 'Success!')
    with info():
        print(TAB, 'Final Marks for Simplex:', marks, '/ 6')


def check_all():
    np.random.seed(0)
    test_pldu()
    test_equations()
    test_simplex()
    print('\033[0m')


if __name__ == '__main__':
    check_all()
