"""M1: implement these acceptance tests, then remove each skip decorator."""

import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_baseline_wires_owned_components():
    """Use test doubles to verify data/conditions/options reach the correct components."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_fixed_parameters_to_residuals():
    """Synthetic known curve -> predictions -> near-zero residuals, same order."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_synthetic_data_to_improved_fit():
    """Fit from nearby theta; require objective improvement, not guaranteed unique parameters."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_root_failure_reaches_optimizer():
    """Force inner failure; residual layer raises; optimizer rejects trial or reports failure."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_baseline_failure_has_no_rmse():
    """Failed fit must return BaselineResult.rmse_a=None."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M1: acceptance test and component implementation pending")
def test_seeded_full_noise_pipeline():
    """Same seed/config repeats outcomes except timing; retain failure trials."""
    raise NotImplementedError("M1: replace with setup and meaningful assertions")
