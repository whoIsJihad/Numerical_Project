"""M5: implement these acceptance tests, then remove each skip decorator."""

import pytest

pytestmark = pytest.mark.numerical


@pytest.mark.skip(reason="M5: acceptance test and component implementation pending")
def test_rmse_known_values_and_invalid_input():
    """Residuals [-3,4] give sqrt(12.5); reject empty/nonfinite/wrong shape."""
    raise NotImplementedError("M5: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M5: acceptance test and component implementation pending")
def test_noise_seed_zero_sigma_and_immutability():
    """Equal RNG seeds match; sigma=0 preserves values; original arrays unchanged."""
    raise NotImplementedError("M5: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M5: acceptance test and component implementation pending")
def test_monte_carlo_retains_successes_and_failures():
    """Use fake FitFunction with controlled failures; keep all requested trials."""
    raise NotImplementedError("M5: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M5: acceptance test and component implementation pending")
def test_zero_and_one_success_summaries():
    """No successes gives None metrics; one success gives None sample std."""
    raise NotImplementedError("M5: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M5: acceptance test and component implementation pending")
def test_summary_statistics():
    """Hand-check failure rate, means and sample parameter standard deviations."""
    raise NotImplementedError("M5: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M5: acceptance test and component implementation pending")
def test_strict_json_export_and_metadata():
    """Round trip result export; require seed/options/provenance and no NaN tokens."""
    raise NotImplementedError("M5: replace with setup and meaningful assertions")


@pytest.mark.skip(reason="M5: acceptance test and component implementation pending")
def test_plots_export_with_units():
    """Use tmp_path and Agg backend; assert figures saved; inspect labels/empty-success case."""
    raise NotImplementedError("M5: replace with setup and meaningful assertions")
