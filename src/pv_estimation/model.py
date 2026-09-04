"""M1: PV equation checker, current derivative and thermal voltage."""

from .contracts import FloatArray, PVConditions


def thermal_voltage(conditions: PVConditions) -> float:
    """Return per-cell k*T/q in volts; reject invalid conditions with ValueError."""
    raise NotImplementedError("M1: implement and test thermal_voltage")


def equation(current: float, voltage: float, theta: FloatArray, conditions: PVConditions) -> float:
    """Return SDM balance in A, zero at a root; see docs/INTERFACES.md.

    Reject invalid inputs with ValueError; numerical overflow/nonfinite output
    raises EvaluationError. The series-cell factor appears in the exponent.
    """
    raise NotImplementedError("M1: implement and test equation")


def current_derivative(
    current: float, voltage: float, theta: FloatArray, conditions: PVConditions
) -> float:
    """Return d(equation)/dI, using the same validation/failure policy as equation."""
    raise NotImplementedError("M1: implement and test current_derivative")
