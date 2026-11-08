# VAZÃO EVSE — Charger Hardware V1 — M1.12: MID meter candidate and lifecycle review

**Status:** PARTIAL — stronger MID candidate identified; no meter approved for production.  
**Date:** 2026-11-08  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.9, M1.10 and M1.11.

## 1. Executive result

Manufacturer product-page evidence materially changes the meter shortlist:

- **EEM-XM375, item 1674510** is listed as a new/current product, MID-compliant under 2014/32/EU, three-phase, CT-operated (1 A / 5 A secondary), Modbus/TCP over Ethernet, bidirectional, accuracy class C (EN 50470-3), operating temperature -40…+70 °C for MID, with an 8-year calibration validity period. This is the strongest current MID candidate found for further evaluation.
- **EEM-EM355, item 2908578** is explicitly marked **“No longer in product range”** by Phoenix Contact, despite MID compliance, RS-485 Modbus and class B (EN 50470-3). Manufacturer identifies replacement **EEM-XM355, item 1674509**. Do not select 2908578 for new procurement.
- **EEM-MA370-R, item 2907980** provides Modbus/RTU and Modbus/TCP but its published product data reviewed in this gate does not show MID approval. Keep it for operational telemetry/measurement evaluation only, not as the default billing meter.
- EEM-XM375 uses CTs and Ethernet; neither direct-current measurement nor CHARX compatibility is established. The existence of a MID certificate does not by itself establish legal suitability for every Portuguese billing model or prove end-to-end transaction attribution.

**Decision:** promote EEM-XM375 1674510 to the lead MID *candidate for technical validation*, not to approved BOM.

## 2. Manufacturer evidence

### 2.1 EEM-XM375 — 1674510

Official product page:  
https://www.phoenixcontact.com/en-pc/products/measuring-device-eem-xm375-1674510

Manufacturer-published data extracted:
- Three-phase energy meter, current transformer measurement 1 A / 5 A AC.
- Modbus/TCP over Ethernet, RJ45, 100 Mbps; web server.
- MID-compliant; product description explicitly references Measuring Instruments Directive 2014/32/EU.
- Bidirectional measurement (delivery and consumption), four-quadrant measurement.
- Accuracy class C under EN 50470-3; class 0.5 under IEC 62053-21.
- Current input via external CTs; nominal secondary 1 A or 5 A.
- Voltage measurement 100…277 V AC phase-neutral / 173…480 V AC phase-phase.
- External supply 100…277 V AC or supply via measurement voltage; 10 VA / 2 W stated.
- IP20 connections; DIN rail; operating temperature -40…+70 °C for MID.
- Manufacturer lists calibration validity period 8 years.
- Register table and English manual UM EN EEM-XMxxx, product ID 111667, revision 03, appear in downloads.

These ratings are manufacturer product-page data, not a wiring schedule. Exact CT models, ratios, burden, polarity, shorting/isolating terminals, conductor routing, sealing and installation rules must follow the model manual and certificate.

### 2.2 EEM-EM355 — 2908578

Official product page:  
https://www.phoenixcontact.com/en-pc/products/measuring-instrument-eem-em355-2908578

Manufacturer-published data:
- MID-compliant, class B (EN 50470-3).
- Three-phase, CT-operated 1 A / 5 A.
- RS-485 Modbus.
- Product lifecycle explicitly: **No longer in product range**.
- Manufacturer replacement link: EEM-XM355 1674509.

**Decision:** historical comparison only; block new design-in and procurement.

### 2.3 EEM-MA370-R — 2907980

Official product page:  
https://www.phoenixcontact.com/en-pc/products/measuring-instrument-eem-ma370-r-2907980

Manufacturer-published data:
- Modbus/RTU over RS-485 and Modbus/TCP over Ethernet.
- 3-phase (3/4-wire), 2-phase and single-phase configurations.
- Current measurement via 1 A / 5 A CT secondary.
- 100…230 V AC auxiliary supply (±20%) or 150…250 V DC.
- The product page reviewed does not identify MID approval.

