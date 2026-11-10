# Physical symbol migration review workspace

Date: 2026-10-30  
Branch: `review/teststation-physical-symbol-migration`

## Safety and provenance

This workspace is isolated from the production/master schematic. The file `TS-V1-M2.9-K-MASTER-REVIEW-BASE.kicad_sch` is an exact byte-for-byte text copy of the current master schematic at the time this branch was created. No wires, labels, junctions, footprints, component values or symbol definitions have been changed in this copy yet.

Source master: `hardware/teststation/V1/CAD/schematics/TS-V1-M2.9-K-MASTER.kicad_sch`  
Source commit at copy time: `3a75a000077a5acd208b5905a345a5e44aa78720`

The original master and legacy baseline remain untouched.

## Verified package pin maps to migrate

- ADS131M06IPBSR: TI PBS 32-pin TQFP. Complete manufacturer pin map and electrical types are recorded in `verification/M2.9-K-COMPONENT-PIN-VERIFICATION-REGISTER.md` and enforced by `verification/scripts/validate_verified_symbol_library.py`.
- TMCS1123A3AQDVGR: TI DVG 10-pin SOIC; exact orderable part confirmed ACTIVE. Pin 2 IN− is an analog input, pins 9 VOC and 10 NC must be present.
- AMC1311BDWVR: TI DWV 8-pin SOIC. Complete manufacturer pin map is recorded in the component register and isolated symbol library.
- The five-symbol draft library is at `symbols/VAZAO-EVSE-Verified-Components.kicad_sym`. Its static and KiCad 10.0.7 parser/export validation passed. It is a library draft, not proof of footprint-pad mapping or approved net intent.

## Migration sequence

1. Keep this exact baseline copy immutable as the comparison point.
2. Create a second working schematic copy from this baseline; do not edit the baseline copy.
3. Replace only embedded library symbol definitions for the target exact part numbers, retaining each placed symbol's UUID, reference, value, position, orientation, unit, pin-instance UUIDs and sheet path.
4. Preserve all existing wires, labels, junctions and no-connect markers byte-for-byte in the first symbol-only migration.
5. Run KiCad 10 CLI ERC and netlist export on both baseline and migrated copy.
6. Compare physical pin-to-net mapping by reference + physical pin number. Report every net delta; do not auto-repair connectivity.
7. Only after package-pad mapping and approved interface intent are signed off may a separate wiring-change copy be created.

## Explicit unresolved engineering gates

- Footprint pad mapping for all symbols remains NOT_VERIFIED.
- Sensor-to-ADC channel assignment and polarity remain NOT_APPROVED.
- The three U19/U2 connections are known physical package pin/function pairings and remain critical review findings:
  - TMCS1123 pin 3 GND ↔ ADS131M06 pin 17 CS
  - TMCS1123 pin 2 IN− ↔ ADS131M06 pin 20 DOUT
  - TMCS1123 pin 8 VS ↔ ADS131M06 pin 19 SCLK
- U19/U2 pin-to-net intended destinations are not inferred.
- E-stop energy-removal and contactor-feedback architecture is not proven by current evidence.
- REF1 remains an unselected/open ADC reference implementation.

## Acceptance criteria for the next migration commit

- A machine-readable comparison proves all placed-symbol UUIDs/references and all wires/labels/junctions are unchanged in the symbol-only migration.
- KiCad 10 CLI loads both schematics without symbol/library errors.
- Static package pin map and electrical-type regression passes.
- Netlist diff is reviewed and contains only documented symbol pin-number/name changes; every physical pin mapping is explicit.
- ERC baseline and migrated report are both archived; improvements are not achieved by suppressing rules or adding arbitrary no-connect markers.
- No fabrication or mains energization approval is implied.



## 2026-11-08 — review-only footprint work

A dedicated `footprints/` directory now holds an isolated U2 candidate footprint and coordinate transcription. U19 remains intentionally without a generated footprint because its pad-centre geometry and board-level insulation design are not yet verified. See `footprints/README.md`. No footprint was assigned to any schematic or PCB.


## 2026-11-08 — workflow #8 and U2 review-only candidate

The U2 ADS131M06IPBSR PBS TQFP-32 review-only footprint candidate, coordinate CSV and static validator were added in commit `9868785dda6340ccf575cc6d15010311ee13eebb`. Workflow [#8](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/42473979552) completed successfully. Its static footprint guard and KiCad 10 schematic export steps passed. Artifact: `evse-symbol-migration-kicad10-7`, ID `13614214105`, SHA-256 `536fb5aab8ac3b8197c73cc68ccf03fcb5058973580f3bc4bc97adb11fff067d`.

Important limitation: CI did not open or render the custom footprint in the KiCad footprint editor and does not prove the coordinate interpretation against independent manufacturer CAD. Candidate remains **REVIEW ONLY / NOT APPROVED**. U19 has no footprint. No schematic assignment, PCB edit, fabrication or mains energization is authorized.


## 2026-11-08 — CI #14: KiCad-native footprint load confirmed

Workflow [#14](https://github.com/AndreVazao/VAZAO-EVSE-Platform/actions/runs/42512318776) completed successfully. In addition to the static geometry/CSV guard and schematic exports, the workflow loaded the U2 review-only footprint through KiCad 10's `pcbnew` API. The test found exactly pads 1–32 and confirmed pad centres/sizes matched the review CSV within 0.001 mm.

Artifact: `evse-symbol-migration-kicad10-7`, ID `13629449480`, SHA-256 `af2533d9e270b77a7671956fdfeb2bb32985b67e75bb45e1413ff24fe352aa9e`.

This confirms KiCad parser/API compatibility and CSV consistency only. It does not independently prove TI drawing transcription, graphical 1:1 appearance, board-level insulation, or manufacturability. The CI also reconfirmed ERC 353 messages / 300 errors / 53 warnings on baseline versus 436 / 383 / 53 on migrated (+83 errors). The candidate remains review-only and unapproved; U19 has no footprint. No production master, legacy baseline, PCB, or wiring was changed.


## 2026-11-10 — TI package drawing re-check

The official TI drawings were visually rechecked. U2's PBS land-pattern drawing 4212229/A explicitly dimensions the opposing pad-row centre lines at 6.20 mm in both axes, supporting the review candidate's ±3.10 mm row centres; the drawing also specifies 0.50 mm pitch and 1.60 × 0.30 mm pads. The TI mechanical top view confirms pin 1 at the lower-left and the numbering progression around the package. This is stronger drawing interpretation evidence, not fabrication approval or independent CAD/physical-sample validation.

For U19, the live TI source is now SBOSA24D Rev. D (revised May 2026). Its DVG0010A outline and land-pattern pages show an asymmetric arrangement (pins 1–2 on one side, pins 3–10 on the other), not a conventional 5+5 SOIC-10. The HV/isolation example is the only viable candidate for further review because TI states 8.1 mm clearance/creepage versus 7.3 mm for IPC nominal, while the datasheet specifies at least 8 mm external clearance/creepage. No U19 footprint or pad coordinates have been generated; the dimension callouts still require a rigorous coordinate reconstruction and PCB-level insulation review.

Sources and detailed limitations are recorded in M2.9-K-U2-U19-PACKAGE-FOOTPRINT-EVIDENCE-REGISTER.md.
