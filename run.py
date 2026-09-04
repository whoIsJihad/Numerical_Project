"""Member 1: wire the pipeline; do not duplicate the numerical algorithms."""

from typing import TypedDict

from current import RootMethod
from fit import FitMethod, FitResult
from model import Array, Bounds


class BaselineResult(TypedDict):
    fit: FitResult
    rmse: float | None  # [A], None when fit did not converge


def run_baseline(
    voltage: Array,
    current: Array,
    vt: float,
    theta0: Array,
    bounds: Bounds,
    scales: Array,
    ns: int = 1,
    root_method: RootMethod = "hybrid",
    fit_method: FitMethod = "lm",
) -> BaselineResult:
    """Return {"fit": fit result, "rmse": value or None}.

    Validate inputs. Bind numerics.residuals into a callback accepting only theta.
    Pass that callback to fit.fit_parameters. Call experiments.rmse only if
    the fit converged. A failed fit has rmse=None.


    Inputs: voltage/current (N,) [V/A], vt > 0 [V/cell], theta0/scales (5,),
    bounds=(lower,upper) each (5,), integer ns >= 1, allowed method names.
    Returns: BaselineResult with fit diagnostics and optional RMSE; no input mutation.
    """
    raise NotImplementedError("Member 1: connect the pipeline")


def main() -> None:
    """Read CSV/temperature/settings, get starting parameters, run and report.

    Begin with one baseline fit. Later offer a noise-study option using Member 5's
    monte_carlo and a fixed-start fit callback. Report failures honestly and
    exit nonzero for failed baseline runs. No argument parser is implemented yet.


    Inputs: No Python arguments; future CLI arguments come from the command line.
    Returns: None; displays/saves results; nonzero exit on baseline failure.
    """
    raise NotImplementedError("Member 1: entry point")


if __name__ == "__main__":
    main()
