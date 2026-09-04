"""M1: implement these acceptance tests, then remove each skip decorator."""

import pytest

pytestmark = pytest.mark.numerical


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_equation_matches_explicit_rs_zero():
    """Set Rs=0; direct SDM current must make equation zero."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_current_derivative_matches_central_difference():
    """Compare analytic current derivative with independent central differences."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_thermal_voltage_and_series_cell_factor():
    """Verify k*T/q and Ns effect in exponent; reject bad temperature/Ns."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_csv_loading_and_order():
    """Use tmp_path CSV; verify columns, values, original order, name/source."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_invalid_data_rejected():
    """Empty, mismatched, multidimensional and nonfinite arrays raise ValueError."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_invalid_parameters_rejected():
    """Test canonical order, physical domains, shapes and bound violations."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_bounds_and_initial_guess_are_feasible():
    """Verify documented heuristics return a finite physical feasible (5,) vector."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")
