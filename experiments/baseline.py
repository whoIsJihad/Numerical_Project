"""M1 entry-point template. Run from repo root after editable installation.

Planned usage: python experiments/baseline.py --data data/cell.csv --temperature-k 298.15
No CLI arguments are implemented yet; these are the required next steps.
"""


def main() -> None:
    """M1: parse dataset/conditions/options; load, initialize, run_baseline, report.

    Include --cells-in-series, model/solver choices and parameter scales.
    Display honest failure status and exit nonzero on failed fit. Use M5 plot_fit
    for converged results. Save declared configuration beside outputs.
    """
    raise NotImplementedError("M1: implement baseline entry point after components are ready")


if __name__ == "__main__":
    main()
