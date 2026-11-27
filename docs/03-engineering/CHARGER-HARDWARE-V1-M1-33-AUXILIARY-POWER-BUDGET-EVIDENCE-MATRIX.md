# VAZÃO EVSE Charger Hardware V1 — Auxiliary Power Budget Evidence Matrix (M1.33)

**Status:** LOAD INVENTORY / NO POWER SUPPLY OR RAIL SELECTED  
**Date:** 2026-11-27  
**Scope:** Auxiliary electrical loads for one Output Cell and shared charger services  
**Parent:** M1.30 controller evidence review; M1.31 protection matrix; M1.32 contactor and feedback architecture

## 1. Purpose and boundary

This milestone establishes the evidence structure needed to calculate auxiliary power demand before selecting an auxiliary power supply, voltage rail, fuse, conductor or distribution topology.

The inventory distinguishes:
- continuous/steady-state demand;
- startup, inrush and transient demand;
- actuator pickup and holding demand;
- optional-module demand and operating-mode simultaneity;
- shared loads versus per-Output-Cell loads.

This is a documentary engineering gate. It is not a power-supply design, wiring schedule, component selection, safety approval or authorisation to energise.

## 2. Budget rules

1. No load value is accepted without an identifiable manufacturer source and controlled document revision.
2. Typical, maximum, peak, startup and holding values must not be mixed or treated as interchangeable.
3. AC input power, DC output power and current on a named DC rail must be recorded separately.
4. Every value must identify voltage, tolerance, operating condition, temperature where relevant, and whether external peripherals are included.
5. Unknown values remain **OPEN / EVIDENCE GAP**; they are not estimated from similar products.
6. Per-output loads and shared loads must be counted separately to avoid omission or double counting.
7. Optional RFID, LTE, Ethernet, HMI and payment modules must be budgeted by configuration, including simultaneous operation where supported.
8. A cloud/CPMS connection is not assumed to be available for local safe operation; safety-critical local functions must remain powered and deterministic under the defined offline modes.
9. No arbitrary design margin is inserted. Margin and derating must be justified after the load envelope, source characteristics and applicable requirements are evidenced.

## 3. Load inventory and evidence matrix

