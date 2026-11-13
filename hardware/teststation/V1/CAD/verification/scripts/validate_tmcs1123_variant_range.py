#!/usr/bin/env python3
"""Regression guard for TMCS1123 peak range vs TestStation provisional envelope.

Validates arithmetic and declared comparison data only. It does not select a
BOM part, approve the analogue front end, or establish thermal safety.
"""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "netlist" / "M2.9-K-TMCS1123-VARIANT-RANGE-COMPARISON.csv"
ADC_PGA1_FSR_V = 1.2
NOMINAL_RMS_A = 32.0
OVERLOAD_RMS_A = 40.0
TRANSIENT_RMS_A = 48.0
TARGET_PEAK_A = 70.0

EXPECTED = {
    ("A3", 5.0): (False, False, False, False, False),
    ("A3", 3.3): (False, False, False, False, False),
    ("A2", 5.0): (True, False, False, False, False),
    ("A1", 5.0): (True, True, True, True, True),
    ("B1", 3.3): (True, True, True, False, False),
}


def as_bool(value: str) -> bool:
    if value.lower() not in {"true", "false"}:
        raise ValueError(f"invalid boolean: {value!r}")
    return value.lower() == "true"


def fits_peak(peak_a: float, low_a: float, high_a: float) -> bool:
    return low_a <= -peak_a and high_a >= peak_a


def main() -> int:
    if not CSV_PATH.is_file():
        print(f"ERROR: missing {CSV_PATH}", file=sys.stderr)
        return 2

    seen = set()
    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    if len(rows) != len(EXPECTED):
        print(f"ERROR: expected {len(EXPECTED)} rows, found {len(rows)}", file=sys.stderr)
        return 1

    nominal_peak = NOMINAL_RMS_A * math.sqrt(2.0)
    overload_peak = OVERLOAD_RMS_A * math.sqrt(2.0)
    transient_peak = TRANSIENT_RMS_A * math.sqrt(2.0)
    failures = []

    for row in rows:
        variant = row["variant"]
        supply = float(row["supply_v"])
        sensitivity = float(row["sensitivity_v_per_a"])
        low = float(row["linear_min_a"])
        high = float(row["linear_max_a"])
        vref = float(row["zero_current_v"])
        selected = as_bool(row["bom_selected"])

        key = (variant, supply)
        if key not in EXPECTED or key in seen:
            failures.append(f"unexpected or duplicate variant/supply row: {key}")
            continue
        seen.add(key)

        actual = (
            fits_peak(nominal_peak, low, high),
            fits_peak(overload_peak, low, high),
            sensitivity * nominal_peak <= ADC_PGA1_FSR_V,
            fits_peak(transient_peak, low, high),
            fits_peak(TARGET_PEAK_A, low, high),
        )
        declared = (
            as_bool(row["expected_32arms_sensor_linear"]),
            as_bool(row["expected_40arms_sensor_linear"]),
            as_bool(row["expected_32arms_adc_pga1_diff"]),
            as_bool(row["expected_48arms_sensor_linear"]),
            as_bool(row["expected_70a_peak_sensor_linear"]),
        )

        if actual != EXPECTED[key] or actual != declared:
            failures.append(f"{key}: expected {EXPECTED[key]}, CSV {declared}, calculated {actual}")
        if selected:
            failures.append(f"{key}: candidate comparison must not select a BOM variant")
        if not (0.0 < vref < supply):
            failures.append(f"{key}: VREF {vref} V outside supply rails")

        print(
            f"{variant:>2} @ {supply:>3.1f} V | "
            f"32 Arms sensor={'PASS' if actual[0] else 'FAIL'} | "
            f"40 Arms sensor={'PASS' if actual[1] else 'FAIL'} | "
            f"48 Arms sensor={'PASS' if actual[3] else 'FAIL'} | "
            f"±70 A peak sensor={'PASS' if actual[4] else 'FAIL'} | "
            f"32 Arms ADC differential-only={'PASS' if actual[2] else 'FAIL'}"
        )

    if seen != set(EXPECTED):
        failures.append(f"missing rows: {sorted(set(EXPECTED) - seen)}")

    print(f"\nADC PGA=1 differential FSR used for screening: ±{ADC_PGA1_FSR_V:.1f} V")
    print("NOTE: ADC PASS is differential-magnitude screening only; common-mode, absolute maximum, scaling, filtering and source impedance remain unverified.")
    print("NOTE: 40 Arms/10 s and 48 Arms/1 s are provisional analysis scenarios, not approved thermal or fault-current ratings.")
    print("NOTE: sensor linear-range PASS does not establish thermal SOA, conductor/PCB safety, or overload duration capability.")

    if failures:
        for failure in failures:
            print(f"ERROR: {failure}", file=sys.stderr)
        return 1

    print("PASS: variant range arithmetic matches the provisional envelope; no BOM variant is selected.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
