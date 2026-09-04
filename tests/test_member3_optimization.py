"""M3: implement these acceptance tests, then remove each skip decorator."""

import pytest

pytestmark = pytest.mark.numerical


@pytest.mark.skip(reason="M3: acceptance test and component implementation pending")
def test_gauss_newton_known_linear_solution():
    """Use residual A@theta-b with a known interior minimizer; check convergence."""
    raise NotImplementedError("M3: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M3: acceptance test and component implementation pending")
def test_lm_improves_nonlinear_objective():
    """Use a small nonlinear callback; accepted history must improve objective."""
    raise NotImplementedError("M3: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M3: acceptance test and component implementation pending")
def test_bounds_and_failed_trials():
    """Record callback inputs; never evaluate outside bounds; reject EvaluationError trials."""
    raise NotImplementedError("M3: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M3: acceptance test and component implementation pending")
def test_failed_initial_evaluation():
    """Initial EvaluationError must produce failed fit with residuals=None."""
    raise NotImplementedError("M3: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M3: acceptance test and component implementation pending")
def test_singular_system_and_iteration_limit():
    """Test honest nonconvergence/reason, not fabricated success."""
    raise NotImplementedError("M3: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M3: acceptance test and component implementation pending")
def test_evaluation_counts_and_input_immutability():
    """Count callback invocations including FD/trials; initial theta unchanged."""
    raise NotImplementedError("M3: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M3: acceptance test and component implementation pending")
def test_programming_errors_are_not_swallowed():
    """A callback raising NotImplementedError must propagate, not become a numerical failure."""
    raise NotImplementedError("M3: replace with setup and meaningful assertions")
