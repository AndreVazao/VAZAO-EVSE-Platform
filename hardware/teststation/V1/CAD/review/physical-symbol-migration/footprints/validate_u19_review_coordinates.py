#!/usr/bin/env python3
"""Validate TI-derived U19 DVG0010A HV coordinates; never grants design approval."""
from __future__ import annotations
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CSV_PATH = ROOT / "TMCS1123A3AQDVGR-DVG0010A-HV-PAD-CENTRES-REVIEW.csv"
EXPECTED_NAMES = {
    1: "IN+", 2: "IN-", 3: "GND", 4: "ALERT", 5: "VREF",
    6: "VOUT", 7: "OC", 8: "VS", 9: "VOC", 10: "NC",
}
SIGNAL_Y = [-4.445, -3.175, -1.905, -0.635, 0.635, 1.905, 3.175, 4.445]
CURRENT_Y = {1: 2.540, 2: -2.540}

def fail(message: str) -> None:
    raise SystemExit("FAIL U19 review coordinate guard: " + message)

with CSV_PATH.open(encoding="utf-8", newline="") as stream:
    rows = list(csv.DictReader(stream))
if len(rows) != 10:
    fail(f"expected 10 rows, got {len(rows)}")
by_pin = {}
for row in rows:
    try:
        pin = int(row["pad_number"])
    except (KeyError, ValueError):
        fail("pad_number must be an integer")
    if pin in by_pin:
        fail(f"duplicate pad number {pin}")
    by_pin[pin] = row
if set(by_pin) != set(range(1, 11)):
    fail(f"pad numbers must be exactly 1..10, got {sorted(by_pin)}")

for pin, row in by_pin.items():
    if row["pin_name"] != EXPECTED_NAMES[pin]:
        fail(f"pin {pin}: expected {EXPECTED_NAMES[pin]}, got {row['pin_name']}")
    if row["source_drawing"] != "4226847/C":
        fail(f"pin {pin}: unexpected source drawing")
    if row["status"] != "REVIEW_ONLY_NOT_APPROVED":
        fail(f"pin {pin}: approval state must remain review-only")
    if row["source_revision"] != "SBOSA24D_REVD":
        fail(f"pin {pin}: source revision must identify current Rev D evidence")
    x, y = float(row["x_mm"]), float(row["y_mm"])
    sx, sy = float(row["pad_x_mm"]), float(row["pad_y_mm"])
    radius = float(row["corner_radius_mm"])
    if abs(x - (-4.875 if pin in (1, 2) else 4.875)) > 1e-6:
        fail(f"pin {pin}: row centre does not match 9.75 mm HV dimension")
    if pin in (1, 2):
        if abs(y - CURRENT_Y[pin]) > 1e-6 or row["side"] != "current_input":
            fail(f"pin {pin}: current-pad centre/side mismatch")
        expected_size = (1.65, 4.41)
    else:
        if abs(y - SIGNAL_Y[pin - 3]) > 1e-6 or row["side"] != "signal":
            fail(f"pin {pin}: signal-pad centre/side mismatch")
        expected_size = (1.65, 0.60)
    if abs(sx - expected_size[0]) > 1e-6 or abs(sy - expected_size[1]) > 1e-6:
        fail(f"pin {pin}: pad size mismatch")
    if abs(radius - 0.05) > 1e-6:
        fail(f"pin {pin}: expected R0.05 typical")
    if row["pad_number"] != str(pin):
        fail(f"pin {pin}: pad number field mismatch")

# Explicit geometric consistency checks from TI's example layout.
row_centre_span = 4.875 - (-4.875)
metal_gap = row_centre_span - 1.65
if abs(row_centre_span - 9.75) > 1e-6 or abs(metal_gap - 8.10) > 1e-6:
    fail("derived HV row separation / metal gap mismatch")
signal_pitch = [SIGNAL_Y[i + 1] - SIGNAL_Y[i] for i in range(7)]
if any(abs(p - 1.27) > 1e-6 for p in signal_pitch):
    fail("signal row pitch must be 1.27 mm")
if abs(CURRENT_Y[1] - CURRENT_Y[2] - 5.08) > 1e-6:
    fail("current pad centre spacing must be 5.08 mm")

print("PASS U19 review CSV: 10 unique pads, TI DVG0010A HV dimensions, 1.27 mm signal pitch, 8.10 mm derived metal gap.")
print("LIMITATION: drawing transcription and static arithmetic only; no CAD, physical sample, PCB insulation, or fabrication approval.")
