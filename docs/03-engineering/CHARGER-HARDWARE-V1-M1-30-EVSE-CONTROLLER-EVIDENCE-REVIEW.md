# VAZÃO EVSE Charger Hardware V1 — EVSE Controller Evidence Review (M1.30)

**Status:** OFFICIAL CATALOG EVIDENCE REVIEW / NO CONTROLLER SELECTED  
**Date:** 2026-11-26  
**Scope:** Controller candidates for first single-output AC Mode 3 prototype; reuse implications for modular output cells  
**Parent:** M1.28 Output Cell architecture; M1.29 24-interface traceability

## 1. Purpose and evidence rules

M1.30 reviews current manufacturer product-catalog data for the two Phoenix Contact candidates already recorded in M1.29. Catalog data is useful evidence, but it is not a substitute for controlled installation manuals, firmware-specific behavior, complete safety integration, wiring review, system calculations and verification.

This document does not select a controller, release wiring, approve protection, or authorize mains energisation. Links below point to manufacturer product pages reviewed on 2026-11-26; the source documents have not been downloaded into controlled project custody or independently SHA-256 verified.

## 2. SEC-1000 (1139034) — catalog evidence

Manufacturer: Phoenix Contact  
Official product page: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034

Current catalog description and data reviewed:
- CHARX control modular AC controller, IEC 61851-1 Mode 3, Case B/C.
- 12 V DC supply, tolerance ±5% (11.4–12.6 V).
- Current consumption: maximum 2 A in stand-alone operation; below 50 mA no-load, without external loads.
- Four digital inputs; four low-side digital outputs, maximum 600 mA each (catalog listing).
- Peripheral interfaces described for energy meter, RFID and DC residual-current detection; modular system bus.
- Vehicle interface according to IEC 61851-1; contactor control listed as floating switch contact.
- Temperature-monitoring inputs listed for Pt1000 and PTC chain.
- IP20, DIN rail; ambient operating range catalogued as −25 °C to +65 °C.

**Engineering implication:** the SEC-1000 is the stronger candidate for an Output Cell architecture where meter, RFID and DC residual-current peripherals may be modular. Its 2 A maximum stand-alone current is a meaningful supply-budget input, not a complete PSU sizing value. The 12 V ±5% tolerance is tight; the supply, distribution, cable drop, transient load and all peripheral loads must be checked against the controller's exact manual.

**Open evidence:** controlled manual/revision; pin and terminal map; exact contactor output ratings/behavior; CP/PP details; RCM peripheral compatibility; firmware and operating-mode behavior; offline/fault behavior; cluster dependencies; system-bus limits; current and inrush under each configuration; lifecycle and cybersecurity support.

## 3. EM-CP-PP-ETH (2902802) — catalog evidence

Manufacturer: Phoenix Contact  
Official Portugal product page: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802  
Official English product page: https://www.phoenixcontact.com/en-gb/products/ac-charging-controller-em-cp-pp-eth-2902802

Current catalog data reviewed:
- AC Mode 3, Type 2, Case B/C; one charging point; stand-alone/client modes.
- Supply range 95–264 V AC (nominal 110–240 V); maximum current consumption listed as 40 mA; no-load power below 1 W.
- Four digital inputs (nominal 24 V).
- Four digital outputs; catalog lists 0.2 A aggregate for internally supplied outputs and up to 0.6 A/channel with external supply.
- Ethernet 10/100, Modbus/TCP; RS-485 2-wire, one supported device, 2.4–19.2 kbit/s.
- IP20, DIN rail; operating temperature −25 °C to +60 °C.

**Engineering implication:** this candidate is a single-point controller with integrated interfaces and an AC supply. Do not assume it has the modular peripheral/cluster capabilities of SEC-1000/SEC-3xxx, or that its one-point RS-485 interface is suitable for the charger-wide meter/load-management topology without exact documentation.

## 4. Consumption discrepancy — status correction

M1.29 recorded a historical discrepancy between a catalog value of 40 mA and a previously reviewed manual value of 70 mA at 230 V / 140 mA at 110 V.

The current official Phoenix Contact product pages retrieved on 2026-11-26 list **maximum 40 mA** and **less than 1 W no-load** for 2902802. This narrows the discrepancy but does not close controlled-document custody or revision verification. Until the exact official manual is archived and its revision checked, mark the discrepancy **PARTIALLY RESOLVED / DOCUMENT REVISION NOT VERIFIED**. Do not treat this catalog result as supplier confirmation or freeze PSU design.

## 5. Preliminary candidate comparison (not a selection)

| Evaluation item | SEC-1000 1139034 | EM-CP-PP-ETH 2902802 |
|---|---|---|
| Supply | 12 V DC ±5% | 95–264 V AC |
| Published consumption | max 2 A stand-alone; <50 mA no-load without external loads | max 40 mA; <1 W no-load |
| Output-cell peripheral modularity | Meter/RFID/DC residual-current peripherals listed | Single point; integrated functions; exact peripheral support open |
| Communications | Modular system bus; peripheral buses per catalog | Ethernet Modbus/TCP and RS-485 |
| Point count | One controller per point in proposed cell; cluster architecture not yet validated | One point |
| Design advantage to investigate | modular safety/measurement peripheral architecture | simplified single-point AC-supplied control |
| Key blocker | controlled docs, exact topology/peripheral behavior and load budget | controlled manual, interface/safety behavior, topology and current discrepancy custody |

Neither candidate is approved. Evaluation criteria and exact document revision must be the same for both before an engineering decision.

## 6. Controller evidence gate (C-EVSE-01)

Required controlled evidence before schematic release:
1. Exact manufacturer manual and revision; original PDF archived and SHA-256 verified.
2. Pin/terminal mapping and complete reference wiring diagram.
3. CP/PP generation/measurement limits and state handling, including invalid/fault cases.
4. Contactor drive interface rating, safe-state behavior, feedback and welded-contact handling.
5. Residual-current/DC detection interface, exact compatible device, diagnostic and trip response.
6. Meter/RFID peripheral models, supported protocols and topology.
7. Local/offline behavior, watchdog, reset, brownout, loss-of-communications and firmware update behavior.
8. Stand-alone/cluster operating restrictions, point-count limits, system-bus constraints and exact backplane current budget if applicable.
9. Auxiliary load budget, peak/inrush, supply tolerance and derating data.
10. Firmware lifecycle, security support, CRA statement, lifecycle and availability confirmation.

## 7. Disposition and next milestone

**M1.30 disposition:** current official catalog data is captured for both candidates; SEC-1000 modular features and its 12 V / 2 A maximum supply demand are now explicitly recognized as key design constraints. The 2902802 consumption conflict is narrowed by current official catalog data but remains open until controlled manual/revision is independently verified.

Next: complete evidence custody for the exact SEC-1000 and 2902802 manuals, then build the safety/protection architecture evidence matrix. No schematic or BOM freeze until controller, residual-current protection, contactor feedback, auxiliary supply and installation assumptions are supported by controlled evidence and calculations.

## 8. Sources

- Phoenix Contact SEC-1000 (1139034), official product page, reviewed 2026-11-26: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-charx-sec-1000-1139034
- Phoenix Contact EM-CP-PP-ETH (2902802), official product page, reviewed 2026-11-26: https://www.phoenixcontact.com/pt-pt/produtos/ac-charging-controller-em-cp-pp-eth-2902802
- Phoenix Contact EM-CP-PP-ETH English product page: https://www.phoenixcontact.com/en-gb/products/ac-charging-controller-em-cp-pp-eth-2902802

Source custody status: web catalog pages reviewed; PDF binary not archived; hashes not independently verified; no supplier contacted.