**Decision:** candidate for operational metering/telemetry only pending fuller metrology evidence. Do not describe it as a MID billing meter.

## 3. Comparison

| Model | Lifecycle | MID evidence | Interface | Current topology | Current decision |
|---|---|---|---|---|---|
| EEM-XM375 1674510 | Listed NEW / in stock on page | Explicit MID 2014/32/EU | Modbus/TCP Ethernet | CT 1 A / 5 A | Lead candidate for validation |
| EEM-EM355 2908578 | No longer in product range | Explicit MID, class B | RS-485 Modbus | CT 1 A / 5 A | Block new procurement; replacement 1674509 |
| EEM-MA370-R 2907980 | Product page available | Not evidenced on reviewed page | Modbus RTU + TCP | CT 1 A / 5 A | Telemetry candidate only pending MID evidence |

## 4. EVSE integration questions still open

1. Does Phoenix Contact provide a supported CHARX SEC-3xxx meter profile for EEM-XM375 1674510? Obtain written confirmation and exact firmware/profile version.
2. Is Modbus/TCP meter integration supported directly by the chosen SEC-3xxx variant, or is a separate gateway/controller required? Confirm network topology, addressing, polling rate and register map.
3. Can one meter be uniquely assigned to each charging point, with independent energy values and transaction binding?
4. Which CTs and ratio are approved for a 32 A / 22 kW three-phase output? Verify CT primary rating, secondary, accuracy class, burden, thermal limits, installation geometry and anti-tamper sealing.
5. Is the measurement chain (meter + CTs + wiring + installation + software) within the MID certificate scope and valid for the intended Portuguese commercial use?
6. What are the local legal, fiscal and metrology requirements for billing/recharging in the target deployment? Obtain qualified Portuguese compliance review; do not infer from the product MID badge alone.
7. How are meter communication loss, reverse energy, phase loss, reset, counter rollover and time synchronisation handled and audited?

## 5. Design implications

- A CT meter is not a drop-in replacement for a direct-connected meter. It adds CT selection, ratio configuration, secondary wiring, terminal safety and sealing requirements.
- Do not open-circuit an energised CT secondary. Use approved shorting/isolating terminal arrangements and follow the meter/CT manufacturers' procedures.
- For one independent EVSE output, use one independently attributable measurement channel/meter unless the manufacturer explicitly validates another arrangement.
- A shared Ethernet network must not cause one meter's identity or energy counters to be attributed to another output.
- MID data must be retained as signed/auditable transaction evidence by the CPMS/local controller architecture; a meter's MID status alone does not implement billing compliance.

## 6. Gate status

| Gate | Status |
|---|---|
| Current MID-capable candidate identified | PARTIAL — EEM-XM375 1674510 |
| Exact MID certificate and scope reviewed | OPEN |
| CT selection and measurement-chain design | OPEN |
| CHARX compatibility/profile confirmed | OPEN |
| Register map and transaction attribution tested | OPEN |
| Portuguese legal/fiscal suitability reviewed | OPEN |
| Procurement and supply-chain confirmation | OPEN |
| Approved production meter | NOT SELECTED |

## 7. Next actions

1. Download and inspect the EEM-XMxxx manual and MID certificate for 1674510; extract exact terminal assignments, CT wiring, sealing and certificate scope.
2. Request Phoenix Contact written confirmation of CHARX SEC-3xxx support for EEM-XM375 1674510 and the supported register/profile.
3. Compare 1674510 with its manufacturer-listed replacement EEM-XM355 1674509 and any current direct-measurement MID alternatives.
4. Prepare a per-output metering architecture and CT specification for the 22 kW reference output.
5. Obtain Portuguese metrology/legal review before making any billing-compliance claim.

**Safety and compliance:** M1.12 is component research only. It does not approve a meter, CT, installation, wiring or billing workflow and does not authorise fabrication or energisation.
