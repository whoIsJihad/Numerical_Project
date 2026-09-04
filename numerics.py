"""Member 4: residuals, finite differences and explicit linear algebra."""


def residuals(theta, voltage, measured_current, vt, ns=1, root_method="hybrid"):
    """Call current.predict_current; return predicted-minus-measured (N,) errors.

    Any failed root raises RuntimeError with point/reason. Do not omit points.
    """
    raise NotImplementedError("Member 4: residual vector")


def jacobian(residual_fn, theta, bounds, scales, relative_step=1e-6):
    """Return finite-difference (N,P) Jacobian of the residual callback.

    Start h_j = relative_step * max(abs(theta[j]), scales[j]); scales are positive.
    Use feasible forward/backward steps at bounds and actual nonzero represented
    step sizes. Failed evaluations raise RuntimeError, never a fabricated zero column.
    """
    raise NotImplementedError("Member 4: finite-difference Jacobian")


def solve_linear(matrix, rhs, pivot_rtol=1e-12):
    """Solve A*x=b via Gaussian elimination with partial pivoting/back substitution.

    Copy inputs. Invalid shapes/nonfinite values raise ValueError; numerical
    singularity raises RuntimeError. Scale pivot checks to matrix magnitude.
    Do not use numpy.linalg.solve/inv/lstsq or SciPy for this algorithm.
    """
    raise NotImplementedError("Member 4: pivoted linear solve")
