#!/usr/bin/env python3
"""Load the review-only U2 footprint with KiCad's own pcbnew API.

This verifies parser/API compatibility and pad geometry consistency. It is
not a manufacturer-drawing verification, PCB DRC, assembly, or sign-off.
"""
from __future__ import annotations

import csv
from pathlib import Path
import sys

try:
    import pcbnew
except Exception as exc:
    raise SystemExit(f"FAIL cannot import KiCad pcbnew Python module: {exc}")

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "VAZAO_EVSE_Review.pretty"
NAME = "ADS131M06IPBSR_PBS_TQFP-32_5x5mm_P0.5mm"
CSV_FILE = ROOT / "ADS131M06IPBSR-PBS-TQFP32-PAD-CENTRES-REVIEW.csv"

def fail(message: str) -> None:
    raise SystemExit("FAIL " + message)

fp = pcbnew.FootprintLoad(str(LIB), NAME)
if fp is None:
    fail(f"KiCad pcbnew could not load {LIB / (NAME + '.kicad_mod')}")

pads = {}
for pad in fp.Pads():
    number = str(pad.GetNumber())
    if number in pads:
        fail(f"duplicate pad number {number}")
    pos = pad.GetPosition()
    size = pad.GetSize()
    pads[number] = (
        pcbnew.ToMM(pos.x), pcbnew.ToMM(pos.y),
        pcbnew.ToMM(size.x), pcbnew.ToMM(size.y),
    )

if set(pads) != {str(n) for n in range(1, 33)}:
    fail(f"KiCad loaded unexpected pad set: {sorted(pads)}")

with CSV_FILE.open(encoding="utf-8", newline="") as stream:
    rows = list(csv.DictReader(stream))
if len(rows) != 32:
    fail(f"expected 32 CSV rows, got {len(rows)}")

for row in rows:
    number = str(int(row["physical_pin"]))
    if row["status"] != "REVIEW_ONLY_NOT_APPROVED":
        fail(f"pin {number}: CSV must remain review-only")
    actual = pads[number]
    expected = tuple(float(row[key]) for key in (
        "x_mm", "y_mm", "pad_size_x_mm", "pad_size_y_mm"
    ))
    if any(abs(a - b) > 0.001 for a, b in zip(actual, expected)):
        fail(f"KiCad/CSV geometry mismatch for pad {number}: {actual} != {expected}")

print(f"PASS KiCad pcbnew loaded {NAME}: 32 unique pads; all pad centres/sizes match review CSV within 0.001 mm.")
print("LIMITATION: this confirms KiCad parser/API compatibility only; no TI drawing validation or fabrication approval.")
