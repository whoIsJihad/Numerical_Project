"""M3: deterministic GN/LM using M4's Jacobian and pivoted linear solve."""

from .contracts import FitOptions, FitResult, FloatArray, ParameterBounds, ResidualFunction


def fit_parameters(
    residual_fn: ResidualFunction,
    initial_theta: FloatArray,
    bounds: ParameterBounds,
    options: FitOptions,
) -> FitResult:
    """Fit residual_fn via options.method ('gauss_newton' or 'lm').

    Validate inputs, handle bounds and failed trials, count all residual calls,
    and record accepted iterations. Numerical nonconvergence is a failed result;
    malformed inputs raise ValueError. Do not swallow NotImplementedError.
    """
    raise NotImplementedError("M3: implement and test fit_parameters")
