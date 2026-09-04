"""Member 5: metrics, reproducible noise experiments and reporting."""

from collections.abc import Callable
from pathlib import Path
from typing import TypeAlias, TypedDict

from numpy.random import Generator

from fit import FitResult
from model import Array

FitFunction: TypeAlias = Callable[[Array, Array], FitResult]  # voltage/current (N,)


class MonteCarloResult(TypedDict):
    seed: int
    sigma: float  # current-noise standard deviation [A]
    trials: list[FitResult]  # length repeats, including failures


class Summary(TypedDict):
    successes: int
    failures: int
    failure_rate: float
    mean_rmse: float | None  # [A], None when no successes
    parameter_mean: Array | None  # (5,), None when no successes
    parameter_std: Array | None  # (5,), None with fewer than two successes


class ResultMetadata(TypedDict):
    """Required provenance/settings for export."""

    source: str  # dataset citation or URL
    temperature_k: float
    ns: int
    theta0: Array  # (5,)
    settings: dict[str, str | int | float | bool]  # named scalar solver settings


def rmse(residuals: Array) -> float:
    """Return sqrt(mean(residuals**2)); reject empty, nonfinite or non-1-D input.

    Inputs: Finite residuals (N,) [A], N > 0.
    Returns: Scalar RMSE [A].
    """
    raise NotImplementedError("Member 5: RMSE")


def add_noise(current: Array, sigma: float, rng: Generator) -> Array:
    """Return a new current array with independent Gaussian noise.

    Sigma is a finite nonnegative standard deviation in A. Use the supplied
    numpy Generator, never reset it or mutate the original current.


    Inputs: Finite current (N,) [A], finite sigma >= 0 [A], NumPy Generator.
    Returns: New noisy current array (N,) [A].
    """
    raise NotImplementedError("Member 5: current noise")


def monte_carlo(
    voltage: Array,
    current: Array,
    fit_fn: FitFunction,
    sigma: float,
    repeats: int = 100,
    seed: int = 42,
) -> MonteCarloResult:
    """Return {"seed": seed, "sigma": sigma, "trials": list of fit dictionaries}.

    fit_fn(voltage, noisy_current) returns a fit_parameters result; the callback
    closes over identical starting parameters/settings for every trial.
    Use one default_rng(seed) stream. Keep every failed and successful fit;
    propagate programming errors. Validate repeats is a positive integer.


    Inputs: voltage/current (N,) [V/A], callback (voltage,current)->FitResult,
    finite sigma >= 0 [A], integer repeats > 0, nonnegative integer seed.
    Returns: MonteCarloResult containing exactly repeats trials.
    """
    raise NotImplementedError("Member 5: Monte Carlo")


def summarize(result: MonteCarloResult) -> Summary:
    """Return successes/failures/failure_rate/mean_rmse/parameter_mean/parameter_std.

    Failure rate uses all trials; other statistics use converged trials only.
    No successes: None for fit statistics. Sample std needs at least two successes.


    Inputs: Nonempty MonteCarloResult of five-parameter PV fits.
    Returns: Summary with the fields declared above; None for unavailable statistics.
    """
    raise NotImplementedError("Member 5: summary")


def save_results(
    result: MonteCarloResult, path: str | Path, metadata: ResultMetadata
) -> None:
    """Write strict JSON including seed, settings and dataset provenance.

    Convert arrays; use null for missing statistics, not NaN. Include temperature,
    series-cell count and initial parameters in metadata. Propagate I/O errors.


    Inputs: MonteCarloResult, destination JSON path, required ResultMetadata fields.
    Returns: None; writes a file. File errors propagate.
    """
    raise NotImplementedError("Member 5: export")


def plot_fit(
    voltage: Array, measured_current: Array, predicted_current: Array, path: str | Path
) -> None:
    """Save a labelled I-V plot in volts/amperes; reject mismatched/nonfinite arrays.

    Inputs: Matching finite (N,) arrays: voltage [V], both currents [A]; destination image path.
    Returns: None; saves a figure.
    """
    raise NotImplementedError("Member 5: plot")
