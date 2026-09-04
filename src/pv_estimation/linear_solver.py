"""M4: explicit Gaussian elimination with partial pivoting and back substitution."""

from .contracts import FloatArray


def solve_linear_system(
    matrix: FloatArray, rhs: FloatArray, *, pivot_rtol: float = 1e-12
) -> FloatArray:
    """Solve square A*x=b without modifying inputs or using library solvers.

    Reject invalid input with ValueError; raise LinearSolveError on numerical
    singularity. Scale pivot checks relative to the matrix magnitude.
    """
    raise NotImplementedError("M4: implement and test solve_linear_system")
