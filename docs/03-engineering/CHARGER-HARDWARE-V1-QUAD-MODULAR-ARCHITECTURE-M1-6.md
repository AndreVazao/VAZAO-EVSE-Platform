# VAZÃO EVSE — Quad Modular Architecture (M1.6)

**Status:** DRAFT / ARCHITECTURE REQUIREMENTS — NOT A RELEASED DESIGN  
**Date:** 2026-11-02  
**Applies to:** 1-, 2- and 4-output AC EVSE variants, wallbox and pedestal  
**Related gate:** M1.5 / M1.5A CHARX modular controller evaluation

## 1. Decision: modularity is a product-level requirement

Every VAZÃO EVSE device shall be designed as a configurable assembly of a mandatory safe charging core and optional functional modules. This is not merely a software feature or an accessory retrofit.

A customer must be able to order, for example:
- a basic public-access charger with no RFID reader and no network connection;
- the same charger with RFID;
- the same charger with Ethernet, Wi-Fi or LTE;
- a connected charger with RFID and HMI;
- a later upgraded configuration, where the mechanical, electrical and firmware compatibility gates permit it.

The enclosure, mounting plate, DIN rail/supports, cable ducts, connector positions, auxiliary power distribution and harness plan shall anticipate the supported option set. Unpopulated positions are reserved, labelled and safely blanked; they are not left with exposed live terminals or loose wiring.

## 2. Product architecture layers

### 2.1 Mandatory charging/safety core (per output)

Each independently usable charging output requires, at minimum, its own appropriately rated and coordinated:
- power path and branch protection, selected for the declared electrical rating and installation;
- contactor/switching device and verified feedback strategy;
- EVSE control function implementing the applicable Mode 3 / IEC 61851 control behaviour;
- CP/PP interface and Type 2 connection;
- local protective/safety inputs and fault handling, including the required residual-current protection/monitoring architecture;
- energy measurement where required by the product's declared billing/regulatory use case;
- temperature and other monitoring required by the validated design;
- local state machine and safe stop behaviour.

The exact protection topology, RCD/DC detection, meter class, conductor sizing and switching components remain subject to the final electrical design and applicable standards. A common enclosure or master controller does not make these functions optional.

### 2.2 Shared platform / base services

The base assembly provides the mechanical chassis, protected auxiliary supply distribution, labelled terminal/interface areas, controller mounting, internal wiring infrastructure, earthing/bonding provisions, service access and the minimum local configuration/diagnostic interface required for commissioning.

Shared services must be sized for the maximum explicitly supported module population, or divided into separately protected and rated branches. No spare connector may be assumed capable of carrying a load until its voltage, current, protection, isolation and thermal rating are documented.

### 2.3 Optional functional modules

| Module family | Optional function | Absent-module behaviour |
|---|---|---|
| RFID | User identification / access control | Public/free-to-use or other configured local policy; no RFID dependency |
| Ethernet | Wired LAN / CPMS connectivity | Local standalone operation |
| Wi-Fi | Wireless LAN | Local standalone operation |
| LTE + antenna/SIM | Wide-area connectivity | No cellular dependency |
| HMI/display | User prompts/status | Basic local indicators or documented no-display behaviour |
| Payment interface | Payment terminal/provider integration | No payment hardware or payment claim |
| Advanced metering | Enhanced reporting / per-session billing data | Only the meter required by the base product's declared use case remains |
| Auxiliary I/O | External sensors, access, building integration | Inputs safely terminated/disabled |
| Remote service/telemetry | Diagnostics and remote maintenance | Local service procedure remains available |

An option may itself require several submodules (e.g. LTE modem, antenna, SIM and protected supply). The BOM and configuration tool must treat the complete compatible set as one selectable option.

## 3. Physical modularity rules

1. Reserve defined mounting zones and dimensions for each supported option family.
2. Provide keyed or otherwise unambiguous connectors; publish pinout, voltage, current, isolation and mating-part references.
3. Use separate, labelled connector groups for mains, protective earth, SELV/PELV auxiliary power and communications. Maintain required segregation and creepage/clearance.
4. Provide protected blanking plates/covers for unpopulated apertures and finger-safe protection for unused electrical interfaces.
5. Keep optional module wiring out of the mandatory safety chain unless that option is explicitly part of the declared operating mode.
6. Provide strain relief, EMC bonding/shield termination and antenna routing provisions where relevant.
7. Make module replacement possible without disturbing the power path or safety-critical wiring wherever practical.
8. Define the maximum thermal dissipation and enclosure/IP/IK impact for every supported populated configuration.
9. Provide a configuration label or machine-readable configuration record showing installed modules, hardware revisions and firmware compatibility.
10. No field retrofit is permitted unless the module, firmware, enclosure and electrical installation are on the approved compatibility matrix.

## 4. Electrical and firmware behaviour when modules are absent

