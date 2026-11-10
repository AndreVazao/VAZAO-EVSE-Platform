# VAZÃO EVSE — Charger Hardware V1 — M1.13: CHARX meter compatibility and CT architecture

**Status:** PARTIAL — meter topology and controller compatibility boundary clarified; no meter approved for production.  
**Date:** 2026-11-10  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.9, M1.11 and M1.12.

## 1. Executive result

M1.13 adds two important manufacturer evidence findings:

1. Phoenix Contact's CHARX load-management guidance explicitly requires a measuring device at each charging point (reference F) so the SEC-3xxx server can calculate and distribute the load against the protected load circuit. The guide also distinguishes a separate upstream/grid-infeed meter (reference M). This reinforces **one independently attributable meter per EVSE output** for the proposed architecture.
2. A retrievable CHARX control modular user manual, Revision 04 / firmware 1.5.1 (2024-03-14), lists the meter models implemented in that firmware. It lists EEM-350 family, EEM-EM357 family, Carlo Gavazzi EM24/EM340/EM111, Inepro PRO380 and Iskra WM3M4(C), but **does not list EEM-XM375 or EEM-XM355**. The manual says the list may be extended in future software and directs the installer to inspect the actual charging-point configuration in the installed firmware.

Therefore:
- EEM-XM375 1674510 remains the strongest MID candidate on product data, but **CHARX compatibility is not confirmed**.
- EEM-XM355 1674509 is a current MID CT meter with RS-485 Modbus and published downloads, but **CHARX compatibility is not confirmed** either.
- A Modbus interface alone is not evidence that CHARX has a supported meter profile or that it will correctly use the meter for current monitoring/load management.
- No production meter is selected.

## 2. Evidence sources and version boundaries

### 2.1 Current CHARX load-management help

Official Phoenix Contact help page:  
https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Load_management.htm

The page describes:
- D: CHARX SEC-3xxx server controller for load management.
- E: client charging controllers.
- F: measuring device at each charging point.
- M: separate higher-level measuring device at the grid feed-in, when monitoring the main fuse and unknown/uncontrolled loads.
- The server limits the load circuit based on momentary current values read from the individual charging-point meters.
- Only loads detected by the F meters may be installed behind the protected load-circuit fuse B.
- Ethernet ETH0 or the RS-485 meter interface can be used for energy measuring devices, subject to the documented topology.
- If two meters share the relevant RS-485 arrangement for charging-point and central-infeed measurement, they must be the same type; the central meter address is offset by one.
- Do not mix dynamic load setpoints through OCPP Smart Charging and other Modbus/TCP or REST applications simultaneously; the help warns of unexpected behaviour.
- Maintain margin to the upstream fuse rating; the help gives examples of 10% below 100 A and 20% above 100 A.

**Design consequence:** keep point meters (F) and the optional upstream meter (M) as separate measurement roles. A single shared meter at the incomer cannot substitute for individual point measurement in the published CHARX load-management topology.

### 2.2 CHARX user manual available for extraction

Retrieved document: *User Manual UM EN CHARX SEC*, Revision 04, dated 2024-03-14, firmware 1.5.1, covering SEC-3150 (1138965), SEC-3100 (1139012), SEC-3050 (1139018), SEC-3000 (1139022) and SEC-1000 (1139034).

Public copy used for technical text extraction:  
https://www.tti.com/content/dam/tti-commons/supplier/phoenix-contact/doc/phoenix-contact-charx-control-modular-user-manual.pdf

Relevant section 4.7, “Connecting the energy measuring device”:
- Meter connection uses the controller's RS-485 “Meter” connector.
- Implemented meter list in that manual revision:
  - Phoenix Contact EEM-350-D-MCB, 2905849
  - Phoenix Contact EEM-DM357, 1252817
  - Phoenix Contact EEM-DM357-70, 1219095
  - Phoenix Contact EEM-EM357, 2908588
  - Phoenix Contact EEM-EM357-EE, 1311985
  - Phoenix Contact EEM-EM157-EE, 1311993
  - Phoenix Contact EEM-AM157-70, 1219090
  - Carlo Gavazzi EM24, EM111, EM340
  - Inepro PRO380-Mod
  - Iskra WM3M4(C)
- The manual says to select the actual meter type in the web-based management and match communication settings to the selected meter's defaults.
- It says the supported list may be extended in future software releases and that the installed firmware's actual list is visible in charging-point configuration.
- The manual says to connect a meter when using current monitoring (overcurrent/out-of-balance) or load management.

**Version limitation:** Revision 04 / firmware 1.5.1 is older than the current CHARX help/manual baseline recorded in M1.11 (Revision 06 / firmware 1.9.1). The extracted list is valid evidence for that older firmware only. It is not proof that firmware 1.9.1 lacks XM-series support. It is also not proof that support was added. The current installed firmware list and written Phoenix confirmation remain mandatory.

