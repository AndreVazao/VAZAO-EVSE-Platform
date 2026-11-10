# VAZÃO EVSE — Charger Hardware V1 — M1.13: CHARX meter compatibility and CT architecture

**Status:** PARTIAL — meter topology and controller compatibility boundary clarified; no meter approved for production.  
**Date:** 2026-11-10  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.9, M1.11 and M1.12.

## 1. Executive result

M1.13 adds two important manufacturer evidence findings:

1. Phoenix Contact's CHARX load-management guidance explicitly requires a measuring device at each charging point (reference F) so the SEC-3xxx server can calculate and distribute the load against the protected load circuit. The guide also distinguishes a separate upstream/grid-infeed meter (reference M). This reinforces **one independently attributable meter per EVSE output** for the proposed architecture.
2. The current official CHARX help for firmware 1.9.1 explicitly lists **EEM-XM355 1674509** as a selectable energy-meter type in charging-point configuration. This upgrades XM355 from an unconfirmed interface candidate to a manufacturer-listed CHARX integration candidate for point measurement/current monitoring/load-management evaluation. The same current list does **not** include EEM-XM375 1674510.
3. The separate current CHARX legal-metrology/OCMF page lists only ISKRA WM3M4C, EMH iML e-moc and Elektro BAUER BSM-WS36A-Y as compatible OCMF hub meters. Neither XM355 nor XM375 appears in that legal-metrology list. Thus XM355's MID product claim and CHARX point-meter profile do not establish signed OCMF billing compatibility.

Therefore:
- EEM-XM355 1674509 is the leading **CHARX-configurable MID point-meter candidate** for further testing, not an approved billing meter.
- EEM-XM375 1674510 remains a MID CT candidate at product level, but its point-meter support in CHARX firmware 1.9.1 is not listed; do not assume its Modbus/TCP interface is enough.
- Neither XM355 nor XM375 is currently evidenced as a CHARX legal-metrology/OCMF compatible meter.
- No production meter or legally compliant billing chain is selected.

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

**Version limitation:** Revision 04 / firmware 1.5.1 is older than the current Revision 06 / firmware 1.9.1 baseline. Its omission of XM-series meters is historical only. The current 1.9.1 configuration page resolves this for XM355 (listed) and XM375 (not listed).

### 2.4 EEM-XM375 1674510 product evidence

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

**Compatibility finding:** EEM-XM375 is not named in the current firmware 1.9.1 selectable meter list. Its Modbus/TCP interface alone does not establish a CHARX point-meter profile. Treat point-meter integration as **not evidenced / not selectable in published current list** unless Phoenix confirms otherwise in writing.

### 2.5 EEM-XM355 1674509 product evidence

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

**Compatibility finding:** the current firmware 1.9.1 charging-point configuration explicitly lists EEM-XM355 1674509 as a selectable meter type. This is manufacturer evidence of a supported profile for point-meter configuration. It is not yet bench validation of four-point operation, MID billing, signed OCMF output or Portuguese legal suitability. The controller's Meter connector is RS-485; confirm the exact baud rate, address, parity and register settings against the XMxxx manual and WBM selection.

### 2.6 EEM-MA370-R 2907980

Official product page:  
https://www.phoenixcontact.com/en-pc/products/measuring-instrument-eem-ma370-r-2907980

The product page confirms Modbus/RTU over RS-485 and Modbus/TCP over Ethernet, with CT 1 A/5 A inputs. MID approval was not evidenced in the reviewed product data. Retain as an operational telemetry candidate only; it is not a billing-meter candidate on current evidence.



### 2.7 Current CHARX legal-metrology / OCMF compatibility

Official Phoenix Contact page:  
https://www.phoenixcontact.com/charx-help/CHARX_control_modular_product_family/Legal_metrology.htm

The current help explains that, in legal-metrology operation, the SEC-3xxx forwards signed OCMF packets from the energy meter to the backend via OCPP. The meter signs the packet after a charging process; the controller forwards it unchanged. The page says the legal-metrology-relevant functions are in the meter, backend (according to the type-examination certificate) and optional transparency-software verification.

The current compatible OCMF meter table lists only:
- ISKRA WM3M4C, version 2.05, OCMF 1.0.
- EMH iML e-moc, version 1.09, OCMF 1.4.1, with specified Modbus settings.
- Elektro BAUER BSM-WS36A-Y, version V60, OCMF 1.4.0, with specified internal switching and IR probe requirements.

**Neither EEM-XM355 nor EEM-XM375 appears in the current OCMF compatible-meter table.** A MID product-page claim and a selectable CHARX energy-meter profile are not equivalent to OCMF signing support. The XM355 must therefore be treated as a point measurement/load-management candidate only until Phoenix confirms a legal-metrology-capable model/firmware and provides the relevant type-examination/certificate evidence.

The page also states that OCMF transmission is automatic when a compatible meter is connected/configured; only OCPP release mode provides OCMF records. Continuous charging release mode does not provide downloadable OCMF records and the supplied energy is not considered billable from a legal-metrology perspective. Offline transactions are temporarily stored on the controller, limited to 100 charging processes, after which older records are deleted. This is a material constraint for any future offline billing design; it must be reflected in product requirements and backend/operator recovery procedures.

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
| XM375 selectable point-meter profile in CHARX firmware 1.9.1 | NOT LISTED — written exception/roadmap confirmation required |
| XM355 selectable point-meter profile in CHARX firmware 1.9.1 | CONFIRMED IN CURRENT CONFIGURATION HELP; bench validation open |
| XM355/XM375 compatible signed OCMF legal-metrology profile | NOT LISTED in current OCMF table |
| Exact XMxxx manual, CT wiring and MID certificate scope for XM375 | OPEN — downloads retrieval failed |
| CT model/ratio/burden/sealing for 32 A output | OPEN |
| Per-output register attribution and OCPP/transaction persistence | OPEN |
| Portuguese legal/fiscal/metrology suitability | OPEN |
| Approved production meter | NOT SELECTED |

## 8. Next actions

1. Ask Phoenix Contact whether XM355 is supported for the required four-point SEC-1000/SEC-3xxx topology and whether any XM-series model/firmware supports signed OCMF legal-metrology output.
2. Obtain the exact EEM-XMxxx manual and MID certificate scope for item 1674509 and item 1674510, plus selected CT datasheets.
3. Compare XM355's proven selectable point-meter profile against the OCMF-capable EMH/BAUER alternatives and lifecycle/procurement status of Iskra WM3M4C; do not procure a discontinued device.
4. Only after compatibility evidence, define per-output meter wiring, CT ratio, shorting terminals, sealing, Modbus addressing and test procedure.
5. Obtain Portuguese metrology/legal review before any billing or MID-compliance claim.

**Safety and compliance:** M1.13 is research and architecture documentation only. It does not approve a meter, CT, protective device, wiring, installation or billing workflow. It does not authorise fabrication release, mains energisation or commercial deployment.
