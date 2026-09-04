"""Implemented scaffold checks only: these do not certify numerical correctness."""

from dataclasses import fields, is_dataclass
from importlib import import_module

import pytest

from pv_estimation import contracts

pytestmark = pytest.mark.scaffold


@pytest.mark.parametrize(
    ("module", "names"),
    [
        ("model", ("equation", "current_derivative", "thermal_voltage")),
        ("data", ("load_iv_csv", "validate_data")),
        ("parameters", ("default_bounds", "initial_guess", "validate_parameters")),
        ("root_solver", ("solve_root",)),
        ("prediction", ("predict_curve",)),
        ("residuals", ("residual_vector",)),
        ("jacobian", ("finite_difference_jacobian",)),
        ("linear_solver", ("solve_linear_system",)),
        ("optimization", ("fit_parameters",)),
        ("pipeline", ("run_baseline",)),
        (
            "experiments",
            (
                "rmse",
                "add_current_noise",
                "run_monte_carlo",
                "summarize_trials",
                "save_results",
                "plot_fit",
                "plot_parameter_variation",
            ),
        ),
    ],
)
def test_public_interfaces_import(module, names):
    imported = import_module(f"pv_estimation.{module}")
    for name in names:
        assert callable(getattr(imported, name))


def test_parameter_order_is_shared():
    assert contracts.PARAMETER_NAMES == ("Iph", "I0", "Rs", "Rsh", "n")


@pytest.mark.parametrize(
    ("record", "required"),
    [
        (contracts.RootResult, {"root", "converged", "reason", "function_evaluations"}),
        (contracts.CurveResult, {"current", "root_results"}),
        (contracts.FitResult, {"theta", "residuals", "converged", "reason", "history"}),
        (contracts.BaselineResult, {"fit", "rmse_a"}),
        (contracts.MonteCarloResult, {"options", "trials"}),
    ],
)
def test_result_contracts_expose_failure_and_diagnostics(record, required):
    assert is_dataclass(record)
    assert required <= {field.name for field in fields(record)}
