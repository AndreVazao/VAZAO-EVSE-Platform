# VAZAO EVSE TestStation V1 — M1.7 Power Architecture, Protection & Contactor/Load Topology

**Status:** Engineering baseline — not production-approved  
**Branch:** `feat/charger-hardware-v1`  
**Product:** VAZAO EVSE TestStation V1  
**Related architecture:** M1.2–M1.6  
**Next milestone:** M1.8 — Concrete electrical schematics + protection/coordination worksheet

---

## 1. Purpose

M1.7 defines the physical power architecture for the VAZAO EVSE TestStation V1, including 230/400 VAC three-phase input, Zone A and Zone B diagnostic power paths, main isolation, protective-device architecture, contactor topology, EVSE-under-test interface, programmable load path, 24 VDC control distribution, PE/protective bonding, emergency isolation, and thermal/fault-management strategy.

This document separates architecture that can be frozen now, candidate component ratings, and values that require site/install-specific calculations before release.

No protective-device rating, breaking capacity, conductor section, or final contactor selection in this document is a substitute for the final electrical design and applicable standards review.

---

## 2. Design envelope

| Parameter | V1 baseline |
|---|---|
| Supply | 3P + N + PE, 400/230 VAC, 50 Hz |
| Maximum EVSE test current | 32 A/phase |
| Maximum EVSE test power | 22 kW |
| Measurement | Zone A + Zone B |
| Load | Programmable/staged AC load |
| Control supply | 24 VDC SELV/PELV architecture |
| Safety | Hardwired emergency/safety chain |
| Communications | CAN-FD + service interfaces |
| Product variants | Mini / PRO / Factory |

The nominal 400/230 V, 32 A/phase envelope is a design envelope, not an assumption that every installation can safely supply 22 kW. Final design must account for supply capacity, prospective short-circuit current, conductor length/section, installation method, ambient/grouping derating, voltage drop, earth-fault loop characteristics, selectivity, interrupt rating and PE arrangement.

---

## 3. Global power topology

Functional path:

**GRID → MAIN ISOLATOR → INPUT PROTECTION → K_MAIN → ZONE A → EVSE UNDER TEST → ZONE B → K_LOAD → PROGRAMMABLE LOAD**

Conceptual topology:

~~~text
      3P+N+PE 400/230 VAC
               │
        [MAIN ISOLATOR]
               │
      [INPUT PROTECTION]
               │
            [K_MAIN]
               │
        ┌──────┴──────┐
        │             │
   ZONE A          CONTROL/MEASURE
   L1/L2/L3/N      isolated sensing
        │
   [EVSE UNDER TEST]
        │
   ZONE B L1/L2/L3/N
        │
     [K_LOAD]
        │
 [PROGRAMMABLE LOAD]
        │
       RETURN
~~~

PE is continuous through the hazardous-power architecture and is not switched as an ordinary current-carrying conductor.

---

## 4. Main isolation

The TestStation shall have a mechanically accessible main isolation device capable of isolating the hazardous power domain.

Candidate architecture:
- 4-pole isolation where neutral isolation is required by the final installation/design;
- lockable handle;
- clearly marked ON/OFF;
- suitable for the maximum prospective fault level;
- mechanically robust for trolley operation.

The exact pole configuration must be confirmed against applicable installation and equipment requirements.

The main isolator shall not depend on software, remain identifiable when the TestStation is unpowered, provide a defined safe isolation state, be mechanically accessible, and support maintenance lockout/tagout procedures where applicable.

---

## 5. Input protection architecture

Conceptual stack:

~~~text
SUPPLY
  │
  ├── Main isolation
  │
  ├── Overcurrent / short-circuit protection
  │
  ├── Residual-current / earth-fault protection
  │   (architecture depends on final application)
  │
  ├── Surge protection where required
  │
  └── Contactor / controlled energisation
~~~

### Protection coordination

Protection cannot be selected from the 32 A nominal test current alone.

