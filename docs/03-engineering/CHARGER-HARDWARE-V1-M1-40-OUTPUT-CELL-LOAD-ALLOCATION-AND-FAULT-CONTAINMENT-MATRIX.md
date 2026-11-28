# VAZÃO EVSE Charger Hardware V1 — Output Cell Load Allocation and Fault-Containment Matrix (M1.40)

**Status:** ARCHITECTURE DECISION INPUT / ALLOCATION OPEN / NO AUXILIARY TOPOLOGY SELECTED  
**Date:** 2026-11-28  
**Scope:** Auxiliary-load ownership, channel boundaries and fault-containment questions for Single, Dual, Quad and future MultiStation AC chargers  
**Parent:** M1.33 Auxiliary Power Budget Evidence Matrix; M1.39 Modular Auxiliary Distribution Architecture Review

## 1. Purpose and decision boundary

M1.40 turns the AUX-01–AUX-16 inventory into a product-family allocation matrix. It identifies the default engineering ownership question for each load: per Output Cell, charger-shared, site/park-shared, or optional/configuration-dependent.

The labels in this document are **allocation classes for analysis**, not approved wiring decisions:

- **CELL:** function belongs to one independently controlled charging output. Physical supply may still be shared only if fault containment is demonstrated.
- **CHARGER-SHARED:** service may serve several cells within one charger, subject to availability, isolation and common-cause analysis.
- **SITE-SHARED:** park-level infrastructure serving multiple chargers; it must not become a dependency for local output safety.
- **OPTIONAL:** present only in a defined product configuration; its absence must not disable mandatory local charging safety.
- **OPEN:** evidence is insufficient to assign a final physical supply domain.

No power-supply voltage/rating, controller, rail, fuse, conductor, protection device, contactor or distribution topology is selected. This document does not authorise schematic/BOM release, testing or energisation.

## 2. Load ownership matrix — AUX-01 to AUX-16

