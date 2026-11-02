# VAZÃO EVSE — CHARX V1 Component Lifecycle and Peripheral Candidate Review (M1.10)

**Status:** DRAFT / MANUFACTURER DATA REVIEW — NOT A FROZEN BOM  
**Reviewed:** 2026-11-02  
**Scope:** Four-output AC EVSE, with reusable single/dual-output variants  
**Controller family:** Phoenix Contact CHARX control modular — candidate architecture

## 1. Executive findings

M1.10 adds current manufacturer product data for the meter, RFID reader, RCM sensor, accessory cable and 12 V PSU candidates. It identifies one procurement blocker and prevents an unsafe assumption about a small auxiliary supply.

| Function | Manufacturer item | Finding | M1.10 disposition |
|---|---|---|---|
| Local controller | CHARX SEC-3000 1139022 / SEC-1000 1139034 | Current product pages publish interface, supply and connection data | Retain as leading study candidate; not selected |
| Energy meter | ISKRA WM3M4C 1429603 | MID Class B, 3-phase direct 40 A, RS-485 Modbus RTU, but Phoenix product page explicitly says “No longer in product range” | **Procurement blocked**; remove from active BOM candidate pending replacement |
| RFID/NFC | CHARX RFID/NFC-PCB 1391227 | 13.56 MHz, RS-485, 10.8–13.2 V, typical 100 mA at 12 V | Compatible-family candidate; reader-per-output/shared-reader behaviour still unverified |
| Residual current monitor | EV-RCM-6DC-WAT 1309697 | One-channel, one charging point; 30 mA AC / 6 mA DC; 100 A 1-phase / 40 A 3-phase | Candidate per output; verify complete protective coordination and exact sensor integration |
| RCM cable | CHARX SEC JST-RCM-CBL 1360462 | 4-position, 0.4 m; manufacturer lists RCM and RFID accessory compatibility | Accessory candidate; connector assignment and required quantity must be confirmed |
| 12 V supply | STEP3-PS/1AC/12DC/2.5/PT 1170953 | 12 V, 2.5 A, 30 W; short-circuit-proof; no integrated secondary fuse | **Not approved for quad cluster**; insufficient evidence of capacity and branch protection |

No item is frozen for production purchase by this document.

## 2. Controller terminal data — what can safely be recorded

Phoenix Contact's current SEC-1000 and SEC-3000 product pages publish:
- supply: 12 V DC ±5%, permissible 11.4–12.6 V;
- maximum standalone current consumption: 2 A (separate no-load figures are also published);
- push-in conductor range: rigid 0.14–1.5 mm²; flexible 0.2–2.5 mm²; ferruled cable range 0.25–1.5 mm²;
- standard wire strip length: 8 mm; contactor-control connection strip length: 10 mm;
- floating contactor switch contact: max. 250 V AC / 30 V DC, rated current 2 A, interrupting rating max. 1500 VA;
- dedicated RS-485 interfaces for energy meter and RFID;
- dedicated CP/PP, locking, RCM, temperature and digital I/O interfaces.

These are product-level connection limits, not permission to select conductor size or protection without the complete circuit design.

### 2.1 Functional signal schedule (not a terminal-numbered wiring schedule)

| Controller connection group | Manufacturer signal designations | Function | VAZÃO treatment |
|---|---|---|---|
| Supply + RFID | 12 V, GND, 12 V, GND, A+, B− | Controller supply and RFID RS-485 | Verify exact plug position/pin order and cable assembly |
| Output | OUT1…OUT4, 12 V supply pins | Digital outputs | Define load mode, branch protection and safe state |
| Input | IN1…IN4, PTC | Digital/analogue inputs and temperature | Define sensor type, thresholds and unused-channel treatment |
| Meter | 12 V, GND, A+, B−, RxD, TxD | Meter RS-485; RxD/TxD reserved | One meter per measured point unless manufacturer confirms another topology |
| RCM | 12 V, GND, ER1, ER2, TST, NC | Residual-current sensor | One validated protective sensing chain per output |
| Socket | CP, PP, LO−, LO+, LD1, LD2 | IEC 61851 vehicle interface and lock feedback | Dedicated per output |
| Contactor SEC-1000 | C1, C2, NC (2x) | Floating contact | SEC-1000 diagram only |
| Contactor SEC-3xxx | C1/L, C2/L*, N (2x) | Floating contact and, where applicable, zero-cross detection | SEC-3xxx variant diagram only |

**Pinout status:** connector-group names and electrical signal names are manufacturer-confirmed. Exact terminal numbering, physical connector positions, mating connector/accessory SKUs, wire insertion mapping and torque/strip details for each connector are not all established by the extracted web product data. Do not turn this table into a workshop wiring instruction. M1.11 must transcribe the current c09 manual and package slip drawings page-by-page, recording page/figure and controller variant.