The final worksheet shall determine:
- Ib — design current;
- In — protective-device rated current;
- Iz — conductor current-carrying capacity;
- Icn/Icu/Ics or applicable interrupt ratings;
- prospective short-circuit current;
- upstream/downstream coordination;
- discrimination where required;
- thermal derating;
- voltage drop.

For a 22 kW three-phase load at 400 V:

I ≈ 22000 / (√3 × 400) ≈ 31.8 A

This supports a nominal 32 A/phase design envelope. It does not automatically determine the breaker rating.

---

## 6. Prospective short-circuit current

The TestStation design shall have a documented short-circuit assumption at the point of connection.

Required inputs:
- upstream transformer/source impedance;
- prospective short-circuit current;
- supply cable impedance;
- protective-device characteristics;
- maximum and minimum fault current where relevant;
- PE/earth fault loop impedance;
- upstream protective device.

**Hold point HP-M1.7-01:** do not freeze final protective-device breaking capacity until the prospective fault level is known.

If the TestStation is intended for multiple environments, the architecture should support an installation/application-specific protection module or documented site limits rather than assuming one universal fault level.

---

## 7. Zone A power path

Zone A represents the electrical condition presented to the EVSE under test.

~~~text
K_MAIN
  │
  ├── VA_L1 measurement
  ├── VA_L2 measurement
  ├── VA_L3 measurement
  ├── IA_L1 measurement
  ├── IA_L2 measurement
  └── IA_L3 measurement
  │
  └── EVSE input terminals
~~~

Zone A shall be physically and logically identifiable in wiring, harnesses, PCB channels and software.

The Zone A dataset is the reference for determining whether an abnormal condition was already present before the EVSE.

---

## 8. EVSE-under-test interface

The TestStation shall provide a controlled connection for the VAZAO EVSE supporting, as applicable:
- L1;
- L2;
- L3;
- N;
- PE;
- CP;
- PP;
- communications/service connections.

Optional diagnostic signals may include contactor feedback, controller alive, charging state, fault state, firmware ID, hardware revision, serial number and selected low-voltage diagnostic points. These must be isolated/protected according to the electrical domain.

---

## 9. Zone B power path

Zone B represents the electrical output/load side of the EVSE path.

~~~text
EVSE output / controlled test path
             │
       VB_L1/L2/L3
       IB_L1/L2/L3
             │
          K_LOAD
             │
     PROGRAMMABLE LOAD
~~~

Zone B data is stored independently from Zone A.

This allows comparison of input phase relationship, EVSE-side phase relationship, voltage, current, power, energy and, where implemented, harmonic/power-quality indicators.

---

## 10. Contactor topology

Logical functions:
- **K_MAIN** — main controlled energisation;
- **K_ZONE_A** — optional Zone A isolation/segmentation;
- **K_ZONE_B** — optional Zone B isolation;
- **K_LOAD** — load isolation;
- additional contactors only where a specific test function requires them.

Not every product variant must populate every logical contactor.

Candidate contactors shall be selected for utilization category, voltage, continuous current, making/breaking duty, switching cycles, inrush, ambient temperature, coordination with upstream protection, auxiliary feedback, mechanical endurance and electrical endurance.

For a 32 A/phase envelope, the final device should not be selected merely because its nominal current equals 32 A. Appropriate utilization category, thermal margin and switching duty must be considered.

### Welded-contact detection

~~~text
Command OFF
    │
    ├── Coil de-energised
    │
    └── Auxiliary contact confirms OPEN
             │
             ├── OPEN → safe progression
             └── CLOSED → fault / inhibit
~~~

The system shall never interpret a software command as proof that hazardous power is absent.

---

## 11. Emergency isolation

Emergency stop architecture is independent of normal application logic.

Baseline:

~~~text
[E-STOP]
   │
   ├── safety chain
   │
   ├── remove contactor coil energy
   │
   └── inhibit hazardous load
