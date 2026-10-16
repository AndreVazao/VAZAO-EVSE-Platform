#!/usr/bin/env python3
"""Static guardrails for the VAZAO EVSE verified-symbol draft.

This is not a replacement for KiCad's own parser. Run it before the KiCad CLI
load/export check. It validates balanced S-expressions and selected pin maps.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[2] / "symbols" / "VAZAO-EVSE-Verified-Components.kicad_sym"

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

def balanced_sexpressions(text: str) -> bool:
    depth = 0
    in_string = False
    escaped = False
    for ch in text:
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\\\":
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
    starts = list(re.finditer(r'^\\t\\(symbol "([^"]+)"', text, re.M))
    result = {}
    for i, match in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else text.rfind(')')
        result[match.group(1)] = text[match.start():end]
    return result

def read_pins(block: str) -> dict[int, str]:
    pins = {}
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if re.search(r'\\(pin (input|output|bidirectional|tri_state|passive|free|unspecified|power_in|power_out|open_collector|open_emitter) line', line):
            name = None
            number = None
            for look in lines[i + 1:i + 5]:
                nm = re.search(r'\\(name "([^"]*)"', look)
                nu = re.search(r'\\(number "([^"]*)"', look)
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

def main() -> int:
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
    if re.search(r'\\(pin no_connect line', text):
        print("ERROR: unsupported/incorrect no_connect electrical pin type; use passive and document NC status", file=sys.stderr)
        return 2

    blocks = top_symbol_blocks(text)
    failures = []
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
    if failures:
        for failure in failures:
            print("FAIL " + failure, file=sys.stderr)
        return 1
    print("PASS static symbol checks. KiCad CLI load/export validation is still required.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
