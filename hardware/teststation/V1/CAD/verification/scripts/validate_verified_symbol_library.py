#!/usr/bin/env python3
"""Static guardrails for the VAZAO EVSE verified-symbol draft.

This is not a replacement for KiCad's own parser. Run it before the KiCad CLI
load/export check. It validates balanced S-expressions and selected pin maps.
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

CAD_ROOT = Path(__file__).resolve().parents[2]
LIB = CAD_ROOT / "symbols" / "VAZAO-EVSE-Verified-Components.kicad_sym"
PAD_AUDIT = CAD_ROOT / "verification" / "netlist" / "M2.9-K-SYMBOL-TO-FOOTPRINT-PAD-AUDIT.csv"
AUDIT_EXPECTED_COUNTS = {"ADS131M06IPBSR": 32, "AMC1311BDWVR": 8, "TMCS1123A3AQDVGR": 10}
AUDIT_COLUMNS = {"part_number", "package_from_manufacturer_evidence", "physical_pin", "symbol_pin_name", "kicad_electrical_type", "footprint_reference", "footprint_pad_number", "footprint_pad_status", "net_intent_status", "manufacturer_source"}

EXPECTED = {
    "ADS131M06IPBSR": {
        1:"AIN2P", 2:"AIN2N", 3:"AIN3N", 4:"AIN3P", 5:"AIN4P", 6:"AIN4N",
        7:"AIN5N", 8:"AIN5P", 9:"NC", 10:"NC", 11:"NC", 12:"NC",
        13:"AGND", 14:"REFIN", 15:"AVDD", 16:"SYNC/RESET", 17:"CS",
        18:"DRDY", 19:"SCLK", 20:"DOUT", 21:"DIN", 22:"XTAL2",
        23:"XTAL1/CLKIN", 24:"CAP", 25:"DGND", 26:"DVDD", 27:"NC",
        28:"AGND", 29:"AIN0P", 30:"AIN0N", 31:"AIN1N", 32:"AIN1P",
    },
    "AMC1311BDWVR": {
        1:"VDD1", 2:"IN", 3:"SHTDN", 4:"GND1",
        5:"GND2", 6:"OUTN", 7:"OUTP", 8:"VDD2",
    },
    "TMCS1123A3AQDVGR": {
        1:"IN+", 2:"IN−", 3:"GND", 4:"ALERT", 5:"VREF",
        6:"VOUT", 7:"OC", 8:"VS", 9:"VOC", 10:"NC",
    },
}

# Electrical types that are safety-/ERC-relevant and explicitly checked against
# the manufacturers' pin-function tables. This is not a substitute for full review.
EXPECTED_TYPES = {
    "ADS131M06IPBSR": {
        1:"input", 2:"input", 3:"input", 4:"input", 5:"input", 6:"input", 7:"input", 8:"input",
        9:"passive", 10:"passive", 11:"passive", 12:"passive", 13:"power_in",
        14:"input", 15:"power_in", 16:"input", 17:"input", 18:"output",
        19:"input", 20:"output", 21:"input", 22:"output", 23:"input",
        24:"passive", 25:"power_in", 26:"power_in", 27:"passive", 28:"power_in",
        29:"input", 30:"input", 31:"input", 32:"input",
    },
    "AMC1311BDWVR": {
        1:"power_in", 2:"input", 3:"input", 4:"power_in",
        5:"power_in", 6:"output", 7:"output", 8:"power_in",
    },
    "TMCS1123A3AQDVGR": {
        1:"input", 2:"input", 3:"power_in", 4:"open_collector",
        5:"output", 6:"output", 7:"open_collector", 8:"power_in",
        9:"input", 10:"passive",
    },
}

def balanced_sexpressions(text: str) -> bool:
    depth = 0
    in_string = False
    escaped = False
    for ch in text:
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and not in_string

def top_symbol_blocks(text: str) -> dict[str, str]:
    starts = list(re.finditer(r'^\t\(symbol "([^"]+)"', text, re.M))
    result = {}
    for i, match in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else text.rfind(')')
        result[match.group(1)] = text[match.start():end]
    return result

def read_pins(block: str) -> dict[int, str]:
    pins = {}
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if re.search(r'\(pin (input|output|bidirectional|tri_state|passive|free|unspecified|power_in|power_out|open_collector|open_emitter) line', line):
            name = None
            number = None
            for look in lines[i + 1:i + 5]:
                nm = re.search(r'\(name "([^"]*)"', look)
                nu = re.search(r'\(number "([^"]*)"', look)
                if nm:
                    name = nm.group(1)
                if nu:
                    number = nu.group(1)
            if name is None or number is None:
                raise ValueError(f"pin missing name/number near: {line.strip()}")
            n = int(number)
            if n in pins:
                raise ValueError(f"duplicate physical pin number {n}")
            pins[n] = name
    return pins

def read_pin_types(block: str) -> dict[int, str]:
    types = {}
    for match in re.finditer(r'\(pin ([a-z_]+) line([\s\S]*?)\(number "([0-9]+)"', block):
        pin_type, body, number = match.groups()
        n = int(number)
        if n in types:
            raise ValueError(f"duplicate physical pin type entry {n}")
        types[n] = pin_type
    return types

def validate_pad_audit() -> list[str]:
    """Check audit completeness without pretending unverified mappings are approved."""
    failures = []
    if not PAD_AUDIT.exists():
        return [f"symbol-to-footprint audit CSV not found: {PAD_AUDIT}"]
    try:
        with PAD_AUDIT.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            if set(reader.fieldnames or []) != AUDIT_COLUMNS:
                return [f"pad audit CSV columns mismatch: {reader.fieldnames}"]
            rows = list(reader)
    except (OSError, csv.Error) as exc:
        return [f"could not read pad audit CSV: {exc}"]

    counts = {part: 0 for part in AUDIT_EXPECTED_COUNTS}
    seen = set()
    for line_number, row in enumerate(rows, start=2):
        part = row["part_number"]
        if part not in counts:
            failures.append(f"pad audit line {line_number}: unexpected part {part!r}")
            continue
        counts[part] += 1
        pin_text = row["physical_pin"].strip()
        if not pin_text.isdigit():
            failures.append(f"pad audit line {line_number}: invalid physical pin {pin_text!r}")
            continue
        key = (part, int(pin_text))
        if key in seen:
            failures.append(f"pad audit line {line_number}: duplicate part/pin {key}")
        seen.add(key)
        if not row["symbol_pin_name"].strip():
            failures.append(f"pad audit line {line_number}: blank symbol pin name")
        if not row["manufacturer_source"].startswith("https://"):
            failures.append(f"pad audit line {line_number}: manufacturer source must be HTTPS")
        if row["footprint_pad_status"] != "NOT_VERIFIED":
            failures.append(f"pad audit line {line_number}: footprint status must remain NOT_VERIFIED")
        if row["net_intent_status"] != "NOT_APPROVED":
            failures.append(f"pad audit line {line_number}: net intent status must remain NOT_APPROVED")
        if row["footprint_reference"].strip() or row["footprint_pad_number"].strip():
            failures.append(f"pad audit line {line_number}: unreviewed footprint/pad fields must remain blank")

    if len(rows) != sum(AUDIT_EXPECTED_COUNTS.values()):
        failures.append(f"pad audit row count {len(rows)} != expected {sum(AUDIT_EXPECTED_COUNTS.values())}")
    for part, expected_count in AUDIT_EXPECTED_COUNTS.items():
        if counts[part] != expected_count:
            failures.append(f"pad audit {part}: {counts[part]} rows != expected {expected_count}")
        expected_pins = set(range(1, expected_count + 1))
        actual_pins = {pin for p, pin in seen if p == part}
        if actual_pins != expected_pins:
            failures.append(f"pad audit {part}: pin coverage {sorted(actual_pins)} != {sorted(expected_pins)}")
    if not failures:
        print("PASS symbol-to-footprint audit CSV: 50 unique pin rows; mappings remain explicitly unverified")
    return failures


def main() -> int:
    audit_failures = validate_pad_audit()
    if not LIB.exists():
        print(f"ERROR: library not found: {LIB}", file=sys.stderr)
        return 2
    text = LIB.read_text(encoding="utf-8")
    if not text.lstrip().startswith("(kicad_symbol_lib"):
        print("ERROR: wrong library root token", file=sys.stderr)
        return 2
    if not balanced_sexpressions(text):
        print("ERROR: unbalanced S-expressions or unterminated string", file=sys.stderr)
        return 2
    if re.search(r'\(pin no_connect line', text):
        print("ERROR: unsupported/incorrect no_connect electrical pin type; use passive and document NC status", file=sys.stderr)
        return 2

    blocks = top_symbol_blocks(text)
    failures = list(audit_failures)
    for symbol, expected in EXPECTED.items():
        if symbol not in blocks:
            failures.append(f"{symbol}: missing top-level symbol")
            continue
        actual = read_pins(blocks[symbol])
        if actual != expected:
            missing = sorted(set(expected.items()) - set(actual.items()))
            extra = sorted(set(actual.items()) - set(expected.items()))
            failures.append(f"{symbol}: pin map mismatch; missing/wrong={missing}; extra/wrong={extra}")
        else:
            print(f"PASS {symbol}: {len(actual)} unique physical pin numbers match expected map")
        actual_types = read_pin_types(blocks[symbol])
        expected_types = EXPECTED_TYPES[symbol]
        if set(expected_types) != set(expected):
            failures.append(
                f"{symbol}: checker configuration error; electrical-type pins "
                f"{sorted(expected_types)} do not cover pin map {sorted(expected)}"
            )
        type_errors = [(pin, expected_types[pin], actual_types.get(pin)) for pin in expected_types
                       if actual_types.get(pin) != expected_types[pin]]
        if type_errors:
            failures.append(f"{symbol}: electrical pin type mismatch {type_errors}")
        else:
            print(f"PASS {symbol}: {len(expected_types)} electrical pin types match reviewed expectations")
    if failures:
        for failure in failures:
            print("FAIL " + failure, file=sys.stderr)
        return 1
    print("PASS static symbol checks. KiCad CLI load/export validation is still required.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