~~~

The MCU/software may monitor the event, but software must not be the sole means of achieving the safe state.

Emergency response shall consider K_MAIN, K_ZONE_A/K_ZONE_B where fitted, K_LOAD, load-enable path, stored energy, DC control supply and restart inhibition.

Automatic restart after E-stop shall not occur without a defined reset/restart sequence.

---

## 12. 24 VDC architecture

The control system uses a separated low-voltage domain.

~~~text
AC INPUT
   │
[Protected PSU]
   │
  24 VDC
   │
   ├── Safety chain
   ├── Contactors
   ├── Sensors
   ├── Fans
   ├── EV interface electronics
   ├── CAN nodes
   └── Main computer power conversion
~~~

Individual branches should have appropriate overcurrent/short-circuit protection, reverse-polarity protection where useful, and status monitoring for critical branches.

Where necessary, split safety power, measurement electronics, communications, actuator/contactor power and auxiliary loads so a non-critical load fault does not unnecessarily collapse the complete safety system.

---

## 13. PE / protective bonding

PE is a dedicated protective domain.

Requirements:
- low-impedance protective bonding;
- dedicated PE conductors;
- metal enclosure bonding;
- trolley/mechanical metalwork bonding where required;
- testable PE continuity;
- no software-controlled PE switching.

The PE architecture shall be verified during safety validation.

---

## 14. Load architecture

The load must reproduce controlled EVSE demand up to the V1 envelope.

At full resistive load:

P_thermal ≈ P_electrical

A 22 kW continuous test can therefore require substantial heat extraction.

The preferred architecture is staged/hybrid rather than one permanently active 22 kW element.

Possible stages:
- low-power verification;
- medium-power test;
- high-power test;
- programmable fine control.

Functional structure:

~~~text
             LOAD BUS
                │
       ┌────────┼────────┐
       │        │        │
    LOAD-1   LOAD-2   LOAD-3...
       │        │        │
      K1       K2       K3
       │        │        │
       └────────┴────────┘
                │
          thermal system
~~~

Actual element values are deferred until the thermal/mechanical design is frozen.

The load controller shall support commanded power/current, ramp-up, ramp-down, emergency shutdown, overtemperature shutdown, fan fault, load branch fault, contactor feedback and state reporting.

Most development/service tests do not require 22 kW continuous operation. The TestStation should prioritize low-power diagnostics, staged power, short high-power validation, and only explicit long-duration high-power tests.

---

## 15. Load thermal architecture

At 22 kW, nearly the full electrical energy becomes heat if a resistive load is used.

The design must define:
- resistor technology;
- enclosure airflow;
- fan redundancy;
- inlet/outlet arrangement;
- thermal sensors;
- hot-spot monitoring;
- emergency overtemperature trip;
- maximum continuous duty;
- cooldown cycle.

**Hold point HP-M1.7-02:** the 22 kW continuous rating shall not be declared until the thermal model and physical cooling design demonstrate the required duty cycle.

---

## 16. Load protection

Each major load branch should have coordinated protection.

The load system shall detect:
- overcurrent;
- open branch;
- unexpected current;
- contactor mismatch;
- overtemperature;
- fan failure;
- sensor failure.

A load fault shall force the load into a defined safe state.

---

## 17. Phase loading

The load architecture shall support:
- balanced three-phase loading;
- single-phase operation;
- controlled phase imbalance;
- phase-loss testing where safely implemented;
- selected abnormal-condition tests.

The software shall explicitly identify the active test mode.

Example balanced three-phase mode:
- L1 = 16 A
- L2 = 16 A
- L3 = 16 A

Example single-phase mode:
- L1 = 32 A
- L2 = 0 A
- L3 = 0 A

Actual permitted combinations depend on EVSE and TestStation configuration.

---

## 18. Phase-angle diagnostic path

The M1.2–M1.6 measurement architecture is preserved.

