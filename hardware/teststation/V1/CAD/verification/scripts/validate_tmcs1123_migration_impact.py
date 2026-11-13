#!/usr/bin/env python3
"""Validate observed baseline/migrated pin impact for all six TMCS1123 sensors.

This is a review-evidence guard, not an approved pin-to-net specification.
All destination-net fields must remain blank until engineering approval.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

VERIFICATION = Path(__file__).resolve().parents[1]
MATRIX = VERIFICATION / "netlist" / "M2.9-K-TMCS1123-ALL-CHANNELS-MIGRATION-IMPACT.csv"

CHANNELS = {
    "U15": ("A", "L1", "3"),
    "U16": ("A", "L2", "4"),
    "U17": ("A", "L3", "5"),
    "U18": ("B", "L1", "3"),
    "U19": ("B", "L2", "4"),
    "U20": ("B", "L3", "5"),
}
PINS = {
    "1": ("IN+", "analog_current_input", "input", "input"),
    "2": ("IN−", "analog_current_input", "output", "input"),
    "3": ("GND", "power_input", "power_in", "power_in"),
    "4": ("ALERT", "open_drain_output", "output", "open_collector"),
    "5": ("VREF", "analog_output", "output", "output"),
    "6": ("VOUT", "analog_output", "output", "output"),
    "7": ("OC", "open_drain_output", "output", "open_collector"),
    "8": ("VS", "power_input", "power_in", "power_in"),
    "9": ("VOC", "analog_input", "not_present", "input"),
    "10": ("NC", "passive", "not_present", "passive"),
}
REQUIRED_COLUMNS = {
    "reference", "zone", "phase", "adc_channel_group", "physical_pin",
    "datasheet_function", "electrical_role", "baseline_symbol_pin_type",
    "migrated_symbol_pin_type", "baseline_export_net", "migrated_export_net",
    "observed_change", "status", "approved_destination_net", "evidence_or_notes",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def expected_nets(ref: str, pin: str, zone: str, phase: str) -> tuple[str, str]:
    signal = f"/{zone}_{phase}_I"
    returned = f"/{zone}_{phase}_I_RET"
    old_unconnected = {
        "1": f"unconnected-({ref}-IN+-Pad1)",
        "2": f"unconnected-({ref}-IN--Pad2)",
        "3": f"unconnected-({ref}-GND-Pad3)",
        "4": f"unconnected-({ref}-ALERT-Pad4)",
        "6": f"unconnected-({ref}-VOUT-Pad6)",
        "7": f"unconnected-({ref}-OC-Pad7)",
        "8": f"unconnected-({ref}-VS-Pad8)",
    }
    new_unconnected = {
        "1": f"unconnected-({ref}-IN+-Pad1)",
        "2": f"unconnected-({ref}-IN−-Pad2)",
        "3": f"unconnected-({ref}-GND-Pad3)",
        "4": f"unconnected-({ref}-ALERT-Pad4)",
        "5": f"unconnected-({ref}-VREF-Pad5)",
        "6": f"unconnected-({ref}-VOUT-Pad6)",
        "7": f"unconnected-({ref}-OC-Pad7)",
        "10": f"unconnected-({ref}-NC-Pad10)",
    }
    if pin == "1":
        return old_unconnected[pin], new_unconnected[pin]
    if pin == "2":
        return ("Net-(U19-IN-)", new_unconnected[pin]) if ref == "U19" else (old_unconnected[pin], new_unconnected[pin])
    if pin == "3":
        return ("Net-(U19-GND)", new_unconnected[pin]) if ref == "U19" else (old_unconnected[pin], new_unconnected[pin])
    if pin == "4":
        return old_unconnected[pin], new_unconnected[pin]
    if pin == "5":
        return returned, new_unconnected[pin]
    if pin == "6":
        return old_unconnected[pin], new_unconnected[pin]
    if pin == "7":
        return old_unconnected[pin], new_unconnected[pin]
    if pin == "8":
        old = "Net-(U19-VS)" if ref == "U19" else old_unconnected[pin]
        return old, signal
    if pin == "9":
        return "not present in legacy symbol", returned
    if pin == "10":
        return "not present in legacy symbol", new_unconnected[pin]
    raise AssertionError(pin)


def expected_status(ref: str, pin: str) -> str:
    if ref == "U19" and pin in {"2", "3"}:
        return "BLOCKED_SUSPICIOUS_BASELINE"
    if pin in {"5", "8", "9"}:
        return "BLOCKED_ANCHOR_DISPLACEMENT"
    return "OBSERVED_REVIEW_ONLY"


def main() -> None:
    if not MATRIX.is_file():
        fail(f"migration-impact matrix not found: {MATRIX}")
    with MATRIX.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            fail(f"missing columns: {', '.join(sorted(missing))}")
        rows = list(reader)

    actual = {}
    for row in rows:
        ref = row["reference"].strip()
        pin = row["physical_pin"].strip()
        key = (ref, pin)
        if key in actual:
            fail(f"duplicate row {ref}.{pin}")
        actual[key] = row
        if ref not in CHANNELS or pin not in PINS:
            fail(f"unexpected component/pin {ref}.{pin}")

        zone, phase, channel = CHANNELS[ref]
        function, role, old_type, new_type = PINS[pin]
        expected = {
            "zone": zone,
            "phase": phase,
            "adc_channel_group": channel,
            "datasheet_function": function,
            "electrical_role": role,
            "baseline_symbol_pin_type": old_type,
            "migrated_symbol_pin_type": new_type,
            "status": expected_status(ref, pin),
        }
        for field, value in expected.items():
            if row[field].strip() != value:
                fail(f"{ref}.{pin} {field} mismatch: {row[field]!r} != {value!r}")

        baseline_net, migrated_net = expected_nets(ref, pin, zone, phase)
        if row["baseline_export_net"].strip() != baseline_net:
            fail(f"{ref}.{pin} baseline net mismatch")
        if row["migrated_export_net"].strip() != migrated_net:
            fail(f"{ref}.{pin} migrated net mismatch")
        if row["approved_destination_net"].strip():
            fail(f"{ref}.{pin} must not have an approved destination net")
        if not row["observed_change"].strip() or not row["evidence_or_notes"].strip():
            fail(f"{ref}.{pin} missing evidence/change note")

    expected_keys = {(ref, pin) for ref in CHANNELS for pin in PINS}
    if set(actual) != expected_keys:
        fail(
            f"coverage mismatch: missing={sorted(expected_keys - set(actual))}; "
            f"extra={sorted(set(actual) - expected_keys)}"
        )

    print(
        "PASS: all 60 TMCS1123 pins across U15-U20 match the recorded "
        "baseline/migrated exports and TI pin functions; VREF/VS/VOC "
        "anchor-displacement rows remain blocked; no destination net is approved."
    )


if __name__ == "__main__":
    main()