| ID | Load / function | Analysis ownership | Single / Wallbox 1 | Dual / Wallbox 2 | Quad pedestal | MultiStation / park | Fault-containment requirement | Evidence gate |
|---|---|---|---|---|---|---|---|---|
| AUX-01 | EVSE controller | CELL unless an exact supported multi-output controller architecture is evidenced | One cell controller candidate | Explicitly prove one-per-cell or validated shared controller | Explicitly prove four-cell grouping or per-cell control | Charger-local controllers; park supervisor separate | Controller or its supply failure must not create unintended energisation; shared controller failure impact must be bounded | AP-01, AP-06, AP-10 |
| AUX-02 | Controller peripherals / expansion | Follows the controller/interface function; OPEN per module | Map each interface to its consuming function | No unverified sharing across cells | No implicit sharing across four cells | Separate charger-local and site modules | Peripheral short/reset must not corrupt unrelated safety control or feedback | AP-01, AP-05, AP-09 |
| AUX-03 | Contactor / switching actuator coil | CELL | One actuator per output | Two independently commanded actuator functions | Four independently commanded actuator functions | Per output, irrespective of park master | Coil short, open circuit or failed pickup must be isolated and detected; no cross-cell actuation | AP-02, AP-06, AP-07, AP-09 |
| AUX-04 | Switching feedback / signal conditioning | CELL | Feedback for the single output | Independent state evidence for each output | Independent state evidence for each output | Per output; park telemetry is supplementary | One channel's feedback fault must not be interpreted as another channel's safe state | AP-02, AP-06, AP-09 |
| AUX-05 | Residual-current detection interface | CELL safety function; physical device topology OPEN | One validated protection boundary | Preserve independent protection boundary per output unless a certified design explicitly proves otherwise | Preserve independent protection boundary per output | Per output; site monitoring cannot replace local protection | Loss, trip or fault of one channel must not silently disable or mask another channel's protection | AP-03, AP-06, AP-09, AP-10 |
| AUX-06 | Metering / energy measurement | CELL by default; shared metering only with explicit validated architecture | Metering for one output | Separate attributable measurement per output | Separate attributable measurement per output | Per output; park aggregation above charger level | Meter/interface failure must not affect another output's measurement attribution or safety control | AP-04, AP-06 |
| AUX-07 | RFID / NFC reader | OPTIONAL; CELL by default, shared only if product UX and security model justify | Optional reader for one output | Reader per output or shared user interface — OPEN | Reader per output or managed shared interface — OPEN | Charger or site access layer, but local authorization fallback must be defined | Reader failure must not interrupt an active safe charging session; no dependency for electrical protection | AP-05, AP-07 |
| AUX-08 | Ethernet interface / switch | CHARGER-SHARED or CELL according to network design; OPEN | One port/interface or small local switch | Shared switch possible, with per-cell interface isolation | Shared switch possible, with channel separation | Site network may be shared; charger boundary retained | Network fault or switch power failure must not affect local safety; assess shared switch as common-cause outage | AP-05, AP-06, AP-09 |
| AUX-09 | LTE modem / router | OPTIONAL; CHARGER-SHARED or SITE-SHARED | Optional local modem | One shared modem possible if service capacity and outage policy validated | One shared modem possible if service capacity and outage policy validated | Site gateway candidate; local chargers remain autonomous | Modem transmit/inrush must not disturb control rail; loss of WAN/CPMS cannot defeat local safe operation | AP-05, AP-07, AP-09 |
| AUX-10 | HMI / display / indicators | OPTIONAL; CELL or CHARGER-SHARED by user-interface design | Optional local HMI | Dedicated per output or common display — OPEN | Per-output indication must remain unambiguous if common display used | Site signage/HMI supplementary | HMI fault must not obscure mandatory local safety state or control another cell | AP-05, AP-06, AP-07 |
| AUX-11 | Payment terminal / peripherals | OPTIONAL; CELL or CHARGER-SHARED subject to transaction attribution | Optional payment function | Shared terminal only with explicit session-to-output binding | Shared terminal only with explicit session-to-output binding | Site payment service possible; local electrical control independent | Payment failure must not cause unsafe switching or cross-charge sessions; transaction failure handling defined | AP-05, AP-06, AP-07 |
| AUX-12 | Temperature / door / environmental sensors | CELL where monitoring protects an output; enclosure sensors may be CHARGER-SHARED | Cell sensors plus enclosure sensors as justified | Per-cell safety sensors remain attributable; enclosure sensors may be shared | Same principle for all four cells | Charger sensors plus site environmental data | Shared sensor fault must not conceal a cell-local overtemperature or access condition | AP-04, AP-06, AP-09 |
| AUX-13 | Cooling / ventilation | CHARGER-SHARED for enclosure thermal management; local devices may be partitioned | Enclosure-level thermal function | Shared cooling possible only after thermal and fault analysis | Shared cooling possible only after thermal and fault analysis | Site HVAC is supplementary, not assumed | Loss/stall must be detected where cooling is safety-relevant; thermal protection must not depend solely on a shared fan | AP-07, AP-08, AP-09 |
| AUX-14 | Local load manager | CHARGER-SHARED for charger coordination; SITE-SHARED for park coordination | Local limiter may be integrated or separate | Charger-level coordinator may allocate between two cells | Charger-level coordinator may allocate between four cells | Park master coordinates charger limits; charger-local limits remain authoritative | Loss of manager must produce a defined conservative local limit; no cloud dependency for safety | AP-06, AP-07, AP-09, AP-10 |
| AUX-15 | Payment printer / receipt mechanism | OPTIONAL; follows payment terminal ownership | Optional per unit | Shared printer only if transaction/output identity is preserved | Shared printer only if transaction/output identity is preserved | Site printer possible as commercial service | Motor/heater peak must not brown out controller or safety interfaces; jam/fault isolated to payment function | AP-05, AP-07, AP-09 |
| AUX-16 | Service / diagnostic interface | CELL for safety-connected diagnostics; CHARGER-SHARED only for isolated service infrastructure | One controlled service boundary | Access to each cell must remain distinguishable | Access to each cell must remain distinguishable | Site service network is separate from charger safety interfaces | Service connection cannot bridge isolation, bypass protection or inject unsafe commands; access controlled | AP-01, AP-06, AP-09, AP-10 |

**Interpretation rule:** a CELL ownership label does not require a separate PSU. A shared physical source may supply multiple CELL loads only after branch protection, fault discrimination, voltage stability, isolation and safe-state consequences are evidenced. Conversely, a CHARGER-SHARED label does not permit a common electrical connection to safety-critical circuits without a reviewed design.

## 3. Product-family count and simultaneity model

