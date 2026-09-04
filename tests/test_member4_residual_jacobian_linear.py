"""M4: implement these acceptance tests, then remove each skip decorator."""

import pytest

pytestmark = pytest.mark.numerical


@pytest.mark.skip(reason="M4: acceptance test and component implementation pending")
def test_residual_sign_shape_and_order():
    """Stub prediction; assert predicted-minus-measured and original data ordering."""
    raise NotImplementedError("M4: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M4: acceptance test and component implementation pending")
def test_failed_prediction_raises_evaluation_error():
    """Stub one failed root; do not drop rows or fabricate residuals."""
    raise NotImplementedError("M4: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M4: acceptance test and component implementation pending")
def test_jacobian_matches_analytic_toy_function():
    """Differentiate a known vector callback and compare analytic entries."""
    raise NotImplementedError("M4: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M4: acceptance test and component implementation pending")
def test_jacobian_scales_and_bounds():
    """Test I0-like tiny scale and one-sided steps near bounds; inputs unchanged."""
    raise NotImplementedError("M4: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M4: acceptance test and component implementation pending")
def test_jacobian_failure_propagates():
    """A perturbed callback failure raises EvaluationError rather than a zero column."""
    raise NotImplementedError("M4: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M4: acceptance test and component implementation pending")
def test_linear_solver_pivots_and_solves():
    """Use A=[[0,2],[1,3]], b=[4,7], expected x=[1,2]; inputs unchanged."""
    raise NotImplementedError("M4: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M4: acceptance test and component implementation pending")
def test_linear_solver_invalid_and_singular():
    """Reject invalid shape/nonfinite values; singular matrix raises LinearSolveError."""
    raise NotImplementedError("M4: replace with setup and meaningful assertions")
