# VAZÃO EVSE — Charger Hardware V1
## M1.27 — Component candidate and evidence register

**Status:** CONTROLLED CANDIDATE REGISTER — NO COMPONENT APPROVED FOR PRODUCTION  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Depends on:** M1.1–M1.26, especially the BOM, interface reviews, lifecycle reviews and M1.25/M1.26 evidence controls.

## 1. Purpose and authority

This register is the controlled bridge between the preliminary BOM and evidence-backed component dossiers. It records candidate identity, intended function, known decision status, evidence gaps and the next acceptance action.

It is not a purchasing list, final BOM, electrical design, compliance assessment or dimensional authority. A product reference appearing here does not mean that its current lifecycle, availability, compatibility, certificate scope, terminal schedule, ratings or suitability have been re-confirmed in this milestone.

No component is promoted to **selected**, **approved**, **released**, or **purchasable** by this register. Exact manufacturer documentation and competent engineering review remain mandatory.

## 2. Status vocabulary

| Status | Meaning |
|---|---|
| Study candidate | Worth retaining for controlled technical evaluation; no selection implied |
| Prototype candidate | Candidate for a documented bench evaluation only |
| Alternative | Secondary route; compatibility and acceptance remain open |
| Hold | Evidence incomplete or variant ambiguity prevents progression |
| Procurement blocked | Known lifecycle/discontinuation issue; do not specify for new procurement |
| Architecture only | Functional class is known, exact product is not selected |
| Open | No sufficiently identified candidate |

Evidence classes follow M1.25: A manufacturer-controlled drawing; B manufacturer CAD; C manufacturer datasheet; D verified physical measurement; E derived engineering value; F visual/third-party unverified material. A URL or catalogue mention is not a stored, authenticated evidence file. No A–D dimensional evidence is asserted in this register.

## 3. Candidate register