- Unpopulated module supplies must be isolated or switched off by design; unused conductors must be safely terminated.
- Missing RFID must not prevent charging in a configuration whose access policy is public/free or otherwise locally authorised.
- Missing WAN/LAN must not prevent local safety operation. CPMS-dependent commercial features may be unavailable, but the EVSE safety controller must remain autonomous.
- A missing HMI must not block charging; user feedback must follow the documented base configuration.
- Firmware must detect/declare optional module presence where the interface supports detection. Otherwise, the commissioning profile must explicitly record the installed option set.
- Missing or failed optional modules must not silently downgrade electrical protection or bypass a safety interlock.
- A module fault may stop the affected output if it compromises that output's safety; it must not stop unrelated outputs unless the fault is in a genuinely shared resource whose failure makes continued operation unsafe.
- Shared supply, gateway or bus failure behaviour must be explicitly designed and tested. Do not promise output independence until demonstrated.

## 5. Quad-output architecture target

The four-output pedestal shall be decomposed into four repeatable output cells plus shared platform services.

**Per output cell (x4):** dedicated power branch, local EVSE control/safety, contactor and feedback, CP/PP, connector/lock interface as applicable, and separately attributable metering where required.

**Shared services:** enclosure/chassis, incoming distribution, auxiliary supply branches, protective-earth system, optional communications gateway, optional RFID/HMI/payment modules, and local multi-output load allocator.

The load allocator may reduce or allocate available current, but it shall not replace any output's local safety controller. Loss of CPMS or external communications must not disable local electrical protection. The design shall define whether failure of a shared controller, bus or auxiliary supply affects one output or all outputs; the safe result must be deterministic and verified.

### Controller topology — not yet frozen

The Phoenix Contact CHARX control modular SEC-1000 / SEC-3000 family remains a study candidate. The published family scaling diagram is not, by itself, proof that a particular four-output bill of materials, bus layout, supply arrangement, meter arrangement or failure-containment design is approved.

M1.7 must verify from the exact current manuals and manufacturer confirmation:
- whether one SEC-1000 is required per output and the exact role of the selected SEC-3000 variant;
- whether a four-output group is a supported topology without an unnecessary extra controller;
- how per-output meters are connected and independently addressed;
- the exact bus connector/accessories, permitted physical arrangement and current budget;
- auxiliary supply loading for the chosen module population;
- behaviour on SEC-3000 loss, SEC-1000 loss, bus interruption and supply-branch failure;
- contactor output compatibility, coil suppression and feedback/weld-detection coverage.

Until those checks are complete, no exact controller count, terminal schedule or production wiring shall be inferred from the 48-point family diagram.

## 6. Fault-containment and validation matrix

| Injected condition | Required design response | Evidence required |
|---|---|---|
| RFID module absent | Public/local policy works; no false authorisation dependency | Functional test in no-RFID configuration |
| Network modules absent | Local charging and safety remain available under configured policy | Offline test, power-cycle and event persistence |
| HMI absent | Charging remains possible; documented local indication | No-HMI test |
| One output controller fails | Affected output enters safe state; other outputs continue only if shared resources remain safe | Multi-output fault-injection test |
| Shared gateway fails | Local output safety remains active; loss of supervisory features is explicit | Gateway-disconnect test |
| Inter-controller bus opens | Deterministic safe response; no uncontrolled contactor operation | Bus interruption at defined points |
| Auxiliary supply branch fails | Only dependent functions/outputs affected; no backfeed | Branch-isolation test |
| Meter communication fails | Billing/energy-data policy is explicit; never fabricate readings | Meter disconnect and recovery test |
| Contactor feedback mismatch / welded contact | Output is locked out and fault latched according to validated safety design | Feedback fault-injection test |
| RCM/RCD fault | Correct local protective response; no master/cloud dependency | Instrumented protection test by qualified personnel |
| Optional module short or miswire | Branch protection prevents propagation; safety core remains protected | Protected bench fault test |

## 7. Configuration and commercial model

The product configurator/BOM shall express each device as:
- mandatory base SKU;
- output count and electrical rating;
- optional module SKUs and compatible combinations;
- factory-installed vs field-installable status;
- firmware/configuration profile;
- resulting enclosure, power-supply, thermal and wiring variant.

The quote and build record must not include RFID, communications, HMI or payment hardware unless selected. The absence of an option must also remove its associated consumables (antenna, SIM, cable, mounting accessory, etc.) while retaining the prepared mounting/interface provisions where specified.

## 8. Release gates

M1.6 establishes requirements and the quad-output decomposition; it does not release fabrication. Before design freeze:
- close M1.7 controller topology and exact manufacturer interface evidence;
- create a module compatibility matrix and connector/pinout register;
- complete per-configuration power, protection, thermal and enclosure calculations;
- produce separate wiring schedules for minimum, RFID, connected and fully equipped variants;
- validate single-, dual- and quad-output fault containment;
- review applicable EU/Portuguese standards and regulatory requirements with qualified engineering support.

**Safety notice:** this is an architecture requirements document, not a construction drawing, compliance assessment or permission to energise mains-connected equipment.