The TestStation calculates:
- φ(L1,L2);
- φ(L2,L3);
- φ(L3,L1).

Zone A and Zone B remain separate.

Example:

~~~text
Zone A:
L1-L2 = 120.1°
L2-L3 = 119.8°
L3-L1 = 120.1°

Zone B:
L1-L2 = 118.9°
L2-L3 = 121.7°
L3-L1 = 119.4°
~~~

The diagnostic engine should report measured facts first and then classify possible causes. It must not immediately conclude that a capacitor or a specific component is defective.

---

## 19. Capacitor / power-factor correction diagnostic guardrail

If phase displacement or reactive behavior indicates a possible compensation issue, the TestStation may calculate a candidate engineering correction.

Qc = P(tan φ1 − tan φ2)

For a three-phase capacitor bank, one possible formulation is:

C = Qc / (3ωV_phase²)

or the corresponding line-voltage formulation depending on connection.

The software must label the result:

**CANDIDATE ENGINEERING VALUE — NOT AN AUTOMATIC REPAIR INSTRUCTION**

Before any field modification, engineering review must consider voltage rating, frequency, tolerance, switching method, discharge, harmonics, resonance, temperature, dielectric duty, applicable standards, system short-circuit level and manufacturer limits.

---

## 20. Measurement/protection interaction

Measurement circuitry must never become the only protection mechanism.

For example, measured I = 0 A does not by itself prove that power is safely isolated.

Safe isolation requires the appropriate physical isolation/protection state and, where applicable, verified contactor feedback and voltage absence.

---

## 21. Connector and terminal architecture

The power path should use clearly segregated terminals for:
- incoming mains;
- Zone A;
- EVSE interface;
- Zone B;
- load;
- PE;
- 24 VDC;
- communications.

High-voltage terminals shall be physically separated from SELV/service connectors.

Service connectors shall not permit accidental connection into hazardous mains domains.

---

## 22. Conductor sizing methodology

Final conductor sections shall be selected using:
1. design current;
2. installation method;
3. ambient temperature;
4. grouping;
5. insulation temperature rating;
6. voltage drop;
7. short-circuit withstand;
8. terminal/device ratings;
9. mechanical constraints;
10. applicable standards.

A generic 32 A assumption must not be used as the sole basis.

**Hold point HP-M1.7-03:** freeze conductor cross-sections only after installation method, cable lengths, enclosure temperature and protection coordination are defined.

---

## 23. Terminal and busbar sizing

Busbars and terminals shall consider continuous RMS current, peak current, temperature rise, enclosure ventilation, fault withstand, creepage/clearance, mechanical short-circuit forces, connection torque and maintenance access.

Terminals shall be rated for the conductor type and expected temperature.

---

## 24. Protection and safety state machine

Baseline states:

~~~text
S0 OFF
  │
  ▼
S1 SELF-CHECK
  │
  ├── FAIL → FAULT
  │
  ▼
S2 SAFE-READY
  │
  ▼
S3 PRE-ENERGISE
  │
  ├── safety chain OK?
  ├── E-stop reset?
  ├── contactors verified?
  └── measurement healthy?
  │
  ▼
S4 ENERGISED
  │
  ▼
S5 TEST RUN
  │
  ├── fault → SAFE SHUTDOWN
  └── complete → SAFE SHUTDOWN
  │
  ▼
S6 SAFE SHUTDOWN
~~~

Any critical safety fault shall prevent progression to an energised state.

---

## 25. Fault matrix

| Fault | Detection | Safe action |
|---|---|---|
| E-stop | hardwired chain | remove controlled power |
| Door/interlock open | safety input | inhibit/stop |
| K_MAIN welded | auxiliary feedback / voltage verification | inhibit |
| K_LOAD welded | feedback / voltage verification | inhibit |
| Load overtemperature | independent thermal sensor/chain | disable load |
| Fan failure | tach/status | reduce/disable load |
| Measurement failure | self-test/range/heartbeat | inhibit affected test |
| ADC communication loss | watchdog/heartbeat | safe state |
| CAN failure | timeout | safe state where required |
| 24 V branch fault | branch protection/status | isolate affected branch |
| Unexpected current | measurement | controlled shutdown |
| Phase loss | voltage measurement | abort affected test |
| PE fault | dedicated safety/installation mechanism | inhibit |
| Software crash | hardware watchdog | safety state |

