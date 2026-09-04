"""M4: scale-aware finite-difference derivatives of residual callbacks."""

from .contracts import FloatArray, JacobianOptions, ParameterBounds, ResidualFunction


def finite_difference_jacobian(
    residual_fn: ResidualFunction,
    theta: FloatArray,
    *,
    bounds: ParameterBounds,
    options: JacobianOptions,
    base_residual: FloatArray | None = None,
) -> FloatArray:
    """Return (N,P) Jacobian, using feasible parameter-scaled FD steps.

    Use supplied base residual if available. Invalid inputs raise ValueError;
    numerical evaluation failures raise EvaluationError. Never mutate theta.
    """
    raise NotImplementedError("M4: implement and test finite_difference_jacobian")
