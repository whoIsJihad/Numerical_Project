"""Tests for the complete PV parameter-estimation pipeline."""

from pathlib import Path

import numpy as np
import pytest

from current import solve_currents, solve_root
from experiments import add_noise, plot_fit, rmse
from fit import fit_parameters
from model import (
    equation,
    initial_parameters,
    load_data,
    thermal_voltage,
    validate_data,
)
from numerics import jacobian, residuals, solve_linear


def sample_problem() -> tuple:
    """Return a small exact I-V curve used by several tests."""
    voltage = np.linspace(0.0, 0.55, 12)
    theta = np.array([0.76079, 0.31069e-6, 0.03655, 52.88991, 1.47727])
    vt = thermal_voltage(306.15)
    current = solve_currents(voltage, theta, vt)["current"]
    lower = np.array([0.0, 1e-12, 0.0, 1.0, 1.0])
    upper = np.array([1.0, 1e-6, 0.5, 100.0, 2.0])
    scales = np.array([1.0, 1e-6, 0.1, 50.0, 1.0])
    return voltage, current, theta, vt, (lower, upper), scales


def test_load_and_validate_data(tmp_path: Path) -> None:
    """The CSV loader separates the two named columns and rejects bad data."""
    csv_path = tmp_path / "small.csv"
    csv_path.write_text("voltage_v,current_a\n0.0,0.8\n0.5,0.2\n")
    voltage, current = load_data(csv_path)
    assert np.array_equal(voltage, [0.0, 0.5])
    assert np.array_equal(current, [0.8, 0.2])
    with pytest.raises(ValueError):
        validate_data(np.array([0.0]), np.array([0.8, 0.2]))


def test_model_equation_and_derivative() -> None:
    """A solved current balances the equation and the derivative matches a small difference."""
    voltage, current, theta, vt, _, _ = sample_problem()
    assert abs(equation(float(current[4]), float(voltage[4]), theta, vt)) < 1e-8
    step = 1e-6
    numerical_slope = (
        equation(float(current[4] + step), float(voltage[4]), theta, vt)
        - equation(float(current[4] - step), float(voltage[4]), theta, vt)
    ) / (2 * step)
    from model import current_derivative

    assert current_derivative(
        float(current[4]), float(voltage[4]), theta, vt
    ) == pytest.approx(numerical_slope, rel=1e-6)


def test_starting_parameters() -> None:
    """Starting values have five entries and lie inside their limits."""
    voltage, current, _, vt, _, _ = sample_problem()
    theta0, bounds, scales = initial_parameters(voltage, current, vt)
    assert theta0.shape == bounds[0].shape == bounds[1].shape == scales.shape == (5,)
    assert np.all(theta0 >= bounds[0]) and np.all(theta0 <= bounds[1])


def test_all_root_methods() -> None:
    """Newton, bisection, and hybrid all solve the same PV current."""
    voltage, _, theta, vt, _, _ = sample_problem()
    answers = [
        solve_root(float(voltage[5]), theta, vt, initial_guess=0.7, method="newton"),
        solve_root(
            float(voltage[5]), theta, vt, bracket=(-0.5, 1.5), method="bisection"
        ),
        solve_root(
            float(voltage[5]),
            theta,
            vt,
            initial_guess=0.7,
            bracket=(-0.5, 1.5),
            method="hybrid",
        ),
    ]
    assert all(answer["converged"] for answer in answers)
    assert (
        max(answer["root"] for answer in answers)
        - min(answer["root"] for answer in answers)
        < 1e-7
    )


def test_current_curve_keeps_input_order() -> None:
    """Calculated currents line up with unsorted and repeated voltages."""
    _, _, theta, vt, _, _ = sample_problem()
    voltage = np.array([0.4, 0.0, 0.4])
    result = solve_currents(voltage, theta, vt)
    assert np.all(np.isfinite(result["current"]))
    assert result["current"][0] == pytest.approx(result["current"][2])
    assert len(result["roots"]) == 3


def test_residuals_and_jacobian() -> None:
    """Exact data has tiny errors and the Jacobian has 12 rows by 5 columns."""
    voltage, current, theta, vt, bounds, scales = sample_problem()
    errors = residuals(theta, voltage, current, vt)
    table = jacobian(theta, voltage, current, vt, bounds, scales)
    assert np.max(np.abs(errors)) < 1e-8
    assert table.shape == (12, 5)
    assert np.all(np.isfinite(table))


def test_gaussian_elimination() -> None:
    """Row swapping solves a system whose first diagonal entry is zero."""
    matrix = np.array([[0.0, 2.0], [1.0, 3.0]])
    rhs = np.array([4.0, 7.0])
    assert np.allclose(solve_linear(matrix, rhs), [1.0, 2.0])
    with pytest.raises(RuntimeError):
        solve_linear(np.array([[1.0, 2.0], [2.0, 4.0]]), np.array([1.0, 2.0]))


def test_parameter_fit_reduces_error() -> None:
    """LM improves a nearby starting guess without changing that input array."""
    voltage, current, _, vt, bounds, scales = sample_problem()
    theta0 = np.array([0.75, 0.4e-6, 0.05, 50.0, 1.5])
    original = theta0.copy()
    result = fit_parameters(voltage, current, vt, theta0, bounds, scales, max_iter=30)
    assert result["converged"]
    assert result["history"][-1] < result["history"][0]
    assert np.array_equal(theta0, original)


def test_error_and_noise_helpers() -> None:
    """RMSE and seeded noise produce known, repeatable results."""
    assert rmse(np.array([-3.0, 4.0])) == pytest.approx(np.sqrt(12.5))
    current = np.array([1.0, 2.0, 3.0])
    first = add_noise(current, 0.1, np.random.default_rng(42))
    second = add_noise(current, 0.1, np.random.default_rng(42))
    assert np.array_equal(first, second)
    assert np.array_equal(current, [1.0, 2.0, 3.0])


def test_plot(tmp_path: Path) -> None:
    """The plot helper writes a nonempty image file."""
    voltage = np.array([0.0, 0.5])
    current = np.array([0.8, 0.2])
    path = tmp_path / "curve.png"
    plot_fit(voltage, current, current, path)
    assert path.exists() and path.stat().st_size > 0
