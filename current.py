"""Member 2: scalar root solving, then current prediction across voltages."""

from collections.abc import Callable
from typing import Literal, TypeAlias, TypedDict

from model import Array

RootMethod: TypeAlias = Literal["newton", "bisection", "hybrid"]
ScalarFunction: TypeAlias = Callable[[float], float]


class RootResult(TypedDict):
    """Ordinary dictionary; all listed keys are required."""

    root: float | None  # None on failure
    converged: bool
    reason: str
    iterations: int
    function_evaluations: int


class CurveResult(TypedDict):
    """Entries align with original input voltage order."""

    current: Array  # (N,) amperes; NaN only at failed points
    roots: list[RootResult]  # length N


def solve_root(
    function: ScalarFunction,
    derivative: ScalarFunction | None,
    initial_guess: float | None = None,
    bracket: tuple[float, float] | None = None,
    method: RootMethod = "hybrid",
    tol: float = 1e-8,
    max_iter: int = 100,
) -> RootResult:
    """Return root/converged/reason/iterations/function_evaluations dictionary.

    Newton needs an initial guess and derivative. Bisection needs a bracket;
    hybrid needs a bracket and derivative. Accept endpoint roots. Safeguard
    Newton inside a sign-changing bracket; check finite values and convergence.
    Use both equation error and scale-aware step/bracket checks, not tiny steps
    alone. Numerical failure returns root=None and converged=False.


    Inputs: function(x)->float; derivative(x)->float or None for bisection; optional scalar guess;
    optional ordered (a,b) bracket; allowed method; finite tol > 0, integer max_iter > 0.
    Returns: RootResult with the keys declared above.
    """
    raise NotImplementedError("Member 2: Newton, bisection and hybrid")


def predict_current(
    voltage: Array,
    theta: Array,
    vt: float,
    ns: int = 1,
    method: RootMethod = "hybrid",
    warm_start: bool = True,
) -> CurveResult:
    """Return {"current": array, "roots": list of root-result dictionaries}.

    Use model.equation/current_derivative through solve_root. Own bracket finding
    with bounded expansion; [0,Iph] is not valid at every voltage. For continuation,
    sort voltages internally and restore original order, including duplicates.
    Warm-start only from successful roots. Failed currents are NaN, with diagnostics.


    Inputs: voltage (N,) [V], theta (5,), vt > 0 [V/cell], integer ns >= 1,
    allowed method, boolean warm_start.
    Returns: CurveResult with N aligned currents and root diagnostics.
    """
    raise NotImplementedError("Member 2: current curve and warm starts")
