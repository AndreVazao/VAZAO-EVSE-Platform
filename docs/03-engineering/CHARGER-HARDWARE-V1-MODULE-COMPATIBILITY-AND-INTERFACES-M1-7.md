# VAZÃO EVSE — Module Compatibility and Interface Register (M1.7)

**Status:** DRAFT / EVIDENCE REGISTER — NOT A RELEASED WIRING DESIGN  
**Date:** 2026-11-02  
**Applies to:** V1 single-, dual- and quad-output AC EVSE, wallbox and pedestal  
**Controller family under evaluation:** Phoenix Contact CHARX control modular

## 1. Purpose and governing rule

M1.7 converts the modular product requirement into a controlled compatibility and interface register. The product shall be orderable with a minimum safe charging configuration and with independently selected options. An interface being present on a controller does not mean the peripheral must be installed.

**Critical distinction:** controller capability, optional peripheral, and mandatory safety function are three different things. A controller may expose an RFID RS-485 interface while the RFID reader is omitted. A meter interface may be built in, while the actual meter is selected according to billing, calibration and regulatory requirements. A communications-capable gateway may be omitted from a standalone product, provided the chosen controller topology supports local standalone operation.

No unverified connector pinout, mating part number, bus limit or safety function is to be inferred from product photographs or a family brochure.

## 2. Manufacturer evidence snapshot

The following information was extracted from Phoenix Contact manufacturer pages and current online help/manual pages on 2026-11-02:

| Item | Manufacturer item no. | Confirmed published properties relevant to modularity |
|---|---:|---|
| CHARX SEC-1000 | 1139034 | 12 V DC ±5%; max 2 A in standalone operation; 18.8 mm wide; DIN-rail bus; separate RS-485 energy-meter and RFID interfaces; CP/PP vehicle interface; residual-current detection interface; temperature interface; contactor floating contact |
| CHARX SEC-3000 | 1139022 | 12 V DC ±5%; max 2 A in standalone operation; 37.6 mm wide; two Ethernet RJ45; USB-C configuration; DIN-rail system bus; RS-485 energy-meter and RFID interfaces; same general local EVSE interface families |
| CHARX SEC-3100 | 1139012 | SEC-3xxx functionality plus cellular interface (LTE CAT1; micro-SIM and SMA antenna interface according to manufacturer family data) |
| CHARX SEC-3050 | 1139018 | SEC-3xxx variant with ISO/IEC 15118 support according to manufacturer family data |
| CHARX SEC-3150 | 1138965 | SEC-3xxx variant with cellular interface and ISO/IEC 15118 support according to manufacturer family data |

Manufacturer references:
- SEC-1000 product page: https://www.phoenixcontact.com/en-pc/products/ac-charging-controller-charx-sec-1000-1139034
- SEC-3000 product page: https://www.phoenixcontact.com/en-pc/products/ac-charging-controller-charx-sec-3000-1139022
- SEC-3xxx technical appendix: https://www.phoenixcontact.com/charx-help/Appendix/CHARX_SEC-3xxx.htm
- Current user manual landing page (firmware 1.9.1, revision 06): https://www.phoenixcontact.com/charx-help/_general/User_Manual.htm

**Important:** The manufacturer describes SEC-1000 as Stand-Alone/Client and SEC-3000 as Stand-Alone/Client/Server. The SEC-3000 product page reports no integrated modem; cellular is identified for SEC-3100 and SEC-3150. Therefore, do not describe Wi-Fi or LTE as built-in to every SEC-3xxx controller. Ethernet, cellular and Wi-Fi are distinct choices. Wi-Fi is not confirmed as an integrated interface by this evidence.

## 3. Modular option compatibility matrix

Legend:
- **Base** — mandatory function or equipment for the declared product configuration.
- **Optional** — may be omitted; omission must not compromise local safety.
- **Variant** — select a controller/module variant at order time; not assumed to be a hot-swappable daughterboard.
- **TBD** — manufacturer or design evidence still required.

| Function / module | Basic public standalone | RFID option | Ethernet/CPMS option | LTE option | HMI/payment option | Classification and integration rule |
|---|---:|---:|---:|---:|---:|---|
| Local EVSE controller and CP/PP | Base | Base | Base | Base | Base | One validated local control/safety function per output |
| Power switching and feedback | Base | Base | Base | Base | Base | Per-output safety path; independent of optional modules |
| Protective devices / residual-current safety | Base | Base | Base | Base | Base | Never an optional commercial module |
| Energy meter | Per declared use case | Same | Same | Same | Same | Decide whether legally/billing-required; not to be removed merely to reduce BOM |
| RFID reader and antenna | Omit | Optional fitted | Optional fitted | Optional fitted | Optional fitted | Controller RFID port may remain unused; no reader needed in open-access mode |
| Ethernet cable/network | Omit | Omit | Optional fitted | Optional | Optional | SEC-3000 family offers two Ethernet ports; confirm exact gateway and network architecture |
| Cellular modem/SIM/antenna | Omit | Omit | Omit | Variant/module | Optional | SEC-3100/3150 cellular variant is not equivalent to a generic plug-in modem |
| Wi-Fi radio/antenna | Omit | Omit | TBD | TBD | Optional/TBD | Not confirmed as integrated in the reviewed CHARX variants; evaluate external certified module/gateway separately |
| Display/HMI | Omit | Omit | Optional | Optional | Optional | Must not be needed to initiate safe local charging |
| Payment terminal | Omit | Omit | Optional | Optional | Optional | Requires independent payment-provider, security and reconciliation design |
| Remote telemetry/service | Omit | Optional | Optional | Optional | Optional | Must degrade to local operation when absent |
| Optional external I/O | Omit | Optional | Optional | Optional | Optional | Isolated/protected and mapped only after interface verification |

