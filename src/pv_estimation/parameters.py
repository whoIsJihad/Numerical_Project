"""M1: physical validation and documented dataset-specific parameter heuristics."""

from .contracts import FloatArray, IVData, ParameterBounds, PVConditions


def default_bounds(data: IVData, conditions: PVConditions) -> ParameterBounds:
    """Propose finite physical bounds in canonical order; document heuristic assumptions."""
    raise NotImplementedError("M1: implement and test default_bounds")


def initial_guess(data: IVData, conditions: PVConditions, bounds: ParameterBounds) -> FloatArray:
    """Return a feasible (5,) starting vector; reject incompatible inputs with ValueError."""
    raise NotImplementedError("M1: implement and test initial_guess")


def validate_parameters(theta: FloatArray, bounds: ParameterBounds | None = None) -> None:
    """Check canonical shape, finiteness, physical domain and optional bounds; ValueError on bad input."""
    raise NotImplementedError("M1: implement and test validate_parameters")
