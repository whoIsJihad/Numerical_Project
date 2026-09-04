"""M4: turn predicted current curves into optimizer residual vectors."""

from .contracts import FloatArray, IVData, PVConditions, RootOptions


def residual_vector(
    theta: FloatArray, data: IVData, conditions: PVConditions, root_options: RootOptions
) -> FloatArray:
    """Return predicted-minus-measured (N,) errors in A.

    Call M2 predict_curve; raise EvaluationError on any failed root. Do not
    return partial vectors or omit failed measurements. Preserve data ordering.
    """
    raise NotImplementedError("M4: implement and test residual_vector")