### 3.1 Minimum public-access configuration

The public-access, no-RFID, no-network product shall:
- run its validated local EVSE state machine without CPMS;
- use an explicitly configured open-access/local release policy;
- not wait for RFID, SIM, Wi-Fi, Ethernet or backend authorisation;
- retain the mandatory local electrical safety functions;
- expose a documented commissioning and service method;
- record local energy/session data to the extent supported by the selected meter/controller and declared product requirements.

This mode must be tested from cold start, after power loss, and with all optional communications and RFID interfaces physically unpopulated.

### 3.2 RFID configuration

RFID is an optional peripheral, not a mandatory property of every charger. If fitted, document:
- exact reader SKU and approved antenna/interface;
- RS-485 wiring, addressing and cable constraints from the reader manual;
- mechanical aperture/mounting and IP rating;
- reader power source and protection;
- offline credential policy and secure credential handling;
- behaviour when the reader is disconnected or fails.

Do not infer that one RFID reader can authorise several outputs, or that every output requires a separate reader, without validating the chosen user experience and controller firmware architecture.

### 3.3 Communications configuration

Treat each medium independently:
- Ethernet: physical port, surge/EMC protection, cable route and network isolation.
- LTE: exact controller variant or separately approved modem, antenna, SIM, RF path and country-band support.
- Wi-Fi: separate certified radio solution if required; no claim of native CHARX Wi-Fi support at this stage.
- CPMS: application-level option, not part of the local safety loop.

No network failure may cause uncontrolled contactor operation. Any backend-dependent commercial policy must be explicitly distinguished from the local safety state machine.

## 4. Controller topology for 1 / 2 / 4 outputs — status

Phoenix publishes a scalable cluster example of one class-3000 plus eleven class-1000 controllers for twelve charging points, with further clusters managed by a class-3000 server architecture. This is useful evidence of the family concept, but it does not by itself approve the VAZÃO four-output topology.

| Product | Study topology only | Status |
|---|---|---|
| Single output | One SEC-1000 standalone, or an appropriate SEC-3xxx variant where communications/server functions are required | Candidate; confirm full function set and standalone configuration |
| Dual output | Two local output controllers; one selected gateway/controller may supervise if required | Open; confirm cluster/bus and independent failure behaviour |
| Quad output | Four local output controllers/output cells; gateway role chosen according to validated cluster topology | Open; do not freeze controller count from the 12-point brochure diagram |

The SEC-3000 is itself described as an AC charging controller with vehicle interface and contactor-control interface; do not automatically count it as a gateway-only device. The exact number of independently controlled outputs in a four-device assembly must be confirmed against the current manual's system topology and manufacturer application support.

## 5. Interface register — what is known and what is not

| Interface | Published evidence | VAZÃO design action |
|---|---|---|
| SEC modular bus | DIN-rail bus connector, one interface per controller | Record exact rail/bus accessory, permitted arrangement, segment topology and current budget from current manual |
| Meter | RS-485 interface on SEC-1000 and SEC-3000 | Select exact meter SKU; confirm protocol, address, termination, cable and per-output attribution |
| RFID | RS-485 interface on SEC-1000 and SEC-3000 | Keep reader optional; exact reader pinout and power must come from reader-specific manual |
| CP/PP | IEC 61851-1 vehicle interface | Use the controller's dedicated interface; no raw MCU connection |
| Lock actuator | Published ±12 V, 2 A for the vehicle interface | Confirm actuator part number, inrush, duty and connector schedule |
| RCM | Dedicated 12 V sensor/interface signals | Select sensor and verify RCM + RCD coordination; no assumption that monitoring replaces protective disconnection |
| Temperature | Pt1000 or PTC chain | Select sensors and define trip limits/placement from validated design |
| Contactor | Floating switch contact; product data gives max switching voltage/current and interrupting rating | Verify actual coil type, inrush, suppression, isolation, auxiliary feedback and weld-fault strategy; do not drive a coil directly without this check |
| Digital I/O | Four inputs and four outputs; outputs max 600 mA according to product data | Allocate only after load and fault-state review |
| Ethernet | SEC-3000 two RJ45 ports, 10/100 Mbps | Optional network wiring; verify ESD/surge and isolation design |
| Cellular | SEC-3100/3150 family data, micro-SIM and SMA antenna interface | Optional variant; verify country bands, antenna placement and supplier availability |
| USB-C | SEC-3xxx configuration/diagnostics | Service interface only; do not expose as a customer-facing charging requirement |

