"""Solar-cell equation, dataset loading, and starting parameter values."""

from pathlib import Path

import numpy as np


def validate_data(voltage: np.ndarray, current: np.ndarray) -> None:
    """Check that voltage and current are matching, usable one-dimensional arrays."""
    if not isinstance(voltage, np.ndarray) or not isinstance(current, np.ndarray):
        raise TypeError("voltage and current must be NumPy arrays")
    if voltage.ndim != 1 or current.ndim != 1:
        raise ValueError("voltage and current must be one-dimensional")
    if voltage.size == 0 or current.size == 0:
        raise ValueError("voltage and current cannot be empty")
    if voltage.size != current.size:
        raise ValueError("voltage and current must have the same length")
    if not np.all(np.isfinite(voltage)) or not np.all(np.isfinite(current)):
        raise ValueError("voltage and current cannot contain NaN or infinity")


def validate_parameters(
    theta: np.ndarray, bounds: tuple[np.ndarray, np.ndarray] | None = None
) -> None:
    """Check the five parameters [Iph, I0, Rs, Rsh, n] and optional limits."""
    if not isinstance(theta, np.ndarray) or theta.shape != (5,):
        raise ValueError("theta must be a NumPy array containing five values")
    if not np.all(np.isfinite(theta)):
        raise ValueError("theta cannot contain NaN or infinity")
    iph, i0, rs, rsh, ideality = theta
    if iph < 0 or i0 <= 0 or rs < 0 or rsh <= 0 or ideality <= 0:
        raise ValueError("theta contains a physically impossible value")
    if bounds is None:
        return
    if not isinstance(bounds, tuple) or len(bounds) != 2:
        raise ValueError("bounds must be (lower, upper)")
    lower, upper = bounds
    if not isinstance(lower, np.ndarray) or not isinstance(upper, np.ndarray):
        raise TypeError("lower and upper bounds must be NumPy arrays")
    if lower.shape != (5,) or upper.shape != (5,):
        raise ValueError("lower and upper bounds must each contain five values")
    if not np.all(np.isfinite(lower)) or not np.all(np.isfinite(upper)):
        raise ValueError("bounds cannot contain NaN or infinity")
    if np.any(lower >= upper):
        raise ValueError("every lower bound must be less than its upper bound")
    if np.any(theta < lower) or np.any(theta > upper):
        raise ValueError("theta lies outside the supplied bounds")


def equation(
    current: float, voltage: float, theta: np.ndarray, vt: float, ns: int = 1
) -> float:
    """Return the leftover error after putting a current into the PV equation.

    A result near zero means the current fits this voltage and parameter set.
    """
    validate_parameters(theta)
    if not np.isfinite(current) or not np.isfinite(voltage):
        raise ValueError("current and voltage must be finite")
    if not np.isfinite(vt) or vt <= 0 or not isinstance(ns, int) or ns < 1:
        raise ValueError("vt must be positive and ns must be a positive integer")
    iph, i0, rs, rsh, ideality = theta
    diode_voltage = voltage + current * rs
    exponent = diode_voltage / (ideality * ns * vt)
    with np.errstate(over="raise", invalid="raise"):
        try:
            answer = iph - i0 * np.expm1(exponent) - diode_voltage / rsh - current
        except FloatingPointError as error:
            raise RuntimeError("PV equation overflowed") from error
    return float(answer)


def current_derivative(
    current: float, voltage: float, theta: np.ndarray, vt: float, ns: int = 1
) -> float:
    """Return the slope that Newton's method needs for its next current guess."""
    validate_parameters(theta)
    _, i0, rs, rsh, ideality = theta
    exponent = (voltage + current * rs) / (ideality * ns * vt)
    with np.errstate(over="raise", invalid="raise"):
        try:
            slope = -i0 * np.exp(exponent) * rs / (ideality * ns * vt) - rs / rsh - 1
        except FloatingPointError as error:
            raise RuntimeError("PV derivative overflowed") from error
    return float(slope)


def thermal_voltage(temperature_k: float) -> float:
    """Calculate thermal voltage vt from temperature in kelvin."""
    if not np.isfinite(temperature_k) or temperature_k <= 0:
        raise ValueError("temperature must be finite and greater than zero")
    boltzmann_constant = 1.380649e-23
    electron_charge = 1.602176634e-19
    return boltzmann_constant * temperature_k / electron_charge


def load_data(path: str | Path) -> tuple[np.ndarray, np.ndarray]:
    """Load voltage_v and current_a from the CSV file named by path."""
    data = np.loadtxt(path, delimiter=",", skiprows=1, dtype=np.float64)
    if data.ndim != 2 or data.shape[1] != 2:
        raise ValueError("CSV must contain exactly two columns")
    voltage = data[:, 0]
    current = data[:, 1]
    validate_data(voltage, current)
    return voltage, current


def initial_parameters(
    voltage: np.ndarray, current: np.ndarray, vt: float, ns: int = 1
) -> tuple[np.ndarray, tuple[np.ndarray, np.ndarray], np.ndarray]:
    """Return a reasonable starting point, limits, and step sizes for fitting."""
    validate_data(voltage, current)
    if not np.isfinite(vt) or vt <= 0:
        raise ValueError("vt must be finite and greater than zero")
    if not isinstance(ns, int) or ns < 1:
        raise ValueError("ns must be a positive integer")
    # These limits come from the French RTC single-cell dataset used here.
    theta0 = np.array([max(current), 5e-7, 0.1, 50.0, 1.5], dtype=np.float64)
    lower = np.array([0.0, 1e-12, 0.0, 1.0, 1.0], dtype=np.float64)
    upper = np.array([1.0, 1e-6, 0.5, 100.0, 2.0], dtype=np.float64)
    scales = np.array([1.0, 1e-6, 0.1, 50.0, 1.0], dtype=np.float64)
    bounds = (lower, upper)
    validate_parameters(theta0, bounds)
    return theta0, bounds, scales
