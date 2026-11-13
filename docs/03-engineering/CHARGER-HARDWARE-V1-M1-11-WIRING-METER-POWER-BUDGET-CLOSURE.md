# VAZÃO EVSE — Charger Hardware V1 — M1.11: wiring evidence, meter lifecycle and 12 V power-budget closure

**Status:** PARTIAL — evidence boundary tightened; no wiring, meter or PSU release.  
**Branch:** `feat/charger-hardware-v1-component-selection`  
**Date:** 2026-11-08  
**Depends on:** M1.5A, M1.8, M1.9 and M1.10.

## 1. Executive result

M1.11 does not justify freezing a terminal-numbered wiring schedule, a MID billing meter, or a 12 V cluster supply. It does, however, close several decision errors and makes the remaining calculations explicit.

- The current CHARX manual landing page identifies **UM EN CHARX SEC, Revision 06**, firmware **1.9.1**, and covers SEC-3150 (1138965), SEC-3100 (1139012), SEC-3050 (1139018), SEC-3000 (1139022) and SEC-1000 (1139034). The page is reviewed 2026-06-29.
- The accessible manual landing page does not expose its complete figure/terminal schedule in machine-readable content. The existing M1.8 functional connector register must therefore remain a *functional* register, not be promoted to numbered terminal wiring.
- EEM-MA370-R **2907980** is an active product page candidate with Modbus RTU/TCP. The page extraction available here does not establish MID certification, a direct-current-input topology suitable for the intended EVSE feeder, CHARX protocol integration, or point-of-sale legal suitability. It is **not approved** as a billing meter.
- EEM-MA370 **2907983** is a distinct non-R model; manufacturer page describes Modbus/TCP, 3-phase capability, 100–230 V AC supply, CT secondary current inputs (1 A / 5 A), 10 VA max dissipation, IP20 and functional insulation on the communication interface. Do not substitute it for 2907980 or assume MID status.
- No 12 V supply can be selected from the available figures. SEC controller 2 A standalone maximum, the 6 A nominal backplane limit, and accessory currents are different constraints and cannot be added or interpreted as a complete cluster budget.

**Decision:** retain CHARX modular as the leading study architecture only. No final component selection or production release.

## 2. Wiring evidence boundary

### 2.1 Verified manufacturer manual identity

Official manual landing page:  
https://www.phoenixcontact.com/charx-help/_general/User_Manual.htm

It identifies UM EN CHARX SEC Revision 06, firmware 1.9.1 and the five controller item numbers listed above. The manual page was published/reviewed 2026-06-29.

Official product/download entry for SEC-1000:  
https://www.phoenixcontact.com/en-pc/products/ac-charging-controller-charx-sec-1000-1139034

### 2.2 Functional signals already evidenced

The M1.8 connector register remains the source for the functional groups: supply/RFID, OUT1…OUT4, IN1…IN4/PTC, meter, RCM, socket CP/PP/lock/LED, contactor, Ethernet, USB-C, cellular antenna and SIM. These names are not terminal numbers.

The following details are still **not verified sufficiently for a manufacturing drawing**:

- connector manufacturer/series and exact plug housing/contact part numbers for every group;
- terminal numbers and pin order for each SEC-3xxx variant and SEC-1000;
- wire cross-sections per terminal, ferrules, strip lengths and tightening torques for each connector;
- approved conductor routing, segregation, shield termination and PE bonding details;
- contactor coil voltage, inrush/holding current, suppression, and whether the controller output can drive the selected interface directly;
- exact auxiliary-contact feedback semantics and welded-contactor diagnostic sequence;
- approved external RCD/RCM arrangement and coordination for each output;
- meter terminal assignment and the validated CHARX meter profile/register map.

**Rule:** no pin number, wire colour, torque or connector SKU may be inferred from a functional signal name or a product photograph. Capture the exact figure/page from the manufacturer manual and the matching accessory documentation before adding it to the terminal schedule.

## 3. Meter lifecycle and suitability review