| Function / BOM refs | Candidate identity | Current controlled status | What is known in the project record | Blocking evidence / next action |
|---|---|---|---|---|
| Modular EVSE controller / MCU1, EVSE1, COM1 | Phoenix Contact CHARX control modular; SEC-1000 local controller with SEC-3xxx class cluster controller | Study candidate | Manufacturer manual/interface reviews and cluster architecture are documented in M1.5–M1.13. Quad study topology was 1 × SEC-3xxx + 3 × SEC-1000. Shared backplane nominal current limit of 6 A is a hard constraint. | Confirm exact SEC-1000 and SEC-3xxx order numbers/revisions, terminal schedule, connector accessories, supply budget, bus failure isolation, contactor interface, meter/OCMF behaviour, lifecycle and written manufacturer confirmation. Bench fault injection required. |
| Modular controller specific variant | Phoenix Contact CHARX SEC-3150, 1138965 | Study candidate; not selected | Project review records a 12 V supply domain, Ethernet/LTE connectivity, I/O, RS-485 interfaces, temperature/RCM interfaces and a floating contactor switch contact. | Revalidate all figures against current official datasheet/manual for exact hardware/firmware revision. Confirm contact rating versus coil inrush and suppression, connector pinout, software support, lifecycle and suitability as the selected SEC-3xxx role. Do not drive a contactor coil directly by assumption. |
| Simpler single-point controller | Phoenix Contact CHARX control advanced, 2902802 | Alternative | Legacy one-point controller interface review exists; terminal-level manual evidence remains incomplete. | Confirm current lifecycle, exact terminal-level manual, supported peripherals, safety functions, firmware support and procurement availability. |
| Controller reference only | Bender CC613 | Procurement blocked | Manufacturer lifecycle review recorded it as discontinued. | Do not procure for a new design. Retain only as historical architecture reference unless manufacturer supplies a formally supported successor path. |
| Point meter / EM1 | Phoenix Contact EEM-XM355, 1674509 | Prototype candidate for point metering/load management | M1.12–M1.16 record manufacturer CHARX point-meter profile support and MID candidate evidence. It is not in the reviewed CHARX OCMF legal-metrology compatibility list. | Obtain exact current certificate and installation documentation; prove one-to-one output attribution, CT/direct topology, register scaling, accuracy, firmware integration and Portuguese billing suitability. Do not represent as an evidenced OCMF billing meter. |
| Point meter alternative / EM1 | Phoenix Contact EEM-XM375, 1674510 | Alternative / compatibility hold | Project review records MID 2014/32/EU candidate information, three-phase CT input and Modbus/TCP; current CHARX profile compatibility was not evidenced. | Obtain current certificate scope, CT-chain requirements, exact wiring and written CHARX compatibility. Do not substitute for XM355 without integration evidence. |
| OCMF / legal-metrology prototype meter / EM1 | EMH iML e-moc | Prototype candidate | M1.14–M1.17 record it as the leading OCMF prototype route based on the reviewed CHARX OCMF list and EMH published product claims. | Confirm exact order variant, current MID and national approval certificates, current CHARX firmware compatibility, four simultaneous output sessions, signed record format/key handling, offline persistence, 32 A continuous thermal suitability and Portuguese metrology/fiscal acceptance. Supplier RFI has not been sent. |
| Meter alternative / EM1 | Carlo Gavazzi EM340DINAV23XS1PFB | Study candidate | Previously retained as a Modbus RTU point-meter candidate; no production approval. | Obtain current manufacturer datasheet, exact wiring/interface, accuracy/certification, per-output attribution and controller integration evidence. |
| Meter alternative / EM1 | Carlo Gavazzi EM24DINAV23XE1PFA | Alternative | Previously retained as an Ethernet Modbus TCP meter alternative; no production approval. | Confirm exact variant, communications and register map, metrology certificate scope, integration and output attribution. |
| Meter lifecycle exclusion / EM1 | ISKRA WM3M4C, 1429603 | Procurement blocked | Project lifecycle review records it as no longer in the Phoenix Contact product range. | Do not use for new procurement. Historical OCMF compatibility evidence does not override lifecycle status. |
| Residual-current monitoring / RCD1, I/O1 | Phoenix Contact EV-RCM-6DC-WAT, 1309697 | Study candidate | Peripheral review records this reference as an RCM candidate. | Reconfirm current datasheet, exact measurement scope, sensor/connection arrangement, fault thresholds, diagnostics, controller compatibility and coordination with the final external RCD architecture. RCM does not replace required protective disconnection. |
| RFID / RFID1 | Phoenix Contact CHARX RFID/NFC PCB, 1391227 | Optional-module candidate | Peripheral review records this product reference. RFID is optional in the product architecture. | Confirm current lifecycle, reader/card technology, secure credential handling, interface/pinout, offline behaviour, environmental suitability and security update path. No monetary balance is stored on the card. |
| Auxiliary power / PSUs | Phoenix Contact STEP3, 1170953 | Study candidate; not approved for quad | Peripheral review records a 12 V / 2.5 A supply candidate; prior engineering review explicitly did not approve it for the quad cluster. | Build complete simultaneous load budget for controller/backplane, auxiliaries, contactor coils, safety and peripherals; include derating, inrush, fault isolation and thermal conditions. Select only after written compatibility and margin review. |
| CHARX accessory cable | Phoenix Contact 1360462 | Accessory candidate | Previously reviewed as a CHARX accessory cable. | Confirm exact mating function, supported variants, pinout, length, lifecycle and whether it is mandatory or optional for the chosen topology. |
| Protection / QF1, RCD1, SPD1, F1 | Exact manufacturer/model not defined | Architecture only | Functional protection requirements exist in the electrical architecture and safety chain. | Qualified designer to complete prospective short-circuit current, coordination, RCD/DC detection, surge category, installation earthing and selectivity study before exact part selection. |
| Contactor and driver / KM1, KMD1 | Exact manufacturer/model not defined | Architecture only | Per-output contactor, feedback and safe de-energisation are required. | Select from exact load category, continuous current, ambient/enclosure temperature, electrical endurance, coil voltage/inrush, suppression, auxiliary feedback and weld-detection evidence. Validate interface against controller output limits. |
| Type 2 interface / X1, CP/PP | Exact manufacturer/model not defined | Architecture only | Each output requires its own Type 2 interface and local CP/PP safety/control. | Select socket/tethered assembly, locking actuator, cable, temperature sensing, ingress protection, mechanical retention and applicable conformity evidence per output rating and enclosure. |
| Enclosure / ENC1, MP1, DIN1, DUCT1, GL1, PE1 | Exact manufacturer/model not defined | Architecture only | M1.20–M1.22 define conceptual zones, service and capacity requirements. | Exact component envelopes, thermal loss, environment, IP/IK, corrosion, structural loads, cable bend radii and installation/service clearances are prerequisites. No dimensioned CAD or enclosure selection yet. |
| HMI, network and payment / HMI1, ETH1, LTE1, WIFI1, ANT1 | Exact manufacturer/model not defined | Optional architecture only | These remain optional modules with reserved physical/electrical provisions. | Define use cases, interfaces, cybersecurity/update lifecycle, antenna placement, data/privacy and payment-provider requirements. No device selected. |

