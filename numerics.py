"""Member 4: residuals, finite differences and explicit linear algebra."""

from collections.abc import Callable
from typing import TypeAlias

from current import RootMethod
from model import Array, Bounds

ResidualFunction: TypeAlias = Callable[[Array], Array]  # theta (P,) -> residuals (N,)


def residuals(
    theta: Array,
    voltage: Array,
    measured_current: Array,
    vt: float,
    ns: int = 1,
    root_method: RootMethod = "hybrid",
) -> Array:
    """Call current.predict_current; return predicted-minus-measured (N,) errors.

    Any failed root raises RuntimeError with point/reason. Do not omit points.


    Inputs: theta (5,), voltage/measured_current (N,) [V/A], vt > 0 [V/cell],
    integer ns >= 1, allowed root_method.
    Returns: Finite residuals (N,) [A].
    """
    raise NotImplementedError("Member 4: residual vector")


def jacobian(
    residual_fn: ResidualFunction,
    theta: Array,
    bounds: Bounds,
    scales: Array,
    relative_step: float = 1e-6,
) -> Array:
    """Return finite-difference (N,P) Jacobian of the residual callback.

    Start h_j = relative_step * max(abs(theta[j]), scales[j]); scales are positive.
    Use feasible forward/backward steps at bounds and actual nonzero represented
    step sizes. Failed evaluations raise RuntimeError, never a fabricated zero column.


    Inputs: callback theta(P,)->residuals(N,), theta/scales (P,), bounds=(lower,upper)
    each (P,), positive scales and finite relative_step > 0.
    Returns: Jacobian (N,P); P=5 for PV, other sizes allowed for toy tests.
    """
    raise NotImplementedError("Member 4: finite-difference Jacobian")


def solve_linear(matrix: Array, rhs: Array, pivot_rtol: float = 1e-12) -> Array:
    """Solve A*x=b via Gaussian elimination with partial pivoting/back substitution.

    Copy inputs. Invalid shapes/nonfinite values raise ValueError; numerical
    singularity raises RuntimeError. Scale pivot checks to matrix magnitude.
    Do not use numpy.linalg.solve/inv/lstsq or SciPy for this algorithm.


    Inputs: Finite matrix (P,P), rhs (P,), finite pivot_rtol > 0.
    Returns: Solution (P,); no mutation. P=5 for the PV optimizer.
    """
    raise NotImplementedError("Member 4: pivoted linear solve")
