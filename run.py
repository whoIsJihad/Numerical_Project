"""Load the RTC dataset and run the complete parameter-fitting pipeline."""

import numpy as np

from experiments import rmse
from fit import fit_parameters
from model import initial_parameters, load_data, thermal_voltage, validate_data


def run_baseline(
    voltage: np.ndarray,
    current: np.ndarray,
    vt: float,
    theta0: np.ndarray,
    bounds: tuple[np.ndarray, np.ndarray],
    scales: np.ndarray,
    ns: int = 1,
    root_method: str = "hybrid",
    fit_method: str = "lm",
) -> dict:
    """Run one fit and return its details and final RMSE."""
    validate_data(voltage, current)
    fit = fit_parameters(
        voltage,
        current,
        vt,
        theta0,
        bounds,
        scales,
        ns,
        root_method,
        fit_method,
    )
    final_rmse = rmse(fit["residuals"]) if fit["converged"] else None
    return {"fit": fit, "rmse": final_rmse}


def main() -> None:
    """Load the French RTC data, fit its parameters, and print the result."""
    voltage, current = load_data("data/rtc_france.csv")
    vt = thermal_voltage(306.15)
    theta0, bounds, scales = initial_parameters(voltage, current, vt, ns=1)
    result = run_baseline(voltage, current, vt, theta0, bounds, scales)

    print("Converged:", result["fit"]["converged"])
    print("Reason:", result["fit"]["reason"])
    print("Parameters [Iph, I0, Rs, Rsh, n]:", result["fit"]["theta"])
    print("RMSE (A):", result["rmse"])


if __name__ == "__main__":
    main()
