from pysat.solvers import Solver

def solve(clauses):
    with Solver(name='g4') as s:
        for clause in clauses:
            s.add_clause(clause)
        return s.solve()