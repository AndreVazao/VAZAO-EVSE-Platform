# VAZAO EVSE verified-component symbol library — controlled draft

Date: 2026-10-16  
Status: **Draft generated; not yet validated by KiCad CLI or approved for schematic migration.**

## Scope

`VAZAO-EVSE-Verified-Components.kicad_sym` is a separate, non-destructive symbol-library draft for three critical IC families whose cached legacy symbols have known pin omissions or pin-number/function errors:

- `ADS131M06IPBSR` — 32 physical pins represented, using the manufacturer PBS/TQFP pin table.
- `AMC1311BDWVR` — 8 physical pins represented, using the manufacturer DWV/SOIC pin table.
- `TMCS1123A3AQDVGR` — 10 physical pins represented using the TMCS1123 10-pin package function table.

The legacy cache library and native master schematic have **not** been changed by this work. The new library is deliberately not yet assigned to schematic instances.

## Verification boundaries

Manufacturer pin-number/function references:

- ADS131M06: [TI datasheet](https://www.ti.com/lit/ds/symlink/ads131m06.pdf) and [exact ADS131M06IPBSR orderable page](https://www.ti.com/product/ADS131M06/part-details/ADS131M06IPBSR).
- AMC1311: [TI datasheet](https://www.ti.com/lit/ds/symlink/amc1311.pdf) and [AMC1311BDWVR orderable page](https://www.ti.com/product/AMC1311/part-details/AMC1311BDWVR).
- TMCS1123: [TI datasheet](https://www.ti.com/lit/ds/symlink/tmcs1123.pdf) and [TMCS1123 product page](https://www.ti.com/product/TMCS1123).

The TMCS1123 function table does not, by itself, prove that the exact source order code `TMCS1123A3AQDVGR` is currently an orderable variant. That exact suffix remains **unverified, not invalid**. Confirm it against TI/purchasing evidence before freezing the BOM.

## Important limitations — do not treat as fabrication-ready

1. The library has been created as a controlled draft but **has not yet passed a KiCad CLI parse/load test**. Run a KiCad library/schematic validation in a suitable KiCad 10 environment before use.
2. No footprint is assigned. Package dimensions, land pattern, pad numbering and pin-1 orientation must be verified against manufacturer package drawings and the selected footprint.
3. Symbol electrical types are engineering classifications for ERC use, not proof of a complete circuit.
4. No pins have been assigned to nets and no intended wiring has been inferred. In particular, the ADC differential input polarity and mapping from each AMC1311/TMCS1123 output to ADS131M06 channels still require an approved pin-to-net intent table.
5. The ADS131M06 physical `NC` pins use passive pin types in the library because KiCad electrical pin types do not encode an NC instruction. The symbol/library documentation records that pins 9–12 and 27 are marked NC by the datasheet; the schematic instance must still use explicit no-connect markers where required.
6. This work does not establish creepage/clearance, isolation class, safety compliance, or permission to energize the TestStation.

## Pin functions represented

### ADS131M06IPBSR

| Pin | Function | Pin | Function |
|---:|---|---:|---|
| 1 | AIN2P | 17 | CS |
| 2 | AIN2N | 18 | DRDY |
| 3 | AIN3N | 19 | SCLK |
| 4 | AIN3P | 20 | DOUT |
| 5 | AIN4P | 21 | DIN |
| 6 | AIN4N | 22 | XTAL2 |
| 7 | AIN5N | 23 | XTAL1/CLKIN |
| 8 | AIN5P | 24 | CAP |
| 9–12 | NC | 25 | DGND |
| 13 | AGND | 26 | DVDD |
| 14 | REFIN | 27 | NC |
| 15 | AVDD | 28 | AGND |
| 16 | SYNC/RESET | 29 | AIN0P |
|  |  | 30 | AIN0N |
|  |  | 31 | AIN1N |
|  |  | 32 | AIN1P |

### AMC1311BDWVR

| Pin | Function | Pin | Function |
|---:|---|---:|---|
| 1 | VDD1 | 5 | GND2 |
| 2 | IN | 6 | OUTN |
| 3 | SHTDN | 7 | OUTP |
| 4 | GND1 | 8 | VDD2 |

### TMCS1123 10-pin function table

| Pin | Function | Pin | Function |
|---:|---|---:|---|
| 1 | IN+ | 6 | VOUT |
| 2 | IN− | 7 | OC |
| 3 | GND | 8 | VS |
| 4 | ALERT | 9 | VOC |
| 5 | VREF | 10 | NC |

For TMCS1123 pins 4, 5, 7 and 9, confirm unused-pin handling from the datasheet before finalizing nets. The datasheet's unused-pin guidance is not a substitute for an approved circuit-level decision.

## Automated checks

- Static regression script: [`validate_verified_symbol_library.py`](../verification/scripts/validate_verified_symbol_library.py).
- Automated KiCad parser/export workflow: [`.github/workflows/validate-evse-symbol-library.yml`](../../../../../.github/workflows/validate-evse-symbol-library.yml). It runs on scoped updates to `main`, can be started by the repository owner by commenting `/run-evse-symbol-validation` on [control issue #3](https://github.com/AndreVazao/VAZAO-EVSE-Platform/issues/3), and reports its result there. It uses KiCad 10.0.7 and requires successful SVG export of all three symbols.

The static check is not a substitute for the KiCad CLI parser/export step; do not mark the library approved until the manual workflow passes.

## Controlled next steps

1. Validate the library syntax using the target KiCad CLI; repair syntax only in this isolated library.
2. Compare symbol pin numbers to manufacturer package drawings and the intended footprint pad map.
3. Verify the exact TMCS1123 suffix and selected package/footprint.
4. Approve the pin-to-net intent table, including every ADC differential pair and each isolation domain.
5. Only then create a separate migrated schematic copy, replace symbols and re-export netlist/ERC.
6. Keep the existing M2.9-K master and legacy M2.9-L source untouched until review passes.