### 5.1 Unresolved connector/pinout gate

This register intentionally does **not** publish invented connector pin numbers or bus accessory order codes. M1.8 must extract exact connector designations, pin numbering, plug/terminal part numbers, mating accessories, conductor sizes, torque/strip requirements and wiring figures from the current revision 06 / firmware 1.9.1 manual and each peripheral's own manual. Every extracted item must include source page/figure/table and hardware variant.

## 6. Supply and thermal budgeting

Manufacturer product pages list a maximum 2 A standalone consumption for SEC-1000 and SEC-3xxx devices, at 12 V DC ±5%. That is a maximum controller consumption figure, not a complete VAZÃO module budget.

For each assembly, calculate:
- controller consumption for the selected number and type of controllers;
- reader, meter, RCM, sensors, relays and external I/O loads;
- any backplane-powered peripheral loads;
- startup/inrush and transient margins;
- branch protection, conductor sizing, voltage drop and thermal rise;
- worst-case enclosure ambient temperature and module dissipation.

The previously extracted manual's nominal 6 A backplane limit must be treated as a hard design constraint pending exact manual figure/conditions. Do not infer that a single 12 V / 6 A supply is automatically suitable for four outputs: all loads and distribution conditions must be included. Provide separately protected branches where appropriate and ensure optional-module short circuits cannot propagate into the local safety core.

## 7. Mechanical slots and harness rules

The enclosure/panel design shall reserve, as supported by the product variant:
- an identified mounting position for each option family;
- protected, keyed, labelled interface connectors;
- separate routing zones for mains, SELV/PELV and communications;
- blanking covers for unused external apertures;
- antenna mounting and RF clearance only on cellular/Wi-Fi configurations;
- cable restraint, bend radius and service loops;
- thermal allowance for maximum populated configuration;
- module identity and revision label.

A reserved connector must not be energised unless the option is fitted and commissioned. Unused conductors must be safely terminated, and unused ports protected against accidental contact, moisture and EMC issues.

## 8. Required configuration SKUs

The product configurator shall generate at least these profiles, without treating them as frozen commercial SKUs yet:

| Profile | Required population |
|---|---|
| BASE-PUBLIC | Mandatory safe charging core; no RFID; no external network module |
| BASE-METERED | Base plus meter required by declared billing/calibration use case |
| RFID-LOCAL | Base plus approved RFID reader; no network required |
| ETH-CONNECTED | Base plus approved Ethernet/gateway variant |
| LTE-CONNECTED | Base plus approved LTE variant, SIM and antenna |
| FULL-SERVICE | Base plus selected RFID, communications, HMI/payment and telemetry modules |

Profiles must be available for 1-, 2- and 4-output enclosures only after the matching controller, thermal, protection and wiring configurations have passed validation.

## 9. Verification plan and acceptance criteria

1. **No-option build:** all outputs operate locally with RFID, WAN/LAN and HMI absent.
2. **RFID-only build:** reader works; disconnecting it follows a defined policy and does not corrupt local safety.
3. **Ethernet-only build:** network can be commissioned without requiring LTE or Wi-Fi.
4. **LTE build:** antenna/SIM are present and tested; no modem is assumed on SEC-3000 or SEC-1000.
5. **Mixed configuration:** each output has its declared option population; configuration records match physical assembly.
6. **Optional branch fault:** a short/disconnection in an optional module branch does not create an unsafe state in unrelated outputs.
7. **Gateway/network loss:** local CP/PP and protective functions continue; remote features are reported unavailable.
8. **Controller/bus fault:** affected outputs enter deterministic safe states; independence claims require fault-injection evidence.
9. **Meter loss:** readings are flagged invalid/unavailable, never fabricated; billing policy is explicit.
10. **Power-cycle:** local policy, credentials (if applicable), configuration and transaction recovery behave as specified.

## 10. Open gates for M1.8

- Exact manual page/figure extraction for every connector and accessory.
- Manufacturer confirmation of 4-output controller topology and failure isolation.
- Exact per-output meter and RFID wiring, including whether a shared reader architecture is supported.
- Approved 12 V supply/distribution design for each populated option profile.
- Wi-Fi solution decision; do not imply native CHARX support.
- Contactor/coil and feedback compatibility.
- Final RCM/RCD and protective-device coordination.
- Enclosure dimensions, reserved mounting/blanking, thermal and IP/IK verification.
- Current availability, lifecycle, firmware support, cybersecurity lifecycle and supplier quotations.

**Safety notice:** this is a controlled architecture/interface evidence register, not a final terminal schedule, construction drawing, conformity assessment or permission to energise mains-connected equipment.
