"""M1: load and validate measured I–V data without changing its order."""

from pathlib import Path

from .contracts import IVData


def load_iv_csv(path: str | Path, *, name: str = "unnamed", source: str = "unspecified") -> IVData:
    """Load voltage_v/current_a columns; validate; propagate file errors.

    Invalid CSV or data raises ValueError. Units are volts and amperes.
    """
    raise NotImplementedError("M1: implement and test load_iv_csv")


def validate_data(data: IVData) -> None:
    """Require finite nonempty matching 1-D arrays; raise ValueError otherwise."""
    raise NotImplementedError("M1: implement and test validate_data")
