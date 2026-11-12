# Review-only footprint workspace

**Nothing in this directory is approved for PCB fabrication or production.** These files are isolated engineering candidates and are not assigned to the production schematic or PCB.

## U2 — ADS131M06IPBSR, TI PBS TQFP-32

Candidate: `VAZAO_EVSE_Review.pretty/ADS131M06IPBSR_PBS_TQFP-32_5x5mm_P0.5mm.kicad_mod`

Evidence basis: TI ADS131M06 datasheet, drawing PBS land pattern 4212229/A (PDF page 100), visually reviewed in the source PDF.
- 32 pads, four sides × eight pads.
- 0.50 mm pitch.
- 1.60 × 0.30 mm rectangular pads.
- Opposing pad-row centre lines 6.20 mm apart; candidate centres at ±3.10 mm.
- Package body outline 5.00 × 5.00 mm, from TI PBS mechanical drawing 4087735/B.
- Pin numbering follows the TI top view: pins 1–8 along bottom left-to-right; 9–16 up right side; 17–24 along top right-to-left; 25–32 down left side.

The coordinate CSV is a transcription of the drawing interpretation, not a manufacturer-provided coordinate table. It must be independently checked against the drawing image and the actual component land pattern before use. In particular, verify pad-row centre dimensions, pad numbering/orientation, mask expansion, paste aperture design, courtyard and silkscreen clearances.

### Required verification before approval
1. Independently reconstruct all 32 pad centres from TI drawing 4212229/A and verify the coordinate CSV.
2. Verify numbering against TI package top view and the symbol's physical pin numbers.
3. Load the footprint in KiCad 10; inspect 1:1 rendering and run footprint checks.
4. Compare against a physical sample or manufacturer CAD data if available.
5. Review solder-mask/paste rules, courtyard, assembly and PCB fab constraints.
6. Run the full symbol-pin-to-pad audit; no footprint assignment is allowed until signed off.

## U19 — TMCS1123A3AQDVGR, TI DVG SOIC-10

**No footprint generated yet.** Although TI Rev D shows IPC and HV/isolation land-pattern options, exact pad-centre coordinates and complete PCB-level creepage/clearance assessment remain unresolved. Do not substitute a generic SOIC-10 footprint. The 8.1 mm HV option is a candidate for study only; it is not proof of finished-board insulation compliance.

## Safety boundary

No master schematic, legacy baseline, production PCB or wiring was modified. No footprint property was assigned. No fabrication, PCB release, or mains energization is authorized.


## 2026-11-08 — CI run #8