## 4. Mandatory dossier fields before selection

Each candidate dossier must contain, at minimum:

1. Manufacturer, exact order code, product designation, hardware variant and document/firmware revision.
2. Current lifecycle state and dated manufacturer evidence.
3. Manufacturer source register with document title, source URL, retrieval date and locally stored source file where licensing permits.
4. SHA-256 of each controlled local evidence file; hashes must be generated from the actual bytes.
5. Electrical ratings and operating conditions relevant to the actual application, with units and explicit conditions.
6. Terminal schedule, mating accessories, connector/pinout evidence and interface ownership.
7. Mechanical envelope evidence under M1.25, including datum, units, orientation and separate installation/service envelope.
8. Compatibility matrix against controller, meter, protection, enclosure and software/firmware dependencies.
9. Known failure modes, safe state, diagnostics, lifecycle/support and cybersecurity/update considerations.
10. Open questions, risk owner, reviewer role/date/scope and independent second-person review before design release.

Do not populate a numeric dimension from a product photograph, retailer page, search snippet or visually scaled model. Do not use a third-party model as dimensional authority.

## 5. Selection gates

| Gate | Required evidence | State |
|---|---|---|
| G1 — identity | Exact manufacturer order code, variant and revision | OPEN |
| G2 — lifecycle | Current manufacturer lifecycle/support evidence | OPEN per candidate |
| G3 — electrical | Ratings, load category, derating and protection coordination | OPEN |
| G4 — interfaces | Terminal schedule, pinout, mating parts and protocol details | OPEN |
| G5 — safety | Safe state, failure behaviour, diagnostics and protective coordination | OPEN |
| G6 — metrology | Certificate scope, meter topology and billing-use-case suitability | OPEN where applicable |
| G7 — mechanical | M1.25 provenance-backed envelope and service access | OPEN |
| G8 — integration | Compatibility and bench evidence in the target configuration | NOT STARTED |
| G9 — supply chain | Availability, lead time, lifecycle, warranty and alternatives | OPEN |
| G10 — approval | Independent technical review and documented decision | OPEN |

## 6. Relationship to CAD evidence control

M1.27 does not create component-envelope JSON records. A candidate can enter the mechanical evidence library only after its exact SKU/variant is established and a permitted manufacturer drawing/CAD/datasheet or verified measurement is available. M1.26 validator tests and CI execution remain a separate gate; the presence of this register does not make the validator pass.

## 7. Current engineering conclusion

The controller, metering and peripheral shortlist is sufficiently structured for targeted manufacturer evidence requests, but not for a production BOM. The highest-value next actions are:

1. Resolve exact CHARX SEC-1000/SEC-3xxx variants, terminal schedule, cluster power and failure isolation.
2. Resolve the per-output metrology route: EMH iML e-moc OCMF prototype versus EEM-XM355 point-meter/load-management route, without conflating their roles.
3. Complete the complete 12 V load budget before selecting a cluster supply.
4. Obtain exact protection, contactor, Type 2 and enclosure evidence only after the relevant electrical/mechanical design inputs are fixed.
5. Send the controlled supplier RFI only after the project owner authorises external contact.

**Release statement:** no production component is selected or approved by M1.27. No purchasing, mains energisation, fabrication, installation, billing approval or commercial deployment is authorised. Physical, thermal, environmental, structural and bench tests remain NOT STARTED unless separately evidenced.


## M1.28 source-audit amendment — CHARX exact order numbers

The 2026-11-17 primary-source audit in `docs/03-engineering/CHARGER-HARDWARE-V1-M1-28-CHARX-CONTROLLER-MANUFACTURER-EVIDENCE-AUDIT.md` resolves the previously incomplete controller identity:

- CHARX SEC-1000 local output-controller study candidate: **1139034**.
- CHARX SEC-3000 cluster/server study candidate: **1139022**.
- CHARX SEC-3050 ISO/IEC 15118 variant: **1139018**.
- CHARX SEC-3100 cellular 4G/2G variant: **1139012**.
- CHARX SEC-3150 cellular + ISO/IEC 15118 variant: **1138965**.

The SEC-1000 and SEC-3xxx contactor terminal arrangements differ and must not be treated as interchangeable. Manufacturer documentation states a maximum of 11 SEC-1000 modules per SEC-3xxx and a 6 A nominal backplane current limit; the proposed four-point configuration still requires a complete worst-case current budget and fault-injection evidence. These exact product identities are now source-backed at desk-review level, but remain study candidates, not approved components. See M1.28 for manufacturer source URLs, interfaces, electrical values and open gates.