---

## 26. Mini / PRO / Factory implementation

### Mini
Priorities: service, installation validation, lower continuous load duty, essential measurement, CP/PP and reports.

### PRO
Adds full three-phase measurement, programmable load, advanced fault simulation, extended diagnostics, long-duration tests and service interfaces.

### Factory
Adds automated sequence, barcode/serial integration, end-of-line reports, traceability, recipe-based tests, production database and operator interlocks.

The same logical safety architecture should be retained across the family.

---

## 27. Charger/TestStation co-design requirements

The charger hardware project shall expose controlled diagnostic interfaces without compromising product safety/certification.

Joint design should define:
- CP/PP access;
- service connector;
- contactor state;
- controller heartbeat;
- fault state;
- hardware/firmware identification;
- selected measurement test points;
- safe current/voltage diagnostic points;
- CAN/service interface where used.

These interfaces must be documented in the charger hardware architecture.

---

## 28. Required engineering calculations before M1.8 freeze

### A. Supply
- nominal voltage;
- frequency;
- maximum design current;
- voltage tolerance;
- supply capacity.

### B. Short circuit
- prospective short-circuit current;
- minimum/maximum fault current as applicable;
- protective-device interrupt rating.

### C. Protection
- overcurrent device;
- residual-current/earth-fault strategy;
- surge protection;
- selectivity;
- coordination.

### D. Conductors
- cross-section;
- current-carrying capacity;
- derating;
- voltage drop;
- short-circuit thermal withstand.

### E. Contactors
- utilization category;
- continuous current;
- switching duty;
- endurance;
- auxiliary feedback.

### F. Load
- resistor/stage values;
- power per stage;
- thermal dissipation;
- airflow;
- duty cycle.

### G. 24 VDC
- total current;
- branch currents;
- PSU margin;
- branch protection.

### H. Mechanical
- enclosure temperature;
- cable bending;
- terminal accessibility;
- airflow;
- service access.

---

## 29. M1.7 approval gates

- [x] power topology defined
- [x] Zone A defined
- [x] Zone B defined
- [x] contactor functions defined
- [x] load architecture defined
- [x] 24 VDC architecture defined
- [x] PE architecture defined
- [x] E-stop relationship defined
- [x] protection methodology defined
- [x] short-circuit hold point defined
- [x] conductor-sizing hold point defined
- [x] thermal hold point defined
- [x] phase diagnostic path retained
- [x] charger/TestStation interface retained
- [ ] final protective devices approved
- [ ] final conductor sizes approved
- [ ] final contactors approved
- [ ] final load elements approved
- [ ] thermal design validated
- [ ] short-circuit/coordination calculations completed

---

## 30. Next milestone — M1.8

M1.8 shall convert this architecture into concrete engineering artefacts:

1. single-line electrical diagram;
2. detailed power schematic;
3. safety/E-stop schematic;
4. 24 VDC distribution schematic;
5. Zone A/Zone B measurement schematic;
6. contactor coil/feedback schematic;
7. load switching schematic;
8. preliminary terminal plan;
9. protection/coordination worksheet;
10. conductor-sizing worksheet;
11. power and thermal budget;
12. BOM update with approved/candidate status.

M1.8 must preserve the distinction between engineering candidate values and verified production values.

---

## Engineering note

This document is intentionally conservative at the mains-power boundary. The TestStation is a laboratory/industrial electrical system and must receive formal electrical design review, appropriate calculations, verification and applicable conformity/certification assessment before connection to live installations or release as a commercial product.
