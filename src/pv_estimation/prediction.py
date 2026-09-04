"""M2: PV-specific brackets, current-curve prediction and continuation."""

from .contracts import CurveResult, FloatArray, PVConditions, RootOptions


def predict_curve(
    voltage: FloatArray,
    theta: FloatArray,
    conditions: PVConditions,
    options: RootOptions,
) -> CurveResult:
    """Call M1's checker through solve_root for each voltage; preserve original order.

    Return aligned per-point diagnostics and NaN for failed currents. Warm-start
    only from successful roots. Invalid inputs raise ValueError.
    """
    raise NotImplementedError("M2: implement and test predict_curve")