| Product configuration | CELL quantity basis | Shared services | Required budget cases | Unresolved decision |
|---|---:|---|---|---|
| Single / Wallbox 1 | 1 | Charger controller/network/HMI services as configured | Standby, charging, contactor pickup, communications burst, optional transaction, fault and recovery | Controller grouping and which services are optional |
| Dual / Wallbox 2 | 2 | Charger-level services may be shared | One cell active; both active; simultaneous switching; one-cell fault while other operates; shared-service failure | Whether common services can be shared without unacceptable common-cause failure |
| Quad pedestal | 4 | Charger-level services may be shared | 1/2/3/4 cells active; credible simultaneous switching; optional modules concurrent; one-cell branch fault; shared-source fault | Repeatable per-cell boundary and acceptable shared-domain failure envelope |
| MultiStation / park | Explicit number of cells per charger and chargers per site | Site network, park supervisor and optional shared services | Per-charger peak; park coincidence; WAN loss; park-master loss; charger isolation; recovery after communications return | Charger-vs-site ownership and local autonomy boundaries |

The eventual current budget must not multiply a nominal single-cell value blindly. For each configuration, record actual fitted quantities, supported operating states and credible simultaneity. Where simultaneity is unknown, mark the case OPEN rather than assuming diversity.

## 4. Fault propagation and containment matrix

| Initiating event | Potential propagation | Minimum design evidence required | Acceptance status |
|---|---|---|---|
| Common auxiliary source fails | All loads on that source reset or drop | Affected-load map; defined safe state per output; restart inhibit; recovery sequence; source fault behaviour | OPEN |
| One cell branch short / overload | Shared source voltage collapse or protection trip affecting other cells | Branch protection coordination; fault current; selectivity; wiring and connector limits; test plan | OPEN |
| Controller/backplane overload | Multiple controllers reset or lose functions | Exact topology; total configured load; vendor bus limit; simultaneous I/O profile; derating and fault behaviour | OPEN |
| Optional modem/RFID/HMI/payment/printer surge | Disturbance of controller or protection interface supply | Exact peak/inrush profiles; source transient response; separated branches; worst-case coincidence | OPEN |
| Contactor coil short or failed pickup | Shared rail disturbance; output cannot switch as commanded | Coil profile; independent branch protection; command/feedback truth table; fault reaction | OPEN |
| Cell-local sensor/interface failure | False safe indication or loss of protection visibility | Diagnostic coverage; fault-state mapping; independence and plausibility checks | OPEN |
| Shared network/switch failure | Loss of CPMS, HMI, payment or park coordination | Offline operation; local control limits; transaction/session recovery; no safety dependency | OPEN |
| Park master or WAN failure | Site-level allocation unavailable | Local fallback limit; stale-command handling; reconnection and resynchronisation rules | OPEN |
| Brownout / repeated power recovery | Unintended output restart or contactor re-pickup | Undervoltage/reset behaviour; safe boot state; restart interlock; event logging | OPEN |
| Cooling failure | Temperature rise across several cells | Thermal model; sensor placement; derating/shutdown thresholds from controlled design; independent overtemperature response | OPEN |
| Service-port misuse or isolation failure | Cross-domain coupling or unsafe command path | Interface isolation; access control; safe-state and service-mode interlocks; verification evidence | OPEN |

No acceptance status is closed by the existence of this matrix. These rows define evidence needed before architecture approval.

## 5. Controller supply specification discrepancy — explicit hold point

The manufacturer sources currently recorded in M1.39 show two published supply statements:

- The manufacturer hardware-wiring help page states **+12 V DC ±0.6 V** for the controller supply.
- The SEC-1000 product catalog page for item **1139034** states **12 V DC ±5%** (11.4–12.6 V).

These statements are not numerically identical. This matrix does not assume that one supersedes the other, that they apply to the same hardware revision, or that the tighter interval is a universal operating requirement. Exact applicability must be resolved against the controlled SEC-1000 manual and hardware revision before a rail can be specified.

**Hold point AP-01:** obtain the official manual binary, inspect its internal title/revision/date and model applicability, verify its SHA-256 against the manufacturer-published checksum, and record the relevant supply specification and any errata. Until then, the supply input range remains **OPEN — CONFLICTING/PARTIAL SOURCE STATEMENTS**. Do not select or set a 12 V rail from this document.

The CHARX backplane nominal 6 A remains specific to that manufacturer backplane. It is not a VAZÃO EVSE distribution rating and does not resolve the supply-range discrepancy.

## 6. Architecture alternatives — decision criteria, not scoring

