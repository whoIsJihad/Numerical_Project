"""Release-only CI utility: fail if numerical acceptance work remains skipped.

Usage: python tools/check_no_skips.py junit.xml
This is infrastructure, not a project numerical implementation.
"""

import sys
import xml.etree.ElementTree as ET

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python tools/check_no_skips.py junit.xml")
    report = ET.parse(sys.argv[1]).getroot()
    tests = list(report.iter("testcase"))
    skipped = [case for case in tests if case.find("skipped") is not None]
    failed = [
        case for case in tests if case.find("failure") is not None or case.find("error") is not None
    ]
    if not tests or skipped or failed:
        raise SystemExit(
            f"Not complete: {len(tests)} tests, {len(skipped)} skipped, {len(failed)} failed."
        )
    print(f"Complete: {len(tests)} tests, no skips or failures.")
