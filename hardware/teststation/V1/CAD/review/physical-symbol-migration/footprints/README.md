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

Added `validate_kicad_footprint_load.py`. It imports KiCad's `pcbnew` Python API, loads the review-only U2 footprint from the custom library, checks that KiCad sees exactly pads 1–32, and compares the loaded pad centres and sizes against the review CSV (0.001 mm tolerance). This closes a gap in the previous CI: the earlier workflow checked footprint text/CSV consistency but never asked KiCad to parse the custom footprint.

The workflow now runs this test after installing KiCad 10. **This check has not yet been confirmed by a completed CI run at the time of this entry.** If the Ubuntu runner's Python environment cannot import `pcbnew`, the workflow must be repaired rather than silently skipping the test.

Scope remains limited: successful loading proves KiCad parser/API compatibility and agreement with the CSV, not that the CSV coordinates are an exact transcription of TI's land-pattern drawing, not PCB-level clearances, and not manufacturing approval. U2 remains `REVIEW_ONLY_NOT_APPROVED`; U19 remains without a footprint.
