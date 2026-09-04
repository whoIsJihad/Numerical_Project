"""Shared interface declarations. Coordinate changes with M1 and affected owners.

No numerical algorithms or automatic validation are implemented here.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal, TypeAlias

import numpy as np
from numpy.typing import NDArray

FloatArray: TypeAlias = NDArray[np.float64]
ScalarFunction: TypeAlias = Callable[[float], float]
ResidualFunction: TypeAlias = Callable[[FloatArray], FloatArray]

PARAMETER_NAMES = ("Iph", "I0", "Rs", "Rsh", "n")


class EvaluationError(RuntimeError):
    """A numerical prediction/residual evaluation could not be completed."""


class LinearSolveError(RuntimeError):
    """A linear system is singular or numerically unsafe to solve."""


@dataclass(frozen=True)
class PVConditions:
    temperature_k: float
    cells_in_series: int = 1


@dataclass(frozen=True)
class IVData:
    voltage: FloatArray
    current: FloatArray
    name: str = "unnamed"
    source: str = "unspecified"


@dataclass(frozen=True)
class ParameterBounds:
    lower: FloatArray
    upper: FloatArray


@dataclass(frozen=True)
class RootOptions:
    method: Literal["newton", "bisection", "hybrid"] = "hybrid"
    x_atol: float = 1e-10
    x_rtol: float = 1e-8
    f_atol: float = 1e-10
    max_iterations: int = 100
    max_bracket_expansions: int = 50
    warm_start: bool = True


@dataclass(frozen=True)
class RootResult:
    root: float | None
    converged: bool
    reason: str
    iterations: int
    function_evaluations: int
    derivative_evaluations: int
    method: str


@dataclass(frozen=True)
class CurveResult:
    current: FloatArray
    root_results: tuple[RootResult, ...]


@dataclass(frozen=True)
class JacobianOptions:
    parameter_scales: FloatArray
    relative_step: float = 1e-6


@dataclass(frozen=True)
class FitOptions:
    jacobian: JacobianOptions
    method: Literal["gauss_newton", "lm"] = "lm"
    max_iterations: int = 100
    max_trial_steps: int = 20
    step_tolerance: float = 1e-8
    objective_tolerance: float = 1e-10
    gradient_tolerance: float = 1e-8
    initial_damping: float = 1e-3


@dataclass(frozen=True)
class FitIteration:
    iteration: int
    theta: FloatArray
    mse: float
    scaled_step_norm: float
    damping: float | None


@dataclass(frozen=True)
class FitResult:
    theta: FloatArray
    residuals: FloatArray | None
    converged: bool
    reason: str
    iterations: int
    residual_evaluations: int
    runtime_seconds: float
    history: tuple[FitIteration, ...]


@dataclass(frozen=True)
class BaselineResult:
    fit: FitResult
    rmse_a: float | None


FitFunction: TypeAlias = Callable[[IVData], FitResult]


@dataclass(frozen=True)
class MonteCarloOptions:
    sigma_current_a: float
    repeats: int = 100
    seed: int = 42


@dataclass(frozen=True)
class MonteCarloTrial:
    index: int
    fit: FitResult
    rmse_a: float | None


@dataclass(frozen=True)
class MonteCarloResult:
    options: MonteCarloOptions
    trials: tuple[MonteCarloTrial, ...]


@dataclass(frozen=True)
class MonteCarloSummary:
    successes: int
    failures: int
    failure_rate: float
    mean_rmse_a: float | None
    parameter_mean: FloatArray | None
    parameter_std: FloatArray | None
