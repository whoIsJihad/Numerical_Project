"""Member 3: fit parameters by calling Member 4's Jacobian and linear solver."""

from typing import Literal, TypeAlias, TypedDict

from model import Array, Bounds
from numerics import ResidualFunction

FitMethod: TypeAlias = Literal["gauss_newton", "lm"]


class FitResult(TypedDict):
    """Ordinary dictionary; all listed keys are required."""

    theta: Array  # best valid (P,) iterate, or initial theta if none evaluated
    residuals: Array | None  # (N,), or None when no valid evaluation exists
    converged: bool
    reason: str
    iterations: int
    evaluations: int  # every residual callback invocation
    history: list[float]  # accepted mean squared errors


def fit_parameters(
    residual_fn: ResidualFunction,
    theta0: Array,
    bounds: Bounds,
    scales: Array,
    method: FitMethod = "lm",
    tol: float = 1e-8,
    max_iter: int = 100,
) -> FitResult:
    """Return theta/residuals/converged/reason/iterations/evaluations/history dict.

    GN: solve (J.T@J)*step=-J.T@r; use bounded backtracking.
    LM: add damping*identity, adjust damping using objective improvement.
    Keep candidates inside bounds; reject failed trial evaluations, with bounded
    retries. Initial evaluation failure returns a failed result.
    Count every residual call, including FD and rejected trials. History stores
    accepted MSE values. Return best valid theta/residuals; residuals may be None.
    Use scaled step, objective and gradient checks; report iteration-limit failure.
    Document tolerance policy. Catch known RuntimeError numerical failures only;
    NotImplementedError is a programming/incomplete-code signal and must propagate.


    Inputs: callback theta(P,)->residuals(N,), theta0/scales (P,), bounds=(lower,upper)
    each (P,), positive scales/tol, integer max_iter > 0, allowed method.
    Returns: FitResult (keys above). P=5 for PV; toy callbacks may use other P.
    """
    raise NotImplementedError("Member 3: Gauss-Newton and LM")
