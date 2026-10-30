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