| Criterion | Central shared source | Per-cell auxiliary domains | Hybrid domains |
|---|---|---|---|
| Common-cause outage | Potentially broad; must be bounded | More naturally limited per cell, shared services still remain | Depends on partition and shared-domain size |
| Component count / service burden | Potentially lower | Potentially higher | Intermediate, configuration-dependent |
| Cell isolation | Requires carefully coordinated branches | Potentially clearer | Must be explicitly demonstrated |
| Quad scalability | Depends on total demand and fault containment | Repeated cell pattern, more hardware | Potentially scalable if group boundaries are proven |
| Optional accessory disturbance | Needs explicit segregation | Can isolate per cell | Can separate optional and safety-critical domains |
| Evidence maturity today | Insufficient | Insufficient | Insufficient |

No weighted score is assigned. Cost, space or component count cannot override safety boundaries. A decision requires exact load data, protection coordination, fault analysis, thermal evidence and independent review.

## 7. Traceability to M1.33 evidence gates

| Gate | Required closure evidence | M1.40 impact |
|---|---|---|
| AP-01 | Exact controller supply range, configured consumption, manual revision and applicability | Required for AUX-01/AUX-02 and all controller-fed loads |
| AP-02 | Contactor coil pickup, hold, inrush, duty and suppression | Required for per-cell AUX-03 and branch demand |
| AP-03 | Residual-current interface/protection auxiliary demand and fault behaviour | Required for per-cell AUX-05 |
| AP-04 | Meter, sensor and signal-conditioning data | Required for AUX-04/AUX-06/AUX-12 |
| AP-05 | Exact optional RFID, LTE, Ethernet, HMI, payment and printer profiles | Required for AUX-07 to AUX-11 and AUX-15 |
| AP-06 | Quantities and shared/per-cell allocation for each product | Central purpose of this matrix; still OPEN until architecture review |
| AP-07 | Simultaneity across normal, startup, fault and recovery modes | Required for Single/Dual/Quad/MultiStation peak cases |
| AP-08 | Enclosure thermal and derating evidence | Required for source and cooling allocation |
| AP-09 | Isolation, transient response, branch protection and fault behaviour | Required for every proposed shared or per-cell domain |
| AP-10 | Independent engineering review of calculations and architecture | Required before architecture selection or schematic release |

## 8. Required decision record before architecture selection

The next decision package must contain, at minimum:

1. Controlled controller and peripheral document set, with exact model/revision applicability and verified binary custody.
2. Completed AUX-01–AUX-16 configuration register with quantities and exact supply profiles.
3. Per-product simultaneity cases for Single, Dual and Quad, including optional-module combinations and fault/recovery states.
4. Proposed domain diagram identifying CELL, CHARGER-SHARED and SITE-SHARED boundaries.
5. Branch protection and isolation coordination evidence for every shared source feeding cell-local loads.
6. Fault tree / fault propagation review demonstrating no unacceptable cross-cell effect and deterministic safe states.
7. Thermal and enclosure derating evidence.
8. Independent review sign-off and documented unresolved deviations.

## 9. Design disposition

| Decision item | M1.40 status |
|---|---|
| AUX-01–AUX-16 functional ownership model | MAPPED FOR REVIEW; physical allocation OPEN |
| Single / Wallbox 1 architecture | OPEN |
| Dual / Wallbox 2 architecture | OPEN |
| Quad architecture | OPEN |
| MultiStation / park allocation | OPEN |
| Central source vs per-cell vs hybrid | NO PREFERENCE / EVIDENCE INSUFFICIENT |
| Controller/backplane suitability | NOT APPROVED |
| 12 V rail specification | HOLD — source discrepancy unresolved |
| PSU, fuse, conductor, connector and protection selection | NOT SELECTED |
| Schematic/BOM release | NOT AUTHORISED |
| Bench/mains testing or energisation | NOT CLAIMED / NOT AUTHORISED BY THIS DOCUMENT |

## 10. Next milestone

M1.41 should close the controller-document evidence hold point if the exact official manual binary can be acquired and verified, then update AP-01 with controlled supply and configured-load facts. If the binary remains unavailable, record the retrieval attempts and preserve AP-01 as OPEN; do not infer a rail specification. In parallel, exact peripheral candidates may be researched without selecting them or changing the architecture decision.

No supplier contact, procurement, physical test, mains test, certification or compliance approval is claimed.
