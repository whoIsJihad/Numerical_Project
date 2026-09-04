"""Member 1: solar-cell model and measured data. Start with equation()."""


def equation(current, voltage, theta, vt, ns=1):
    """Return Iph-I0*expm1((V+I*Rs)/(n*ns*vt))-(V+I*Rs)/Rsh-I.

    Zero means the current guess fits the equation. Validate physical inputs;
    numerical overflow raises RuntimeError. Do not silently clip the exponent.
    """
    raise NotImplementedError("Member 1: equation")


def current_derivative(current, voltage, theta, vt, ns=1):
    """Return the equation's derivative with respect to current, not parameters."""
    raise NotImplementedError("Member 1: current derivative")


def thermal_voltage(temperature_k):
    """Return per-cell k*T/q; reject nonfinite/nonpositive temperature."""
    raise NotImplementedError("Member 1: thermal voltage")


def load_data(path):
    """Read voltage_v,current_a CSV columns; return validated (voltage, current) arrays."""
    raise NotImplementedError("Member 1: CSV loading")


def validate_data(voltage, current):
    """Require nonempty, finite, matching 1-D arrays; ValueError otherwise."""
    raise NotImplementedError("Member 1: data validation")


def validate_parameters(theta, bounds=None):
    """Check shape (5,), finite physical values and optional (lower, upper) bounds."""
    raise NotImplementedError("Member 1: parameter validation")


def initial_parameters(voltage, current, vt, ns=1):
    """Return (theta0, bounds, scales) using documented dataset-specific heuristics.

    Bounds are two finite (5,) arrays. Scales are positive (5,) typical magnitudes
    used for finite differences and step tests. Starting theta must be feasible.
    """
    raise NotImplementedError("Member 1: starting parameters")