### 2.3 EEM-XM375 1674510 product evidence

Official product page:  
https://www.phoenixcontact.com/en-pc/products/measuring-device-eem-xm375-1674510

Confirmed product-page properties:
- Three-phase CT-operated meter, 1 A / 5 A secondary.
- Modbus/TCP over Ethernet, RJ45, 100 Mbps; integrated web server.
- MID 2014/32/EU stated by manufacturer.
- Class C EN 50470-3; class 0.5 IEC 62053-21.
- Bidirectional/four-quadrant measurement.
- Measurement voltage 100–277 V AC phase-neutral / 173–480 V AC phase-phase.
- External supply 100–277 V AC or via measurement voltage; stated 10 VA / 2 W.
- IP20 connections, DIN rail mounting, MID operating range -40…+70 °C.
- Manufacturer-stated calibration validity: 8 years.
- Product page exposes CT accessory families and connection-diagram images.
- The page's downloads query returned an error during this review; the EEM-XMxxx manual and exact MID certificate were not obtained as files.

**Compatibility finding:** the product's Modbus/TCP interface is not listed as a supported CHARX point-meter profile in the extracted Revision 04 manual. The current help's reference to Ethernet ETH0 for measuring devices does not, by itself, identify XM375 as an implemented model. Treat integration as **unconfirmed** until Phoenix identifies the supported firmware, profile, network port/topology, register map and configuration entry.

### 2.4 EEM-XM355 1674509 product evidence

Official product page:  
https://www.phoenixcontact.com/en-pc/products/measuring-device-eem-xm355-1674509

Confirmed product-page properties:
- Three-phase CT-operated meter, 1 A / 5 A secondary.
- Modbus/RTU over RS-485.
- Two passive opto-isolated pulse outputs; four tariffs via Modbus.
- MID 2014/32/EU stated by manufacturer.
- Class C EN 50470-3; class 0.5 IEC 62053-21.
- Bidirectional/four-quadrant measurement.
- Manufacturer-stated calibration validity: 8 years.
- Product page exposes English manual UM EN EEM-XMxxx, product ID 111667, revision 03, plus register-table archive and EU declaration of conformity.

**Compatibility finding:** RS-485 matches the physical interface type of the CHARX “Meter” connector, but the model is not named in the Revision 04 implemented meter list. Interface similarity does not prove protocol/profile support. Do not connect it as an assumed drop-in replacement for EEM-EM357 or EM340.

### 2.5 EEM-MA370-R 2907980

Official product page:  
https://www.phoenixcontact.com/en-pc/products/measuring-instrument-eem-ma370-r-2907980

The product page confirms Modbus/RTU over RS-485 and Modbus/TCP over Ethernet, with CT 1 A/5 A inputs. MID approval was not evidenced in the reviewed product data. Retain as an operational telemetry candidate only; it is not a billing-meter candidate on current evidence.

## 3. CT architecture for one 22 kW output

Reference output: 400 V three-phase, 32 A maximum per phase, AC Mode 3 Type 2.

At this stage, specify functional requirements, not a final CT SKU:
- One three-phase meter and one correctly matched CT per measured phase for each output, unless the meter's approved wiring diagram specifies otherwise.
- CT primary rating must be selected from the actual maximum continuous current and overload/protection coordination; do not assume a 32 A CT is suitable merely because the EVSE is configured to 32 A.
- CT secondary must match the selected meter input exactly (1 A or 5 A); never mix ratios or secondary types.
- Select CT accuracy class, rated burden, frequency, thermal/short-time withstand and aperture from the complete meter + CT + cable chain.
- Confirm polarity (P1/P2, S1/S2 or manufacturer markings), phase association and phase rotation. Commissioning must detect reversed polarity and incorrect phase mapping.
- Provide approved shorting/isolating CT terminal blocks. Never leave an energised CT secondary open-circuit.
- Keep CT secondary wiring segregated, identified and protected; route each output's three CT circuits only through its own meter.
- Physical arrangement must prevent cross-assignment between output 1…4 and meter 1…4. Use durable labels and a traceable meter/CT serial-number register.
- If MID billing is intended, preserve the complete approved measurement chain, sealing points, configuration controls and tamper evidence required by the exact certificate and applicable national rules.

No CT part number, ratio, burden, cable size, terminal part number or seal arrangement is approved by M1.13. The meter's input ratings and CT accessory list are insufficient to complete those selections without the model manual, CT datasheets and installation geometry.

## 4. Per-output metering architecture