- Workflow: [run #8](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/42473979552), commit `9868785dda6340ccf575cc6d15010311ee13eebb`.
- Result: completed / success. The static review-footprint geometry/CSV guard passed; KiCad 10 CLI installation/version confirmation passed; baseline and migrated schematic exports passed; evidence upload passed.
- Artifact: `evse-symbol-migration-kicad10-7`, ID `13614214105`, 17,784 bytes, expires 2026-12-08.
- Artifact SHA-256: `536fb5aab8ac3b8197c73cc68ccf03fcb5058973580f3bc4bc97adb11fff067d`.

**Scope limitation:** the workflow ran the Python static guard and KiCad CLI schematic exports. It did not load/render the custom footprint in KiCad's footprint editor, verify its manufacturability, or prove the interpreted TI dimensions. The candidate remains review-only and unapproved.


## 2026-11-08 — KiCad-native footprint load guard added

Added `validate_kicad_footprint_load.py`. It imports KiCad's `pcbnew` Python API, loads the review-only U2 footprint from the custom library, checks that KiCad sees exactly pads 1–32, and compares the loaded pad centres and sizes against the review CSV (0.001 mm tolerance). This asks KiCad itself to parse the custom footprint rather than relying only on text/CSV consistency.

The workflow runs this test after installing KiCad 10. The completed CI result is recorded below.


## 2026-11-08 — CI #14: KiCad-native footprint load passed

- Workflow: [run #14](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/42512318776).
- Workflow head commit: `0650ba92548c6e18fb2438deef7dfb7a3dcea29d`.
- Job `validate-review-schematics`: completed / success.
- Confirmed successful steps: verified-symbol pin-map regression; static review-footprint geometry/CSV guard; KiCad 10 installation and version; **KiCad `pcbnew` API load of the custom U2 footprint**; baseline/migrated schematic ERC and netlist exports; artifact upload.
- The native load test reported that KiCad loaded exactly pads 1–32 and that pad centres/sizes matched the review CSV within 0.001 mm.
- Artifact: `evse-symbol-migration-kicad10-7`, ID `13629449480`, 17,786 bytes, expires 2026-12-08.
- SHA-256: `af2533d9e270b77a7671956fdfeb2bb32985b67e75bb45e1413ff24fe352aa9e`.

**Correction to the previous entry:** the KiCad-native load check is no longer pending; CI #14 confirms it passed. The check proves parser/API compatibility and agreement between the loaded footprint and the review CSV only. It does not independently validate the coordinate transcription against TI's drawing, perform a graphical 1:1 footprint-editor inspection, establish board-level clearances, or approve fabrication. U2 remains `REVIEW_ONLY_NOT_APPROVED`; U19 remains without a generated footprint.

The same CI run re-confirmed the unresolved schematic comparison: baseline ERC 353 messages (300 errors, 53 warnings); migrated ERC 436 messages (383 errors, 53 warnings), a regression of 83 errors. This workflow is a successful validation/evidence pipeline, **not** an electrical-design pass.


## 2026-11-10 — CI #17 repeat validation

Workflow [#17](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/42807619534) completed successfully on commit 5199baad11f8d787ade6785307cde06fe75f5aff. All steps passed, including static footprint geometry/CSV validation, KiCad 10 version confirmation, KiCad pcbnew API loading of the U2 candidate, baseline/migrated schematic exports, and evidence upload.

Artifact: evse-symbol-migration-kicad10-7, ID 13761195036, 17,784 bytes, expires 2026-12-10. SHA-256: af0c882993c9e20acd74e2cc83459cbad50abd6bfca93aa50e6ce6e5217311e0.

This repeat run confirms the review footprint remains parseable by KiCad 10 and internally consistent with its coordinate CSV. It does not validate the manufacturer's drawing independently, perform graphical 1:1 inspection, or approve fabrication. U2 remains review-only/not approved; U19 remains without a footprint.


## 2026-11-10 — U19 HV pad-centre reconstruction (review-only)

A coordinate transcription has been added at `TMCS1123A3AQDVGR-DVG0010A-HV-PAD-CENTRES-REVIEW.csv`. It derives nominal pad centres from TI drawing 4226847/C:
- HV row-centre separation: 9.75 mm → X = ±4.875 mm.
- Eight signal pads: 7 × 1.27 mm pitch, symmetric → Y = ±0.635, ±1.905, ±3.175, ±4.445 mm.
- Two current pads: 5.08 mm centre spacing, symmetric → Y = ±2.540 mm.
- HV metal dimensions: current pads 1.65 × 4.41 mm; signal pads 1.65 × 0.60 mm.
- Derived metal gap between rows: 9.75 − 1.65 = 8.10 mm, matching TI's explicit 8.1 mm label.

The CSV axes are defined relative to the centre of the pattern: X negative is the current-input side, X positive is the signal side; Y positive points toward the upper edge of TI's drawing. The pad-number sequence follows TI's package top view (1 then 2 on the left, 3 at the bottom of the signal row through 10 at the top). A KiCad footprint orientation transform must be documented and visually checked; do not assume the CSV axes match KiCad's screen axes.

**Status: coordinate transcription REVIEW ONLY; no U19 footprint generated or assigned.** This is a mathematical reconstruction of TI's example drawing, not manufacturer CAD or physical sample validation. The 8.1 mm component pad gap does not establish finished-board insulation compliance. Full PCB creepage/clearance assessment remains mandatory.


## 2026-11-10 — U19 HV footprint candidate created (review-only)

Candidate: `VAZAO_EVSE_Review.pretty/TMCS1123A3AQDVGR_DVG0010A_HV_SOIC-10.kicad_mod`.

The candidate is generated from the ten-pad CSV transcription of TI drawing 4226847/C. It uses the TI HV dimensions and pad numbering: two large current-input pads on the left, eight signal pads on the right, with 1.27 mm signal pitch and 8.10 mm derived metal gap. The nominal R0.05 corner treatment is represented using KiCad round-rectangle pads; actual rendered corner geometry must still be inspected against the TI drawing.

The KiCad-native loader `validate_kicad_footprint_load.py` now loads both U2 and U19 and checks all pad centres and dimensions against their respective review CSVs with 0.001 mm tolerance. The CI workflow includes the U19 CSV arithmetic/numbering guard.

**Status: candidate exists, but remains REVIEW_ONLY_NOT_APPROVED.** The native loader proves KiCad can parse the file and that its geometry matches the CSV; it does not independently prove the CSV against TI's drawing. Before approval, inspect the footprint at 1:1 in KiCad, verify the asymmetric pin numbering/orientation visually, compare with a physical sample or manufacturer CAD, and complete board-level insulation coordination. Do not assign this footprint to a production PCB yet.
