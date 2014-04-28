# solves *bounded* LPs of the form:
# max cx
# sub to: Ax <= b

from sympy import *
from itertools import combinations

# enumerates all the vertices of {x | Ax <= b}
def enumeratevertices(A, b):
    m, n = A.rows, A.cols

    for rowlist in combinations(range(m), n):
        Ap = A.extract(rowlist, range(n))
        bp = b.extract(rowlist, [0])

        if Ap.det() != 0:
            xp = Ap.LUsolve(bp)

            d = A * xp - b
            feasible = True
            for i in range(m):
                if d[i] > 0:
                    feasible = False

            if feasible:
                yield xp

# finds the optimum using vertex enumeration
def findoptimum(A, b, c):
    m, n = A.rows, A.cols

    bestvalue, bestvertex = None, None
    for vertex in enumeratevertices(A, b):
        if bestvalue is None or (vertex.T * c)[0] > bestvalue:
            bestvalue = (vertex.T * c)[0]
            bestvertex = vertex

    return bestvertex

def solve(A, b, c):
    x = findoptimum(A, b, c)

    if not x:
        print 'LP is infeasible'
    else:
        print 'Vertex', x.T, 'is optimal'
        print 'Optimal value is', (c.T * x)[0]

if __name__ == '__main__':

    # small example
    A = Matrix([[50, 24],
         [30, 33],
         [-1, 0],
         [0, -1]])
    b = Matrix([2400, 2100, -45, -5])
    c = Matrix([1, 1])

    solve(A, b, c)