| Product | Point meter allocation | Controller relationship | Status |
|---|---|---|---|
| Single output | MTR-01 dedicated to output 1 | One point measurement channel | Required architecture |
| Dual output | MTR-01 and MTR-02, independently wired/addressed | Each point value assigned to its own charging point | Required architecture |
| Quad output | MTR-01…MTR-04, independently wired/addressed | Each point value assigned to its own charging point | Required architecture |
| Optional grid-infeed monitoring | MTR-GRID separate from point meters | Higher-level fuse/load monitoring only | Optional additional meter |

A shared Ethernet switch or RS-485 bus does not remove the requirement for unique meter identity and point attribution. If Phoenix supports a multi-drop bus, addresses, termination, isolation, polling and failure handling must be documented for the exact model and firmware. No shared-meter shortcut is assumed.

## 5. Manufacturer questions — required written response

Request written confirmation from Phoenix Contact technical support for the following exact questions:

1. Does CHARX SEC-3000/3050/3100/3150 firmware 1.9.1 support EEM-XM375 item 1674510 as a charging-point meter for current monitoring and load management? If yes, provide the exact WBM meter-type entry, profile/driver version, network port and topology.
2. Does the same firmware support EEM-XM355 item 1674509 on the RS-485 Meter connector? If yes, provide the exact WBM selection and communication defaults.
3. Are either of these models approved for the CHARX SEC-1000 client architecture, and are meters configured independently per client charging point?
4. Can one SEC-3xxx server manage four independently metered points using these models? Provide the supported meter count, bus/network arrangement, polling interval and failure behaviour.
5. For XM375, does CHARX use ETH0 for the meter, and can ETH0 simultaneously support the intended server/client/network arrangement without conflict?
6. Provide the current supported-meter list for firmware 1.9.1 (and later available firmware), not only the 2024 Revision 04 / firmware 1.5.1 list.
7. Confirm whether XM375 or XM355 MID energy registers are consumed by CHARX for transaction records/OCPP meter values, and identify the exact registers, units, scaling, direction and persistence behaviour.

No supplier request has been sent by this engineering gate. This section is the controlled question list for the next supplier interaction.

## 6. Validation plan once compatibility is confirmed

Bench validation only, using isolated SELV/controller interfaces and a safe metering test source:
1. Verify meter identity, firmware, serial number, CT ratio and configuration export.
2. Verify phase-to-CT mapping and polarity with a known reference load.
3. Compare active energy and instantaneous current against a traceable reference across low, nominal and maximum operating points.
4. Inject reversed CT polarity, missing phase, swapped phases, wrong ratio, duplicate Modbus address, lost Ethernet/RS-485 and meter power loss.
5. Verify that meter loss inhibits/limits charging as required by the controller safety and load-management design; it must never silently substitute another point's measurement.
6. Verify restart, counter persistence, timestamp quality and transaction-to-output attribution.
7. Verify four-point simultaneous load allocation and upstream fuse margin.
8. Preserve raw test results, firmware versions, register dumps, configuration exports and calibration/certificate evidence.

No mains energisation or vehicle charging is authorised by this plan. A qualified engineering test procedure and suitable isolated test equipment are required.

## 7. Gate status

| Gate | Status |
|---|---|
| Per-point meter requirement in CHARX load-management topology | CONFIRMED by current manufacturer help |
| Separate optional grid-infeed meter role | CONFIRMED by current manufacturer help |
| XM375 MID product-page claim and CT 1 A/5 A interface | CONFIRMED at product-page level |
| XM355 MID product-page claim and RS-485 interface | CONFIRMED at product-page level |
| XM375 support in CHARX firmware 1.9.1 | OPEN — written confirmation required |
| XM355 support in CHARX firmware 1.9.1 | OPEN — written confirmation required |
| Exact XMxxx manual, CT wiring and MID certificate scope for XM375 | OPEN — downloads retrieval failed |
| CT model/ratio/burden/sealing for 32 A output | OPEN |
| Per-output register attribution and OCPP/transaction persistence | OPEN |
| Portuguese legal/fiscal/metrology suitability | OPEN |
| Approved production meter | NOT SELECTED |

## 8. Next actions

1. Obtain from Phoenix Contact the current firmware 1.9.1 supported-meter list and written XM375/XM355 compatibility confirmation.
2. Obtain the exact EEM-XMxxx manual and MID certificate for item 1674510, plus selected CT datasheets and certificate scope.
3. Compare a supported legacy/direct or CT meter option against the XM series; favour proven CHARX integration where the commercial metrology requirements are met.
4. Only after compatibility evidence, define per-output meter wiring, CT ratio, shorting terminals, sealing, Modbus addressing and test procedure.
5. Obtain Portuguese metrology/legal review before any billing or MID-compliance claim.

**Safety and compliance:** M1.13 is research and architecture documentation only. It does not approve a meter, CT, protective device, wiring, installation or billing workflow. It does not authorise fabrication release, mains energisation or commercial deployment.
