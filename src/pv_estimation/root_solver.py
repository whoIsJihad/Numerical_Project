"""M2: generic scalar Newton, bisection and safeguarded Newton methods."""

from .contracts import RootOptions, RootResult, ScalarFunction


def solve_root(
    function: ScalarFunction,
    derivative: ScalarFunction | None,
    *,
    initial_guess: float | None,
    bracket: tuple[float, float] | None,
    options: RootOptions,
) -> RootResult:
    """Solve function(x)=0; dispatch using options.method.

    Newton needs an initial guess and derivative; hybrid needs a derivative
    and bracket; bisection needs a bracket. Numerical failure returns root=None
    and converged=False with diagnostics. Invalid options raise ValueError.
    """
    raise NotImplementedError("M2: implement and test solve_root")