| ID | Load / interface | Scope / quantity basis | Candidate / exact model | Supply rail / voltage | Steady current or power | Startup / inrush / peak | Pickup / hold (if applicable) | Source, revision and date | Evidence status | Safety criticality | Simultaneity / operating mode |
|---|---|---|---|---|---|---|---|---|---|---|---|
| AUX-01 | EVSE controller | Shared or per-cell — topology OPEN | Phoenix CHARX SEC-1000 (1139034) is an evidence candidate only | Catalog states 12 V DC ±5% | Catalog states max. 2 A standalone; no-load <50 mA without external loads | External-load startup profile not evidenced | N/A | Current catalog evidence reviewed in M1.30; controlled manual revision and archived source still OPEN | PARTIAL — catalog only | High | Continuous while charger control is active; exact modes OPEN |
| AUX-02 | Controller peripheral interfaces / expansion modules | Per selected controller configuration | Exact module set OPEN | OPEN | OPEN | OPEN | N/A | Exact controlled controller and module manuals required | OPEN / EVIDENCE GAP | High | Depends on installed modules and active functions |
| AUX-03 | Switching actuator coil | Per Output Cell; count follows output count | No contactor/relay selected | Coil rail OPEN | OPEN | Pickup/inrush OPEN | Pickup and holding values OPEN | Exact actuator datasheet and coil variant required | OPEN / EVIDENCE GAP | High | Switching events; duty and simultaneity OPEN |
| AUX-04 | Switching feedback / signal conditioning | Per Output Cell | Method and components OPEN | OPEN | OPEN | OPEN | N/A | Feedback device and interface datasheets required | OPEN / EVIDENCE GAP | High | Continuous or sampled mode OPEN |
| AUX-05 | Residual-current detection interface (AC/DC) | Per Output Cell or shared arrangement only if validated | Device/interface OPEN | OPEN | OPEN | OPEN | N/A | Exact protection-device documentation and interface limits required | OPEN / EVIDENCE GAP | Critical | Continuous monitoring; fault-state demand OPEN |
| AUX-06 | Metering / energy measurement | Per Output Cell unless selected architecture proves otherwise | Exact meter OPEN | OPEN | OPEN | OPEN | N/A | Meter datasheet and communication-interface documentation required | OPEN / EVIDENCE GAP | Medium / safety interface as applicable | Measurement active/standby modes OPEN |
| AUX-07 | RFID / NFC reader | Optional, per installed reader | Exact reader OPEN | OPEN | OPEN | OPEN | N/A | Manufacturer datasheet including RF transmit peak required | OPEN / EVIDENCE GAP | Low for energy delivery; access-control impact | Reader active, polling and standby modes OPEN |
| AUX-08 | Ethernet interface / switch | Shared or per-cell, topology OPEN | Exact device(s) OPEN | OPEN | OPEN | OPEN | N/A | Datasheets and port-load conditions required | OPEN / EVIDENCE GAP | Medium | Link-up, traffic, PoE if any (not assumed) |
| AUX-09 | LTE modem / router | Optional, shared or per charger | Exact modem/router and antenna configuration OPEN | OPEN | OPEN | TX burst / registration peak OPEN | N/A | Manufacturer power profile across network states required | OPEN / EVIDENCE GAP | Low for local safety; operational connectivity | Registration, transmit bursts, weak-signal condition |
| AUX-10 | HMI / display / indicators | Optional, per installed panel | Exact display, brightness and indicator set OPEN | OPEN | OPEN | Backlight/display startup OPEN | N/A | Datasheets at defined brightness and temperature required | OPEN / EVIDENCE GAP | Low, except safety indication requirements | Active, dimmed and standby modes OPEN |
| AUX-11 | Payment terminal / peripherals | Optional, per payment configuration | Exact certified terminal and peripherals OPEN | OPEN | OPEN | Transaction / modem / printer peak OPEN | N/A | Manufacturer integration and power documentation required | OPEN / EVIDENCE GAP | Low for power path; payment availability | Idle, transaction and peripheral activity |
| AUX-12 | Temperature / door / environmental sensors | Quantity and distribution OPEN | Exact sensor family OPEN | OPEN | OPEN | Startup OPEN | N/A | Datasheets and signal-conditioning requirements required | OPEN / EVIDENCE GAP | Medium / High where used in protection | Continuous monitoring and fault state |
| AUX-13 | Auxiliary cooling / ventilation | Enclosure thermal design not frozen | Fan or thermal device not selected | OPEN | OPEN | Motor startup / locked-rotor demand OPEN | N/A | Thermal study and exact manufacturer data required | OPEN / EVIDENCE GAP | Medium / potentially high if thermal safety depends on it | Thermostat-controlled or continuous mode OPEN |
| AUX-14 | Local controller / load manager | Shared charger or park controller, architecture-dependent | Exact controller OPEN | OPEN | OPEN | Startup and communication peak OPEN | N/A | Exact datasheet and operating profile required | OPEN / EVIDENCE GAP | High for load-limit enforcement | Offline, online, degraded and recovery modes |
| AUX-15 | Optional payment printer / receipt mechanism | Per payment-equipped unit | Exact printer OPEN | OPEN | OPEN | Motor/heater peak as specified by manufacturer | N/A | Exact printer datasheet and duty cycle required | OPEN / EVIDENCE GAP | Low | Print cycle and standby; simultaneous loads OPEN |
| AUX-16 | Service / diagnostic interface | Shared or per-cell | Exact interface OPEN | OPEN | OPEN | Connection/startup OPEN | N/A | Interface and isolation documentation required | OPEN / EVIDENCE GAP | High if it interfaces with safety/control | Service-only; normal operation isolation rules OPEN |

**Important:** The SEC-1000 figures above are catalog-level evidence already recorded in M1.30, not a complete load profile. The stated 2 A maximum must not be interpreted as a verified system-wide consumption value or as permission to size a supply. External loads, startup profile and exact controlled manual remain unresolved.

## 4. Configuration and quantity model

The eventual budget must be calculated for explicit product configurations, not a generic charger total:

| Configuration | Per-output loads | Shared loads | Optional modules | Quantity / simultaneity evidence |
|---|---|---|---|---|
| Single pedestal / Wallbox 1 | One Output Cell | Controller, communications and shared services as selected | RFID, LTE, Ethernet, HMI, payment | OPEN |
| Dual pedestal / Wallbox 2 | Two independent Output Cells | Shared controller/network only where architecture permits | Options per product configuration | OPEN |
| Quad pedestal | Four independent Output Cells | Shared services and local distribution as selected | Options per product configuration | OPEN |
| MultiStation / park | Output Cells per charger plus park-level controls | Master/load manager/network infrastructure | Site-dependent | OPEN |

For dual and quad products, the auxiliary budget must preserve the distinction between per-cell loads and common loads. The AC feeder alternatives (independent feeders or common trunk with local distribution) do not determine the DC auxiliary topology automatically; both must be explicitly designed and evidenced.

## 5. Calculation method — values intentionally not populated

For each named rail and each supported configuration, the calculation record must include:

- **Steady-state demand:** sum of the verified steady currents of loads active in that operating mode, multiplied by their evidenced quantities.
- **Peak demand:** maximum credible coincident demand using manufacturer-defined peak values and a documented simultaneity model.
- **Startup/inrush:** time-dependent demand and duration, including the source's ability to start the complete connected load without voltage collapse or unintended reset.
- **Actuator demand:** pickup and holding conditions evaluated separately, including the credible number of simultaneous switching events.
- **Operating modes:** startup, idle/standby, charging, communications activity, payment transaction, fault response, service and recovery.
- **Source capability:** output rating across input range, temperature and derating; transient response; overload/current-limit behaviour; isolation and protection characteristics.
- **Distribution losses:** verified cable, connector and conversion losses once rail voltage, topology, route and conductor data exist.

No numerical totals, rail voltages, PSU ratings, fuse ratings, conductor sections or design margins are issued in M1.33 because the necessary source data and architecture are incomplete.

## 6. Evidence required to close the budget

| Gate | Required evidence | Status |
|---|---|---|
| AP-01 | Controlled controller manual, exact revision, input range and complete consumption profile | OPEN |
| AP-02 | Exact contactor/relay coil datasheet: pickup, hold, inrush, duty and suppression constraints | OPEN |
| AP-03 | Selected residual-current/protection interfaces and their auxiliary consumption | OPEN |
| AP-04 | Meter, sensor and signal-conditioning candidate datasheets | OPEN |
| AP-05 | RFID/NFC, LTE, Ethernet, HMI and payment module exact candidates and profiles | OPEN |
| AP-06 | Shared-versus-per-cell allocation and quantities for single/dual/quad variants | OPEN |
| AP-07 | Simultaneity matrix for all operating and fault modes | OPEN |
| AP-08 | Environmental and thermal derating assumptions supported by enclosure design | OPEN |
| AP-09 | Source isolation, transient response, fault behaviour and protection coordination requirements | OPEN |
| AP-10 | Independent engineering review of calculations and selected auxiliary architecture | OPEN |

## 7. Safety and design constraints

- Loss of auxiliary power must not cause uncontrolled re-energisation or defeat a required safe state.
- Local safety and protection functions must not depend on RFID, payment, LTE, Ethernet, HMI or CPMS availability.
- Auxiliary supply faults must be assessed for propagation between Output Cells and shared services.
- Any shared rail must be evaluated for a single fault affecting multiple outputs.
- Service/diagnostic connections must not bypass isolation, protection or safe-state behaviour.
- The eventual power architecture must identify galvanic isolation boundaries and protective-earth relationships from controlled component evidence and qualified review.

## 8. Disposition and next milestone

M1.33 creates the load inventory, evidence fields, configuration model and calculation method. All AP-01–AP-10 remain OPEN. No auxiliary PSU, rail voltage, fuse, conductor, converter, load module or distribution topology is selected. No schematic/BOM freeze, bench test, mains test or energisation is claimed.

Next: obtain and archive controlled manufacturer documents for the controller and candidate auxiliary loads, resolve shared/per-cell allocation, then populate the budget with traceable steady, peak and inrush data before any supply selection.
