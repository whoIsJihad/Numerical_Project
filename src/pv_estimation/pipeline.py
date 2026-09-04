"""M1: baseline wiring only; algorithms remain with their component owners."""

from .contracts import (
    BaselineResult,
    FitOptions,
    FloatArray,
    IVData,
    ParameterBounds,
    PVConditions,
    RootOptions,
)


def run_baseline(
    data: IVData,
    conditions: PVConditions,
    initial_theta: FloatArray,
    bounds: ParameterBounds,
    root_options: RootOptions,
    fit_options: FitOptions,
) -> BaselineResult:
    """Validate data/parameters, bind M4 residual callback, invoke M3, then M5 RMSE.

    Return rmse_a=None for failed fits. See docs/INTERFACES.md for the exact
    call chain. Do not reimplement missing member functions in this runner.
    """
    raise NotImplementedError("M1: wire and integration-test run_baseline")