| Candidate | Evidence found | Decision |
|---|---|---|
| ISKRA WM3M4C 1429603 | Phoenix product page previously marked “no longer in product range” | Block new procurement |
| EEM-MA370-R 2907980 | Manufacturer product page identifies Modbus/RTU/TCP | Keep as investigation candidate; MID, direct/CT topology, CHARX compatibility and billing suitability open |
| EEM-MA370 2907983 | Manufacturer page identifies Modbus/TCP; 3-phase/2-phase/single-phase; current inputs 1 A or 5 A secondary; supply 100–230 V AC; max dissipation 10 VA; IP20 | Not a drop-in replacement; CT-based input and supply/interface differ; MID not established |
| EEM-EM355 2908578 / EEM-XM375 1674510 | Previous lifecycle review recorded these as alternatives to investigate | No approval until exact current datasheet, MID certificate, interface, measurement topology and CHARX integration are verified |

Manufacturer references:
- EEM-MA370-R 2907980: https://www.phoenixcontact.com/en-pc/products/measuring-instrument-eem-ma370-r-2907980
- EEM-MA370 2907983: https://www.phoenixcontact.com/en-pc/products/measuring-instrument-eem-ma370-2907983
- EMpro energy meters: https://www.phoenixcontact.com/en-pc/products/energy-monitoring/energy-measuring-devices-and-energy-meters

### 3.1 Required meter closure evidence

Before selection, obtain written confirmation for each intended use:
1. Is the meter MID-certified for the exact model/variant and applicable measurement class? Obtain certificate and scope.
2. Is it a direct-connected meter or CT-operated? Record primary/secondary ratios, burden, CT accuracy and anti-tamper requirements.
3. Does it measure the complete energy delivered by one EVSE output, with no shared loads?
4. Is there a supported CHARX firmware/profile and exact register map, including scaling, signed values, phase mapping, reset behaviour and communication-loss handling?
5. Can the reading be attributed to the correct EVSE transaction and retained through power/network restart?
6. Does the selected national/legal billing model require MID or other metrological controls? Confirm with the compliance specialist for Portugal before claiming compliant billing.

Until then, distinguish **operational energy telemetry** from **legally suitable billing measurement**.

## 4. 12 V supply and distribution — calculation framework

### 4.1 Constraints that must not be conflated

- SEC-3xxx / SEC-1000 supply data previously extracted: 12 V ±5%.
- Controller maximum standalone consumption previously recorded: up to 2 A. This is not a measured normal draw and must not be multiplied blindly to declare cluster current.
- CHARX DIN-rail backplane: 6 A nominal limit. This is a hard bus constraint, not proof that the whole 12 V auxiliary system may draw 6 A, nor permission to inject auxiliary loads into the bus.
- RFID/NFC PCB 1391227: manufacturer data recorded in M1.10 gives typical 100 mA at 12 V.
- Lock actuator peak/holding current, RCM current, sensor loads, I/O, indicators, external relays and any HMI/network accessory remain to be sourced or measured.
- STEP3-PS/1AC/12DC/2.5/PT 1170953 (12 V, 2.5 A) is **not approved** for a quad assembly.

### 4.2 Required separated power domains

Create a power tree with at least these explicitly documented domains:
- **PWR-CTRL/BACKPLANE:** controller cluster supply using only the manufacturer-approved feed arrangement and respecting the 6 A nominal backplane limit.
- **PWR-AUX-12V:** separately fused auxiliary distribution for approved peripherals/actuators, unless Phoenix explicitly approves a shared feed and documents the current path.
- **PWR-COIL:** contactor coil supply/interface sized for coil inrush and switching duty; do not assume the SEC output is a coil driver.
- **PWR-SAFETY:** RCM and other safety-related devices supplied as specified by their manufacturer, with supply failure detected where required.

No arbitrary backplane injection, parallel supplies or commoning of independently protected domains.

### 4.3 Budget equations

For each supply domain, build a load schedule from manufacturer maximum/peak values or measured worst-case values:

`I_domain = Σ(I_continuous,max) + Σ(I_peak,coincident)`

For auxiliary 12 V, a preliminary worksheet is:

`I_AUX = N_RFID × 0.10 A + N_lock × I_lock,peak + N_RCM × I_RCM + I_sensors + I_IO + I_indicators + I_other`

This is a formula, not a completed budget. The 0.10 A RFID value is typical only; obtain maximum current and startup transient before sizing.

For the controller/backplane domain:

`I_BUS,measured,max ≤ 6 A nominal backplane limit`

The controller standalone 2 A maximum is a data point for an individual standalone controller, **not** evidence of four independent 2 A consumers on one bus. Obtain manufacturer-approved cluster loading and verify it on a bench with all modules, locks and peripherals in worst-case operation.

A 20% engineering reserve may be used as an internal design target after the complete worst-case load is known; it is not a manufacturer rating, does not replace temperature/derating calculations, and never permits exceeding the 6 A bus limit.

### 4.4 Configuration worksheet

| Configuration | Controller arrangement under study | Additional load items | Release condition |
|---|---|---|---|
| 1 output | Standalone SEC-1000 or selected SEC-3xxx architecture | 1 point meter, optional RFID, one lock, one RCM | Measure actual controller and simultaneous accessory peaks |
| 2 outputs | SEC-3xxx + 1 SEC-1000 (topology under study) | 2 point meters, 2 locks, up to 2 RCM channels; shared/individual RFID to be proven | Confirm bus feed and worst-case current; test client/server loss |
| 4 outputs | SEC-3xxx + 3 SEC-1000 (topology under study) | 4 point meters, 4 locks, up to 4 RCM channels; shared/individual RFID to be proven | Manufacturer-approved bus budget, measured peak load and fault containment |

The table is not a statement that the proposed cluster is approved or that one RCM/reader can serve several outputs.

## 5. Bench validation plan (SELV only)

Before any mains-connected test:
1. Assemble the controller cluster and approved power feed on a current-limited SELV bench.
2. Log input voltage/current at startup, steady idle, all outputs enabled, all locks actuated in the worst credible overlap, RFID polling, RCM operation and communication activity.
3. Repeat at minimum/maximum intended ambient temperature or apply manufacturer derating data.
4. Inject one fault at a time: controller supply undervoltage, bus open, one SEC-1000 removed, SEC-3xxx reset, meter disconnected, RFID disconnected, RCM supply loss, lock short/open, and auxiliary branch short (with protective devices in place).
5. Verify every output's safe state, diagnostics, recovery policy, transaction continuity and no unintended re-energisation.
6. Record instrument calibration, firmware, hardware revisions, configuration export, measured waveforms/logs and pass/fail criteria.

No test in this plan authorises energising the AC power path. Any later mains test requires a qualified laboratory/engineer, approved test procedure and suitable protective equipment.

## 6. Architecture decision

**Keep CHARX modular as a candidate, not as a frozen design.** The shared SEC-3xxx/backplane cluster has dependencies that must be explicitly fault-tested. If a single point of failure is unacceptable, compare a four-controller independently supplied architecture with an external load-management master. Do not claim local autonomy, session continuity or safe failover without manufacturer evidence and tests.

## 7. M1.11 gate status

| Gate | Status |
|---|---|
| Manual revision and supported controller models identified | PARTIAL — identity verified; terminal/figure extraction incomplete |
| Terminal-numbered wiring schedule | OPEN |
| Current MID meter selected | OPEN |
| Meter-to-CHARX integration/register map | OPEN |
| Approved cluster power-feed arrangement | OPEN |
| Complete 1/2/4-output 12 V budgets | OPEN |
| SELV fault-injection evidence | NOT RUN |
| Production BOM/wiring release | BLOCKED |

## 8. Next closure actions (M1.12)

1. Obtain the full Revision 06 manual PDF and exact accessory/package-slip documents; extract each relevant wiring figure with page/figure identifiers.
2. Obtain Phoenix written confirmation of the approved SEC-3xxx/SEC-1000 cluster supply/feed, maximum simultaneous module load and fault behaviour on bus/master loss.
3. Obtain full datasheets and MID certificates for 2907980, 2908578 and 1674510; request explicit CHARX compatibility and register-profile support.
4. Build a measured SELV current budget for 1/2/4 outputs and select supplies only after derating, inrush, protection and thermal calculations.
5. Update terminal schedule and BOM only from verified manufacturer documents and measured test evidence.

**Safety statement:** This document is engineering evidence management, not a wiring instruction, conformity assessment, construction certificate or permission to energise. Final design must be reviewed against applicable IEC/EN EVSE requirements and Portuguese/EU legal obligations by qualified professionals.