## 3. Energy meter — lifecycle correction

Phoenix Contact's page for **ISKRA WM3M4C ENERGYMETER, item 1429603** publishes:
- three-phase direct measurement up to 400 V / 40 A;
- RS-485 Modbus RTU;
- default slave address 33, 8 data bits, no parity, one stop bit;
- MID compliance and Class B (EN 50470-3);
- operating temperature −25 °C to +70 °C.

However, the same manufacturer page explicitly states **“No longer in product range.”**

**Decision:** do not procure 1429603 for a new VAZÃO product, despite its published technical suitability. Retain its data only as a historical interface reference.

The page lists similar/replacement-family devices including EEM-MA370-R (2907980), EEM-EM355 (2908578) and EEM-EM375 (2908581). These are not automatically CHARX-compatible:
- EEM-EM375 is also marked “No longer in product range” and points to replacement 1674510; it uses Ethernet/Modbus TCP and current transformers, not the direct RS-485 meter interface assumed by the old candidate.
- EEM-EM355 is a MID meter with Modbus RTU and current-transformer measurement; compatibility, CT sizing, address settings and current firmware support need confirmation.
- EEM-MA370-R must be checked for its exact measurement method, protocol, MID variant, lifecycle and CHARX support.

**New selection rule:** shortlist only meters for which Phoenix Contact confirms compatibility with the chosen CHARX firmware and which meet the intended Portuguese billing/metrology use case. Verify the exact MID certificate and national legal metrology requirements independently before any commercial billing deployment. A generic Modbus register map is not sufficient evidence.

Manufacturer references:
- 1429603: https://www.phoenixcontact.com/en-pc/products/measuring-instrument-iskra-wm3m4c-energymeter-1429603
- 2907980: https://www.phoenixcontact.com/en-pc/products/measuring-instrument-eem-ma370-r-2907980
- 2908578: https://www.phoenixcontact.com/en-pc/products/measuring-instrument-eem-em355-2908578
- 2908581: https://www.phoenixcontact.com/en-pc/products/measuring-instrument-eem-em375-2908581
- 1674510: https://www.phoenixcontact.com/en-pc/products/measuring-device-eem-xm375-1674510

## 4. RFID reader and cable accessory

Phoenix Contact publishes CHARX RFID/NFC-PCB item **1391227**:
- 13.56 MHz RFID/NFC;
- RS-485 interface;
- supply range 10.8–13.2 V DC;
- typical current consumption 100 mA at 12 V during operation;
- PCB mounting; nominal bore dimension 63.2 mm;
- operating temperature −25 °C to +65 °C;
- manufacturer explicitly describes it for connection to CHARX control modular AC charging controllers.

This is a credible compatible-family candidate, but the manufacturer data reviewed here does not prove one reader can authorise four outputs, nor does it establish whether a reader is required per controller/output. The four-output design must test addressing, reader loss, active-session behaviour and event/session attribution.

Phoenix Contact lists accessory **CHARX SEC JST-RCM-CBL, 1360462**:
- 4-position;
- 0.4 m cable;
- plug-in contact at one end;
- described for connecting EV-RCM-6DC-WAT 1309697 and CHARX RFID/NFC-PCB 1391227 to CHARX control modular modules;
- minimum order quantity / packing unit shown as 10 pieces on the current product page; page status temporarily out of stock at review.

The cable's product description establishes intended accessory compatibility but not the exact conductor-to-terminal pin mapping. Obtain the package slip and current drawing before harness release.

Manufacturer references:
- RFID 1391227: https://www.phoenixcontact.com/en-pc/products/rfid-nfc-device-charx-rfid-nfc-pcb-1391227
- Cable 1360462: https://www.phoenixcontact.com/en-pc/products/cable-set-charx-sec-jst-rcm-cbl-1360462

## 5. Residual-current monitoring candidate

Phoenix Contact publishes EV-RCM-6DC-WAT item **1309697**:
- one channel / one charging point;
- Mode 3, Type 2;
- 30 mA AC and 6 mA DC residual-current detection;
- rated current 40 A for three-phase application (100 A one-phase);
- supply 10.8–13.2 V DC;
- IEC 62955;
- two signal interfaces (Error/Test);
- manufacturer lists compatibility with CHARX SEC-1000 and SEC-3xxx controllers and the 1360462 cable set.

