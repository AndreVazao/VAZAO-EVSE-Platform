# Review-only footprint workspace

**Nothing in this directory is approved for PCB fabrication or production.** All candidates are isolated engineering evidence and are not assigned to the production schematic or PCB.

## Current status — 2026-11-11

| Device | Candidate | Automated KiCad 10 load | Approval |
|---|---|---|---|
| U2 — ADS131M06IPBSR, PBS TQFP-32 | `VAZAO_EVSE_Review.pretty/ADS131M06IPBSR_PBS_TQFP-32_5x5mm_P0.5mm.kicad_mod` | CI #24/#25 passed | REVIEW ONLY |
| U19 — TMCS1123A3AQDVGR, DVG0010A HV | `VAZAO_EVSE_Review.pretty/TMCS1123A3AQDVGR_DVG0010A_HV_SOIC-10.kicad_mod` | CI #24/#25 passed before the axis-transform correction; rerun required | REVIEW ONLY |

The native-load test previously compared KiCad coordinates directly with the drawing-oriented CSV. That was insufficient for U19 because the CSV defines Y positive toward the top of the TI drawing, while KiCad footprint-local Y positive points down the screen. The U19 candidate and native validator are being corrected to apply the explicit transform **X_KiCad = X_TI; Y_KiCad = −Y_TI**. The next CI run must pass before the corrected candidate can be considered internally validated.

## U2 — ADS131M06IPBSR, TI PBS TQFP-32

Evidence basis: TI ADS131M06 datasheet and official package drawings:
- Mechanical outline 4087735/B.
- Land pattern 4212229/A.

Candidate geometry:
- 32 pads, four sides × eight pads.
- 0.50 mm pitch.
- 1.60 × 0.30 mm rectangular pads.
- Opposing pad-row centre lines 6.20 mm apart; candidate centres at ±3.10 mm.
- Package body outline 5.00 × 5.00 mm nominal.
- TI top-view numbering: pins 1–8 along bottom left-to-right; 9–16 up right side; 17–24 along top right-to-left; 25–32 down left side.

The coordinate CSV is a transcription of the drawing interpretation, not a manufacturer-provided coordinate table. Independently verify all pad centres and numbering against the TI drawing and actual component land pattern. Check mask expansion, paste apertures, courtyard, silkscreen and assembly constraints.

## U19 — TMCS1123A3AQDVGR, TI DVG0010A SOIC-10

Candidate geometry is based on TI drawing 4226847/C, in current datasheet SBOSA24D Rev. D:
- Asymmetric 2+8 arrangement; not a conventional symmetric 5+5 SOIC-10.
- HV/isolation land-pattern option.
- Current pads: 1.65 × 4.41 mm; signal pads: 1.65 × 0.60 mm.
- Signal-side pitch: 1.27 mm.
- Drawing-oriented row-centre separation: 9.75 mm.
- Derived nominal pad-metal gap: 8.10 mm, matching TI's labelled HV option.
- Drawing-oriented numbering: pins 1 and 2 on the left/current side (pin 1 upper, pin 2 lower); pins 3–10 on the right/signal side from lower to upper.

The CSV uses a drawing coordinate frame where X negative is the current-input row, X positive is the signal row, and Y positive points toward the top of the TI drawing. KiCad local coordinates require the explicit vertical transform X_KiCad = X_TI and Y_KiCad = −Y_TI. The footprint editor must still be used to visually confirm pin numbering and orientation against TI's top view.

The 8.10 mm component pad-metal gap does **not** establish finished-board insulation compliance. Review tracks, copper pours, vias, slots, board edges, pollution degree, material group, working voltage, altitude, coating and applicable product standards.

## Required verification before approval

1. Independently reconstruct U2 and U19 pad centres from the dimensioned TI drawings; do not treat CSV equality as independent source verification.
2. Confirm the drawing-to-KiCad axis transforms and pin numbering visually in KiCad 10 at 1:1 scale.
3. Compare against manufacturer CAD or physical samples where available.
4. Inspect solder-mask, paste, courtyard, silkscreen, assembly and fab constraints.
5. Perform full-board insulation coordination for U19.
6. Run physical-pin-to-symbol-pin-to-pad mapping and electrical netlist/ERC regression.
7. Resolve the known +83 ERC error regression before any production consideration.

## CI evidence

- [CI #24](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/42869290910), commit `f822f43cc64cf3b6ad2085739756e6b5b98d63df`, artifact ID `13788278851`.
- [CI #25](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/42869328727), commit `636ba7f9df8247327ea4effd045006b78551c2e6`, artifact ID `13788043116`.

Those runs passed KiCad 10 native loading of both candidates and CSV consistency **before** the explicit U19 axis transform was introduced. They do not validate the corrected transform. A fresh CI run is required.

## Safety and change boundary

- Both candidates remain `REVIEW_ONLY_NOT_APPROVED`.
- No footprint is assigned to the schematic or PCB.
- Production master, legacy baseline and production PCB remain untouched.
- Baseline ERC: 353 messages (300 errors, 53 warnings); migrated ERC: 436 messages (383 errors, 53 warnings), +83 errors.
- No fabrication, PCB release or mains energization is authorized.
