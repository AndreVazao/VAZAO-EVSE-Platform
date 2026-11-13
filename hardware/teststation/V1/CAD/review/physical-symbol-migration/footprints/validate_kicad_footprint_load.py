#!/usr/bin/env python3
"""Load review-only U2 and U19 candidates using KiCad's pcbnew API.

Checks parser/API compatibility and consistency against the respective review
coordinate CSVs. This is not independent drawing validation or design sign-off.
"""
from __future__ import annotations
import csv
from pathlib import Path
import pcbnew

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "VAZAO_EVSE_Review.pretty"

def fail(message: str) -> None:
    raise SystemExit("FAIL " + message)

def check(name: str, csv_name: str, number_field: str, expected_numbers: set[str], *, invert_y: bool = False) -> None:
    fp = pcbnew.FootprintLoad(str(LIB), name)
    if fp is None:
        fail(f"KiCad could not load {name}.kicad_mod")
    pads = {}
    for pad in fp.Pads():
        number = str(pad.GetNumber())
        if number in pads:
            fail(f"{name}: duplicate pad number {number}")
        pos, size = pad.GetPosition(), pad.GetSize()
        pads[number] = (pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y),
                        pcbnew.ToMM(size.x), pcbnew.ToMM(size.y))
    if set(pads) != expected_numbers:
        fail(f"{name}: unexpected KiCad pad set {sorted(pads)}")
    with (ROOT / csv_name).open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != len(expected_numbers):
        fail(f"{name}: expected {len(expected_numbers)} CSV rows, got {len(rows)}")
    for row in rows:
        number = str(int(row[number_field]))
        if number not in expected_numbers:
            fail(f"{name}: unexpected CSV pad {number}")
        if row["status"] != "REVIEW_ONLY_NOT_APPROVED":
            fail(f"{name} pad {number}: CSV approval state is not review-only")
        actual = pads[number]
        if number_field == "physical_pin":
            keys = ("x_mm", "y_mm", "pad_size_x_mm", "pad_size_y_mm")
        else:
            keys = ("x_mm", "y_mm", "pad_x_mm", "pad_y_mm")
        expected = tuple(float(row[key]) for key in keys)
        if invert_y:
            expected = (expected[0], -expected[1], expected[2], expected[3])
        if any(abs(a-b) > 0.001 for a,b in zip(actual, expected)):
            fail(f"{name} pad {number}: KiCad/CSV mismatch {actual} != {expected}")
    if name.startswith("TMCS1123A3AQDVGR"):
        # TI top-view orientation: pin 1 is above pin 2 on the left/current row;
        # pin 3 is below pin 10 on the right/signal row. KiCad local +Y points down.
        if not (pads["1"][1] < pads["2"][1]):
            fail("U19 orientation: KiCad pin 1 must be above pin 2")
        if not (pads["3"][1] > pads["10"][1]):
            fail("U19 orientation: KiCad pin 3 must be below pin 10")
        if not (pads["1"][0] < pads["3"][0]):
            fail("U19 orientation: current-input row must be left of signal row")
        if abs((pads["3"][0] - pads["1"][0]) - 9.75) > 0.001:
            fail("U19 orientation: row-centre separation must be 9.75 mm")
        if abs((pads["3"][1] - pads["10"][1]) - 8.89) > 0.001:
            fail("U19 orientation: signal-row vertical span must be 8.89 mm")
        print("PASS U19 top-view orientation: pin 1 above 2; pin 3 below 10; current row left of signal row.")
    print(f"PASS KiCad pcbnew loaded {name}: {len(pads)} pads; centres/sizes match review CSV within 0.001 mm.")

check(
    "ADS131M06IPBSR_PBS_TQFP-32_5x5mm_P0.5mm",
    "ADS131M06IPBSR-PBS-TQFP32-PAD-CENTRES-REVIEW.csv",
    "physical_pin", {str(n) for n in range(1,33)}
)
check(
    "TMCS1123A3AQDVGR_DVG0010A_HV_SOIC-10",
    "TMCS1123A3AQDVGR-DVG0010A-HV-PAD-CENTRES-REVIEW.csv",
    "pad_number", {str(n) for n in range(1,11)}, invert_y=True
)
print("U19 transform applied: X_KiCad = X_TI; Y_KiCad = -Y_TI (TI drawing Y points up; KiCad local Y points down).")
print("LIMITATION: KiCad parsing and transformed CSV consistency only; no independent TI drawing verification, visual inspection, PCB insulation assessment, or fabrication approval.")