This makes it a strong candidate for evaluation per output. It is **not** a complete RCD/protection design. The final AC RCD/overcurrent protection, disconnection behaviour, sensor location, test function, conductor routing, fault response and applicable installation standard must be reviewed together. Do not assume that the 6 mA DC sensor replaces the required upstream residual-current protective device.

Manufacturer reference:
- https://www.phoenixcontact.com/en-pc/products/differential-current-monitoring-ev-rcm-6dc-wat-1309697

## 6. 12 V supply — do not select by guess

Phoenix Contact STEP3-PS/1AC/12DC/2.5/PT item **1170953** is a DIN-rail supply rated:
- 12 V DC;
- 2.5 A nominal output;
- 30 W;
- short-circuit-proof and no-load-proof;
- electronic secondary-side fuse protection (not an integrated replaceable branch fuse);
- derating above 50 °C, 2%/K;
- 20 ms buffering at 120 V AC and 90 ms at 230 V AC (published typical values).

This supply is a possible low-voltage supply candidate for a limited auxiliary load, but **is not approved as the quad-cluster supply**. The controller pages publish maximum 2 A standalone consumption per controller, while the cluster bus has a 6 A nominal limit. Those separate figures do not establish actual cluster consumption or the approved source arrangement. A 2.5 A PSU cannot be declared suitable for four controllers and peripherals based on the available evidence.

Before selecting a supply:
1. Obtain Phoenix Contact's permitted cluster supply-feed arrangement for the exact number and mix of controllers.
2. Determine whether the backplane is fed through the SEC-3xxx or an SEC-1000 for the proposed configuration.
3. Record measured and maximum consumption for each controller and connected accessory, including simultaneous lock operation.
4. Separate backplane loads from external 12 V auxiliaries; calculate voltage drop and startup/transient demand.
5. Select independently protected branches and confirm that an optional-module short cannot collapse local safety control.
6. Verify ambient-temperature derating, PSU fault response and restart behaviour.

Do not parallel supplies or inject a second source into the CHARX backplane unless the manufacturer explicitly approves that arrangement for the selected configuration.

Manufacturer reference:
- https://www.phoenixcontact.com/en-pc/products/power-supply-unit-step3-ps-1ac-12dc-25-pt-1170953

## 7. M1.10 component decision register

| Ref | Candidate | Decision | Closure evidence |
|---|---|---|---|
| MCU1 | SEC-3000 / SEC-1000 family | Keep as leading study architecture | Server/client failure, exact topology, firmware and local operation tests |
| EM1 | ISKRA WM3M4C 1429603 | Block new procurement; discontinued | Confirm current replacement and CHARX compatibility |
| EM1-A | EEM-MA370-R 2907980 | Investigate only | Datasheet, protocol, MID, direct/CT measurement and CHARX support |
| EM1-B | EEM-EM355 2908578 | Investigate only | Datasheet, CT arrangement, Modbus map, MID and CHARX support |
| EM1-C | EEM-XM375 1674510 | Investigate only | Ethernet topology, MID, current availability and CHARX load-management support |
| RFID1 | CHARX RFID/NFC-PCB 1391227 | Compatible-family candidate | Multi-output reader architecture and offline failure tests |
| RCM1 | EV-RCM-6DC-WAT 1309697 | Per-output candidate | Full protective coordination and tested fault chain |
| CAB1 | CHARX SEC JST-RCM-CBL 1360462 | Accessory candidate | Pin mapping, quantity, availability and harness drawing |
| PSU1 | STEP3-PS/1AC/12DC/2.5/PT 1170953 | Not approved for quad | Complete load budget and manufacturer feed approval |

## 8. M1.11 required work

1. Retrieve and transcribe the current CHARX SEC manual c09 and SEC-1000 package slip: exact terminal positions, plug part numbers, wiring figures, conductor limits, strip lengths and torque by connector.
2. Obtain the package slip and pin assignment for RFID 1391227 and cable 1360462.
3. Ask Phoenix Contact to confirm supported current meter models and the exact four-output meter arrangement for firmware 1.9.1.
4. Verify whether EM355, MA370-R or another current meter is supported, including the MID variant and Modbus register/address plan.
5. Confirm RCM per-output integration and exact protective-device coordination.
6. Obtain the approved cluster supply arrangement and build a populated 12 V/backplane current budget.
7. Update BOM only after lifecycle, compatibility and technical data are verified.

**M1.10 status: PARTIAL — current RFID and RCM accessory candidates are identified; the former meter candidate is blocked as discontinued; the 2.5 A supply is not approved for the quad. Exact connector pin schedule, meter replacement and cluster power budget remain open.**

**Safety notice:** this is a manufacturer-data review, not a frozen BOM, terminal-level construction drawing, conformity assessment or permission to energise mains-connected equipment.
