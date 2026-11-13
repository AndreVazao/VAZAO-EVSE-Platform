#!/usr/bin/env python3
"""Guard the review-only U2/U19 pin-to-net intent matrix.

This validator checks source-backed pin functions and observed historical nets.
It deliberately rejects any approved destination assignment: this matrix is
not an approved electrical design specification.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

VERIFICATION = Path(__file__).resolve().parents[1]
MATRIX = VERIFICATION / "netlist" / "M2.9-K-U2-U19-PIN-TO-NET-INTENT-REVIEW.csv"

EXPECTED = {
    "U2": {
        "3": "AIN3N", "4": "AIN3P", "5": "AIN4P", "6": "AIN4N",
        "7": "AIN5N", "8": "AIN5P", "17": "CS", "18": "DRDY",
        "19": "SCLK", "20": "DOUT", "21": "DIN",
    },
    "U19": {
        "1": "IN+", "2": "IN−", "3": "GND", "4": "ALERT", "5": "VREF",
        "6": "VOUT", "7": "OC", "8": "VS", "9": "VOC", "10": "NC",
    },
}
REQUIRED_COLUMNS = {
    "reference", "physical_pin", "datasheet_function", "electrical_role",
    "functional_group_evidence", "baseline_export_net", "migrated_export_net",
    "candidate_interface", "approved_destination_net", "status",
    "evidence_or_notes",
}
ALLOWED_STATUS = {"NOT_APPROVED", "TBD", "BLOCKED_SUSPICIOUS_BASELINE"}
EXPECTED_OBSERVED = {
    ("U2", "17"): ("Net-(U19-GND)", "unconnected"),
    ("U2", "19"): ("Net-(U19-VS)", "unconnected"),
    ("U2", "20"): ("Net-(U19-IN-)", "unconnected"),
    ("U19", "2"): ("Net-(U19-IN-)", "unconnected"),
    ("U19", "3"): ("Net-(U19-GND)", "unconnected"),
    ("U19", "5"): ("/B_L2_I_RET", "unconnected"),
    ("U19", "8"): ("Net-(U19-VS)", "/B_L2_I"),
    ("U19", "9"): ("not present in legacy symbol", "/B_L2_I_RET"),
}
SUSPICIOUS = {
    ("U2", "17"), ("U2", "19"), ("U2", "20"),
    ("U19", "2"), ("U19", "3"), ("U19", "8"),
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not MATRIX.is_file():
        fail(f"intent matrix not found: {MATRIX}")
    with MATRIX.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            fail(f"missing CSV columns: {', '.join(sorted(missing))}")
        rows = list(reader)

    actual = {}
    for row in rows:
        key = (row["reference"].strip(), row["physical_pin"].strip())
        if key in actual:
            fail(f"duplicate pin row: {key[0]}.{key[1]}")
        actual[key] = row
        if key[0] not in EXPECTED or key[1] not in EXPECTED[key[0]]:
            fail(f"unexpected pin row: {key[0]}.{key[1]}")
        expected_function = EXPECTED[key[0]][key[1]]
        if row["datasheet_function"].strip() != expected_function:
            fail(
                f"{key[0]}.{key[1]} function mismatch: "
                f"{row['datasheet_function']!r} != {expected_function!r}"
            )
        if row["status"].strip() not in ALLOWED_STATUS:
            fail(f"invalid/non-review status on {key[0]}.{key[1]}: {row['status']!r}")
        if row["approved_destination_net"].strip():
            fail(f"destination must remain unapproved/blank on {key[0]}.{key[1]}")
        if not row["candidate_interface"].strip() or not row["evidence_or_notes"].strip():
            fail(f"missing review context on {key[0]}.{key[1]}")
        if key in SUSPICIOUS and row["status"].strip() != "BLOCKED_SUSPICIOUS_BASELINE":
            fail(f"known suspicious baseline pair not blocked: {key[0]}.{key[1]}")
        if key in EXPECTED_OBSERVED:
            expected_baseline, expected_migrated = EXPECTED_OBSERVED[key]
            observed = (
                row["baseline_export_net"].strip(),
                row["migrated_export_net"].strip(),
            )
            if observed != (expected_baseline, expected_migrated):
                fail(
                    f"observed net mismatch on {key[0]}.{key[1]}: "
                    f"{observed!r} != {(expected_baseline, expected_migrated)!r}"
                )

    expected_keys = {
        (ref, pin) for ref, pins in EXPECTED.items() for pin in pins
    }
    missing_rows = expected_keys - set(actual)
    extra_rows = set(actual) - expected_keys
    if missing_rows or extra_rows:
        fail(
            f"pin coverage mismatch; missing={sorted(missing_rows)}, "
            f"extra={sorted(extra_rows)}"
        )

    # The legacy functional note groups U19 as Zone B current channel 4.
    for pin in ("5", "6"):
        text = actual[("U2", pin)]["functional_group_evidence"]
        if "U19" not in text or "channel 4" not in text:
            fail(f"U2.{pin} must retain the unapproved channel-4 grouping note")
    for pin in ("3", "4", "7", "8"):
        text = actual[("U2", pin)]["functional_group_evidence"]
        if "not U19's channel" not in text:
            fail(f"U2.{pin} must not be misrepresented as U19's ADC channel")

    print(
        "PASS: U2/U19 review matrix covers all 21 declared pins; "
        "datasheet functions and observed nets match; suspicious legacy "
        "connections remain blocked; no destination net is approved."
    )


if __name__ == "__main__":
    main()
