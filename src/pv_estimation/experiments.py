"""M5: reproducible current-noise studies, metrics and reporting."""

from collections.abc import Mapping
from pathlib import Path

from numpy.random import Generator

from .contracts import (
    FitFunction,
    FloatArray,
    IVData,
    MonteCarloOptions,
    MonteCarloResult,
    MonteCarloSummary,
)


def rmse(residuals: FloatArray) -> float:
    """Return sqrt(mean(r**2)) in A; reject empty/nonfinite/non-1-D inputs."""
    raise NotImplementedError("M5: implement and test rmse")


def add_current_noise(data: IVData, sigma_current_a: float, rng: Generator) -> IVData:
    """Return a new dataset with independent Gaussian current noise; voltage unchanged.

    Do not mutate data or reset rng. Sigma must be finite and nonnegative.
    """
    raise NotImplementedError("M5: implement and test add_current_noise")


def run_monte_carlo(
    data: IVData, fit_fn: FitFunction, options: MonteCarloOptions
) -> MonteCarloResult:
    """Use one seeded Generator; perturb data, call fit_fn, retain every trial.

    fit_fn closes over identical initial theta, bounds and numerical options.
    Numerical failures are FitResult failures; do not swallow programming errors.
    """
    raise NotImplementedError("M5: implement and test run_monte_carlo")


def summarize_trials(result: MonteCarloResult) -> MonteCarloSummary:
    """Count all failures; summarize successful fits only, with explicit missing statistics."""
    raise NotImplementedError("M5: implement and test summarize_trials")


def save_results(
    result: MonteCarloResult, path: str | Path, *, metadata: Mapping[str, object]
) -> None:
    """Export strict JSON with options, diagnostics, trials and provenance; propagate I/O errors."""
    raise NotImplementedError("M5: implement and test save_results")


def plot_fit(data: IVData, predicted_current: FloatArray, path: str | Path) -> None:
    """Save measured/predicted I–V plot with units; reject nonfinite/misaligned arrays."""
    raise NotImplementedError("M5: implement and test plot_fit")


def plot_parameter_variation(result: MonteCarloResult, path: str | Path) -> None:
    """Save per-parameter variation plots; annotate success count and handle zero successes."""
    raise NotImplementedError("M5: implement and test plot_parameter_variation")
