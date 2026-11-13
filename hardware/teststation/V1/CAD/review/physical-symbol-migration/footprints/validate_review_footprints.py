#!/usr/bin/env python3
"""Static guardrails for review-only EVSE footprint candidates; not CAD sign-off."""
from __future__ import annotations
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LIB = ROOT / "VAZAO_EVSE_Review.pretty"
U2 = LIB / "ADS131M06IPBSR_PBS_TQFP-32_5x5mm_P0.5mm.kicad_mod"
CSV_FILE = ROOT / "ADS131M06IPBSR-PBS-TQFP32-PAD-CENTRES-REVIEW.csv"

def fail(message: str) -> None:
    raise SystemExit("FAIL " + message)

text = U2.read_text(encoding="utf-8")
if not text.lstrip().startswith('(footprint "ADS131M06IPBSR_PBS_TQFP-32_5x5mm_P0.5mm"'):
    fail("unexpected footprint root/name")
if "REVIEW ONLY" not in text or "NOT FOR FABRICATION" not in text:
    fail("review-only markings missing")
pad_re = re.compile(r'\(pad "([0-9]+)" smd rect \(at (-?[0-9.]+) (-?[0-9.]+)\) \(size ([0-9.]+) ([0-9.]+)\)')
pads = {int(n): tuple(map(float, (x, y, sx, sy))) for n, x, y, sx, sy in pad_re.findall(text)}
if set(pads) != set(range(1, 33)) or len(pads) != 32:
    fail(f"U2 pad numbers must be exactly 1..32; got {sorted(pads)}")
for n, (x, y, sx, sy) in pads.items():
    if abs(sx - 0.3) > 1e-6 and abs(sy - 0.3) > 1e-6:
        fail(f"U2 pad {n}: expected 0.30 mm pad width")
    if abs(sx - 1.6) > 1e-6 and abs(sy - 1.6) > 1e-6:
        fail(f"U2 pad {n}: expected 1.60 mm pad length")
# Check four 8-pad rows and their 0.50 mm pitch.
for side, nums in {
    "bottom": range(1, 9), "right": range(9, 17),
    "top": range(17, 25), "left": range(25, 33),
}.items():
    coords = [(pads[n][0], pads[n][1]) for n in nums]
    varying = [p[0] for p in coords] if side in ("bottom", "top") else [p[1] for p in coords]
    fixed = [p[1] for p in coords] if side in ("bottom", "top") else [p[0] for p in coords]
    varying = sorted(varying)
    if any(abs((b-a)-0.5) > 1e-6 for a,b in zip(varying, varying[1:])):
        fail(f"{side}: pitch is not 0.50 mm")
    if max(fixed)-min(fixed) > 1e-6 or abs(abs(fixed[0])-3.1) > 1e-6:
        fail(f"{side}: row centre is not at ±3.10 mm")
with CSV_FILE.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
if len(rows) != 32 or {int(r["physical_pin"]) for r in rows} != set(range(1,33)):
    fail("coordinate CSV must contain physical pins 1..32 exactly once")
for row in rows:
    n = int(row["physical_pin"])
    expected = pads[n]
    actual = tuple(float(row[k]) for k in ("x_mm","y_mm","pad_size_x_mm","pad_size_y_mm"))
    if any(abs(a-b)>1e-6 for a,b in zip(actual,expected)):
        fail(f"CSV mismatch for physical pin {n}: {actual} != {expected}")
    if row["status"] != "REVIEW_ONLY_NOT_APPROVED" or row["pad_number"] != str(n):
        fail(f"CSV approval/pad-number guard failed for pin {n}")
print("PASS review-only U2 footprint: 32 unique pads, 0.50 mm pitch, 6.20 mm row-centre span, CSV matches; engineering approval remains NOT GRANTED.")
