<!-- Exact path: docs/02-architecture/TS-V1-M2.6-PROTOTYPE-HARDWARE-FREEZE-COMPLETE-BOM-ASSEMBLY.md -->

# VAZAO EVSE TestStation V1 — M2.6
## Prototype Hardware Freeze — CP/PP, Protection, Connectors, PCB, Harness, Thermal, BOM and Assembly

**Status:** Engineering prototype baseline  
**Milestone:** M2.6  
**Branch:** `feat/charger-hardware-v1`  
**Scope:** 230/400 VAC, 3-phase, 32 A/phase, up to 22 kW AC, IEC 61851 / Type 2  
**Important:** This document freezes a buildable prototype baseline, not a production/certification release. All mains work remains subject to competent electrical engineering review, installation-specific calculations, laboratory verification and applicable standards.

---

## 1. Objective

M2.6 converts the M2.5 architecture into a concrete prototype implementation package:

1. exact CP component baseline;
2. exact PP resistor-bank baseline;
3. exact MOSFET/coil suppression baseline;
4. concrete input protection candidate;
5. concrete EV connector;
6. complete resistor/capacitor BOM for the identified circuits;
7. PCB dimensions and stack-up;
8. first placement coordinates;
9. trace/current calculations;
10. thermal calculations;
11. creepage/clearance engineering worksheet;
12. harness connector MPNs;
13. production-style quantity BOM;
14. mechanical/assembly sequence;
15. prototype inspection checklist.

The package deliberately separates **FROZEN FOR PROTOTYPE**, **CANDIDATE**, and **HOLD** items.

---

# 2. Design baseline

| Parameter | Prototype value |
|---|---:|
| AC input | 3P + N + PE |
| Nominal voltage | 230/400 VAC |
| Frequency | 50 Hz |
| Maximum test current | 32 A/phase |
| Maximum apparent power target | 22 kVA class |
| EV interface | IEC 62196-2 Type 2 |
| Charging control | IEC 61851-1 Mode 3 |
| CP PWM | 1 kHz nominal |
| Measurement | 3× Zone A voltage + 3× Zone B voltage + 3× Zone A current + 3× Zone B current |
| ADC | ADS131M06IPBSR |
| Voltage isolation | AMC1311BDWVR |
| Current sensor | TMCS1123A3AQDVGR |
| Measurement MCU | STM32G474RET6 |
| Safety MCU | STM32G031K8T6 |
| CAN isolation | ISO1044BDWR |
| Main contactor | LC1D32BD |
| Measurement isolated DC/DC | MEE1S2405SC |
| 24 V PSU | QUINT4-PS/3AC/24DC/10, 2904621 |
| EV socket | Phoenix Contact EV-T2M3SE12-3AC32A-2,0M6,0E15, 1052448 |

The selected Type 2 infrastructure socket is rated 32 A AC, 480 V, has L1/L2/L3/N/PE plus CP/PP and is specified by Phoenix Contact for Mode 3 / Case B. It is therefore suitable as the concrete prototype interface, subject to mechanical and sourcing verification. 

---

# 3. Critical correction from M2.5 — isolated DC/DC

The previous project notes used the designation `MEJ1S2405SC`. The current Murata source identifies the 24 V → 5 V, 1 W, 200 mA SIP device as **MEE1S2405SC**.

**M2.6 rule:** use `MEE1S2405SC` on the prototype BOM unless procurement confirms an equivalent/current manufacturer designation.

Murata data currently found:

- input: 21.6–26.4 V;
- nominal input: 24 V;
- output: 5 V;
- maximum output: 1 W;
- maximum output current: 0.2 A;
- isolation: 1000 V;
- efficiency: 83%;
- temperature: −40 to +85 °C.

This is enough for the AMC1311B isolated-side prototype supply budget, but the final safety/isolation architecture must verify the required working voltage, surge category, creepage, clearance and isolation capacitance rather than relying only on the headline isolation voltage.

---

# 4. CP — Control Pilot prototype circuit

## 4.1 Architecture

The TestStation CP simulator is a bidirectional test interface:

```
TS-EV
  |
  +-- CP_DRV_PWM ----> isolated/protected CP output stage
  |
  +-- CP_SENSE ------> protected ADC/comparator input
  |
  +-- R_STATE_B -----> 2.74 kΩ selectable load
  |
  +-- R_STATE_C -----> 882 Ω selectable load
  |
  +-- R_STATE_D -----> 246 Ω selectable load
  |
  +-- D_CP ----------> polarity/half-wave handling
  |
  +-- FAULT_CP ------> controlled E/F fault simulation
```

TI's EVSE reference design documents the standard state-resistance values of 2.74 kΩ for State B, 882 Ω for State C and 246 Ω for State D, with a 1 kHz pilot. The same TI reference design shows a 2.74 kΩ EV-connected load and a 1.3 kΩ additional load for the charging state in its specific simulation implementation. 

## 4.2 CP resistor BOM

Prototype values:

| Ref | Value | Tolerance | Power target | Qty | Status |
|---|---:|---:|---:|---:|---|
| RCP01 | 2.74 kΩ | 1% | 0.25 W | 2 | FROZEN |
| RCP02 | 882 Ω | 1% | 0.25 W | 2 | FROZEN |
| RCP03 | 246 Ω | 1% | 0.5 W | 2 | FROZEN |
| RCP04 | 1.30 kΩ | 1% | 0.5 W | 2 | FROZEN |
| RCP05 | 10.0 kΩ | 1% | 0.125 W | 4 | FROZEN |
| RCP06 | 100 Ω | 1% | 0.25 W | 4 | FROZEN |
| RCP07 | 1.00 kΩ | 1% | 0.25 W | 4 | FROZEN |

Use metal-film, pulse-capable resistors with voltage rating appropriate to the CP circuit.

### CP state switching

Each state resistor is switched by a logic-level N-channel MOSFET or small signal analog switch. The switching device must be rated for the actual CP voltage, transients and fault-injection duty.

**Prototype implementation preference:** use discrete MOSFETs so the firmware can independently command and diagnose every state.

---

# 5. PP — Proximity Pilot simulator

## 5.1 Type 2 baseline

The Type 2 connector/cable uses PP coding. Phoenix Contact Type 2 cable documentation identifies 220 Ω as a coding value on its 32 A cable example.

The TestStation therefore uses a selectable PP coding bank rather than hard-coding a single resistance.

## 5.2 PP resistor bank

Prototype selectable values:

| Ref | Resistance | Intended simulated class | Qty |
|---|---:|---|---:|
| RPP01 | 220 Ω | high-current cable coding | 2 |
| RPP02 | 680 Ω | 32 A-class coding | 2 |
| RPP03 | 1.50 kΩ | lower-current cable coding | 2 |
| RPP04 | 2.70 kΩ | diagnostic/non-standard test state | 2 |
| RPP05 | 10.0 kΩ | open/high-R diagnostic state | 2 |

**Important:** the resistor bank is a simulation tool. The final mapping from resistance to cable-current category must be implemented from the exact applicable IEC 61851 / IEC 62196 coding table used by the charger product release. Do not infer a production current limit from a generic resistance value.

## 5.3 PP fault simulation

Supported prototype states:

- normal selected resistance;
- open circuit;
- short circuit;
- intermittent open;
- intermittent contact;
- out-of-range resistance;
- simulated connector-present / connector-removed.

---

# 6. CP/PP switching MOSFET

## 6.1 Prototype device

Candidate/FROZEN-FOR-PROTOTYPE:

**TI CSD18540Q5B**

Relevant published characteristics include:

- N-channel;
- 60 V VDS;
- logic-level gate capability;
- low RDS(on);
- catalog temperature range −55 to +175 °C.

The device is substantially over-rated for the low-current CP/PP switching function, which is intentional for prototype robustness.

## 6.2 Gate network

Per switched branch:

| Ref | Value |
|---|---:|
| R_GATE | 100 Ω |
| R_GS | 100 kΩ |
| C_GATE | DNP initially |
| D_GATE | DNP initially |

The gate driver must be referenced to the correct SELV/CP domain. No MCU pin may be directly exposed to the external CP connector.

---

# 7. Main contactor driver

## 7.1 Contactor

**Schneider Electric LC1D32BD**

Published manufacturer data identifies it as:

- 3P / 3 NO;
- AC-3;
- up to 440 V;
- 32 A;
- 24 V DC coil.

This is the prototype main contactor baseline. 

## 7.2 Coil driver

Prototype topology:

```
+24V
 |
 |---- LC1D32BD coil ----+---- drain QK_MAIN
                         |
                         +---- D_FLYBACK
                              |
                             0V
QK_MAIN source ------------ 0V
QK_MAIN gate <--- 100R --- SAFE_MCU
QK_MAIN gate --- 100k --- 0V
```

Prototype MOSFET:

**CSD18540Q5B**

Flyback diode:

**1N4007** class, 1 A rectifier diode, prototype baseline.

**Production HOLD:** replace/validate the flyback network after measuring actual LC1D32BD coil release time and the safety-required de-energisation time. A simple diode maximizes coil suppression but may slow release; a TVS/R-C clamp can provide faster release and must be evaluated against coil transient limits.

---

# 8. Input protection

## 8.1 Prototype candidate

**Schneider Electric Acti9 iC60N A9F74440**

Published data:

- 4 poles;
- 40 A;
- curve C;
- 6 kA under IEC 60898-1 listing;
- 10 kA under IEC 60947-2 listing on the Portuguese product page.

This is a **prototype candidate only**, not a universal final protection value.

## 8.2 Why 40 A is not automatically approved

The protection device must be checked against:

- available prospective short-circuit current;
- supply impedance;
- conductor cross-section and length;
- installation method;
- ambient temperature;
- grouping;
- selectivity;
- upstream protection;
- Type 2 EVSE protection requirements;
- RCD/DC residual-current strategy;
- enclosure thermal conditions;
- interrupting rating;
- local installation rules.

If any of those checks fail, the MCB is replaced before energisation.

---

# 9. Surge and residual-current protection

The prototype shall provide positions for:

- SPD;
- residual-current protection;
- DC residual-current detection;
- upstream PE/bonding verification.

These are **not frozen to a generic MPN in M2.6** because the correct device depends on the final TestStation supply arrangement and the exact EVSE safety test objective.

No prototype mains energisation is permitted with these positions bypassed.

---

# 10. Type 2 EV connector

Selected prototype connector:

**Phoenix Contact EV-T2M3SE12-3AC32A-2,0M6,0E15 — 1052448**

Manufacturer data:

- Type 2;
- Mode 3, Case B;
- 32 A AC, 3-phase;
- 22 kW rating at 32 A / 3-phase;
- 480 V rated;
- five power contacts L1/L2/L3/N/PE;
- two signal contacts CP/PP.

The connector includes a locking actuator, so the mechanical implementation must include its required drive/sense wiring.

---

# 11. PCB partition

Four PCBs remain the M2.5 architecture.

## PCB-A — TS-MEASURE

Purpose:
- ADS131M06;
- six AMC1311B channels;
- six MEE1S2405SC isolated supplies;
- six 3.3 V isolated-side regulators;
- TMCS1123A3AQDVGR interfaces;
- calibration/reference;
- measurement MCU.

Suggested prototype size:

**160 mm × 100 mm, 4-layer**

## PCB-B — TS-SAFE

Purpose:
- safety MCU;
- E-stop monitoring;
- interlock;
- contactor drivers;
- contactor feedback;
- watchdog;
- power fault inputs.

Suggested prototype size:

**120 mm × 80 mm, 4-layer**

## PCB-C — TS-EV

Purpose:
- CP generation/sense;
- CP state simulation;
- PP resistor bank;
- Type 2 interface;
- locking actuator interface;
- fault injection.

Suggested prototype size:

**120 mm × 80 mm, 4-layer**

## PCB-D — TS-POWER/LOAD

Purpose:
- mains distribution;
- protection;
- contactors;
- load switching;
- staged load interfaces.

Preferred implementation:

**DIN-rail / point-to-point industrial assembly**, not a conventional FR-4 PCB for the 32 A mains path.

---

# 12. PCB stack-up

## 4-layer signal PCBs

Prototype stack:

| Layer | Function |
|---|---|
| L1 | components + critical signals |
| L2 | solid reference / controlled ground where permitted |
| L3 | power + secondary routing |
| L4 | signals + low-current power |

Nominal board thickness:

**1.6 mm**

Copper:

**35 µm / 1 oz outer + 35 µm / 1 oz inner**

Do not route hazardous mains conductors through PCB-A/B/C unless the specific PCB is redesigned and re-qualified for the applicable isolation system.

---

# 13. PCB placement coordinates — first placement

Coordinates use lower-left PCB origin.

## PCB-A

| Ref group | X mm | Y mm | Zone |
|---|---:|---:|---|
| J-A1 Zone A HV sense | 8 | 20 | isolation edge |
| AMC1311 A1 | 30 | 20 | ISO-A1 |
| MEE1S2405SC A1 | 52 | 20 | ISO-A1 |
| AMC1311 A2 | 30 | 42 | ISO-A2 |
| MEE1S2405SC A2 | 52 | 42 | ISO-A2 |
| AMC1311 A3 | 30 | 64 | ISO-A3 |
| MEE1S2405SC A3 | 52 | 64 | ISO-A3 |
| AMC1311 B1 | 82 | 20 | ISO-B1 |
| MEE1S2405SC B1 | 104 | 20 | ISO-B1 |
| AMC1311 B2 | 82 | 42 | ISO-B2 |
| MEE1S2405SC B2 | 104 | 42 | ISO-B2 |
| AMC1311 B3 | 82 | 64 | ISO-B3 |
| MEE1S2405SC B3 | 104 | 64 | ISO-B3 |
| ADS131M06 | 72 | 45 | MEAS-3V3 |
| STM32G474RET6 | 92 | 75 | MCU |
| CAN/USB service | 130 | 75 | SELV |

These are **initial placement coordinates**, not manufacturing coordinates. Final placement must follow actual package land patterns, creepage keepouts, routing, thermal and EMC review.

---

# 14. PCB trace-width baseline

For 1 oz copper and short prototype traces, use conservative initial values:

| Circuit | Initial width |
|---|---:|
| MCU GPIO | 0.20 mm |
| SPI | 0.20 mm |
| CAN | 0.25 mm |
| 3.3 V measurement rail | 0.50 mm |
| 5 V isolated rail | 0.75 mm |
| 24 V control rail | 1.00 mm |
| contactor coil PCB feed | 1.50 mm |
| measurement current-sensor supply | 0.75 mm |

These are layout starting points only. Final width must be verified using actual copper thickness, permissible temperature rise, length and connector current rating.

The 32 A mains path remains off-PCB using appropriately sized conductors and DIN/industrial terminals.

---

# 15. Current-sensor interface

Selected baseline:

**TI TMCS1123A3AQDVGR**

The TMCS1123 family is an active ±1300 V reinforced-isolation Hall current sensor family with 80 ARMS capability, 250 kHz bandwidth, 8.1 mm minimum creepage/clearance and multiple sensitivity options. 

Prototype configuration:

- three sensors Zone A;
- three sensors Zone B;
- 75 mV/A sensitivity variant;
- one sensor per phase;
- short high-current copper path;
- Kelvin/low-noise output routing;
- local decoupling;
- overcurrent alert wired to safety/measurement MCU.

At 32 A:

[
V_{OUT,signal}=32A	imes75mV/A=2.40V
]

The actual TMCS1123 output transfer function, reference, offset and ADC scaling must be implemented from the exact device revision/datasheet before firmware calibration.

---

# 16. Voltage-sensor channel

Each AMC1311B channel receives an independent floating divider.

Prototype nominal divider:

- Rtop = 4 × 470 kΩ in series;
- Rbottom = 10 kΩ;
- all resistors 1% minimum;
- resistor pulse/working-voltage rating individually verified.

At 230 Vrms:

[
V_{PK}=230sqrt2=325.3V
]

Divider ratio:

[
10k/(4	imes470k+10k)=0.005319
]

Therefore:

[
V_{LOW,PK}approx1.73V
]

At 253 Vrms:

[
V_{LOW,PK}approx1.90V
]

This remains below the AMC1311B 2 V input upper boundary with little tolerance/surge margin. Therefore the M2.6 design **must not assume the nominal calculation is sufficient**.

Final release gate:

- resistor tolerance;
- resistor voltage coefficient;
- resistor working voltage;
- surge;
- AMC1311 input absolute maximum;
- 253 Vrms operating case;
- transient test;
- calibration offset/gain;
- PCB creepage/clearance.

---

# 17. AMC1311B supply

Each AMC1311B gets an independent isolated 5 V domain:

```
24V
 |
 MEE1S2405SC
 |
 +5V_ISO-x
 |
 TLV70033DCKR
 |
 +3V3_ISO-x
 |
 AMC1311B
```

Six channels = six independent isolated converters.

**Never combine the isolated output returns of separate floating measurement channels unless the isolation architecture is explicitly redesigned and re-qualified.**

---

# 18. Decoupling BOM

Per AMC1311B:

| Ref | Value | Package | Qty/channel |
|---|---:|---|---:|
| C_ISO_01 | 100 nF | X7R | 1 |
| C_ISO_02 | 1 µF | X7R | 1 |
| C_ISO_03 | 4.7 µF | X7R | 1 |

Per ADS131M06:

| Ref | Value | Package |
|---|---:|---|
| C_ADC01 | 100 nF | X7R |
| C_ADC02 | 1 µF | X7R |
| C_ADC03 | 4.7 µF | X7R |

Per MCU:

| Ref | Value | Package |
|---|---:|---|
| C_MCU01..08 | 100 nF | X7R |
| C_MCU09 | 4.7 µF | X7R |

Per 24 V branch:

| Ref | Value | Type |
|---|---:|---|
| C24_01 | 100 nF | ceramic |
| C24_02 | 10 µF | electrolytic |
| C24_03 | 47 µF | electrolytic |

Exact voltage ratings:

- 3.3 V rails: ≥10 V;
- 5 V rails: ≥10 V;
- 24 V rail: ≥35 V;
- CP: ≥25 V;
- mains sensing capacitor positions: ≥630 V if populated, subject to the actual circuit.

---

# 19. Resistor BOM — production-style quantities

| Function | Value | Tol. | Qty |
|---|---:|---:|---:|
| Voltage divider high | 470 kΩ | 1% | 24 |
| Voltage divider low | 10 kΩ | 1% | 6 |
| CP State B | 2.74 kΩ | 1% | 2 |
| CP State C | 882 Ω | 1% | 2 |
| CP State D | 246 Ω | 1% | 2 |
| CP charging branch | 1.30 kΩ | 1% | 2 |
| CP gate | 100 Ω | 1% | 12 |
| CP gate pull-down | 100 kΩ | 1% | 12 |
| PP | 220 Ω | 1% | 2 |
| PP | 680 Ω | 1% | 2 |
| PP | 1.50 kΩ | 1% | 2 |
| PP | 2.70 kΩ | 1% | 2 |
| PP | 10 kΩ | 1% | 2 |
| feedback pull-up | 10 kΩ | 1% | 12 |
| LED/diagnostic | 1 kΩ | 1% | 20 |
| CAN termination | 120 Ω | 1% | 4 |
| service/config | 10 kΩ | 1% | 12 |

Procurement quantity shall include 10–20% spare for prototype rework.

---

# 20. Harness connectors

Low-voltage removable harness baseline:

**Phoenix Contact MSTB 2,5/5-ST-5,08 — 1757048**

Published data:

- 5 positions;
- 5.08 mm pitch;
- 2.5 mm² nominal conductor;
- 12 A nominal;
- 320 V nominal;
- screw connection.

Use for:

- TS-SAFE I/O;
- CP/PP low-current harness;
- service/control signals.

For higher-density low-current signals, use the Phoenix Contact MCV/MC family only after the exact voltage/current/isolation requirement is checked.

High-voltage 32 A paths shall not use these PCB connectors.

DIN-rail power terminal baseline:

**Phoenix Contact PT 6 — 3211813**

Published data:

- 6 mm²;
- 41 A nominal;
- 1000 V nominal;
- Push-in;
- DIN rail.

This is appropriate as a prototype terminal baseline for the 32 A-class power distribution, subject to conductor, ferrule, enclosure and thermal verification.

---

# 21. Mechanical assembly zones

Prototype trolley:

- target: 720 H × 480 W × 300 D mm;
- 25–35 kg target;
- lower zone: mains/load;
- middle zone: contactors/protection;
- upper zone: PCBs and HMI;
- front: Type 2 interface;
- rear: AC input and service;
- separate measurement harness routing.

Minimum physical segregation:

1. HV power compartment;
2. HV load compartment;
3. isolated measurement compartment;
4. SELV electronics compartment;
5. external EV connector compartment.

Do not route CP/PP and measurement harnesses parallel to high-current load conductors for long distances.

---

# 22. Creepage / clearance worksheet

This worksheet is an engineering starting point, not a certification claim.

## Required checks

| Interface | Working voltage | Pollution/installation | Initial target | Status |
|---|---:|---|---:|---|
| HV to PE | 400 VAC | enclosure-dependent | ≥8 mm preferred prototype target | HOLD |
| HV to SELV | 400 VAC | enclosure-dependent | ≥8 mm preferred prototype target | HOLD |
| AMC1311 HV-side to LV-side | device-defined | datasheet | use manufacturer minimum + margin | HOLD |
| TMCS1123 isolation | device-defined | device-defined | ≥8.1 mm baseline | CHECK |
| CP to SELV | ≤12 V nominal | controlled | ≥3 mm | CHECK |
| PP to SELV | ≤30 V | controlled | ≥3 mm | CHECK |
| CAN isolated barrier | device-defined | device-defined | ≥8 mm target | CHECK |

The final creepage/clearance values must be calculated from the applicable standard, pollution degree, material group, altitude, overvoltage category and working voltage.

---

# 23. Thermal calculations

## 23.1 22 kW load

If the electronic load is implemented as resistive:

[
P_{heat}approx22,000W
]

Therefore the load compartment must be treated as a **22 kW heater** during full-power tests.

This cannot be solved with a normal small fan.

## 23.2 Contactor

Contactor coil losses are measured during bring-up.

For every contactor:

[
P_{coil}=V_{coil}	imes I_{coil}
]

Record:

- cold coil current;
- stabilized current;
- coil temperature;
- release time;
- enclosure temperature.

## 23.3 PCB

For semiconductor loss:

[
P=I^2R_{DS(on)}
]

For linear regulator:

[
P=(V_{IN}-V_{OUT})I
]

No regulator may be thermally approved from nominal calculations alone; prototype temperature logging is mandatory.

---

# 24. Power distribution

The selected 24 V PSU baseline is:

**Phoenix Contact QUINT4-PS/3AC/24DC/10 — 2904621**

Published data identifies 24 V DC / 10 A / 240 W nominal class.

24 V branches:

- B1 measurement isolated DC/DC ×6;
- B2 safety MCU;
- B3 contactors;
- B4 CP/PP;
- B5 fans;
- B6 service/HMI;
- B7 spare.

Each branch gets:

- branch protection;
- test point;
- current measurement or calculated budget;
- labelled return.

---

# 25. Production-style BOM

| Item | MPN / value | Qty | Status |
|---|---|---:|---|
| ADC | ADS131M06IPBSR | 2 | FROZEN prototype |
| Voltage isolation | AMC1311BDWVR | 6 | FROZEN prototype |
| Current sensor | TMCS1123A3AQDVGR | 6 | FROZEN prototype |
| Measurement MCU | STM32G474RET6 | 1 | FROZEN prototype |
| Safety MCU | STM32G031K8T6 | 1 | FROZEN prototype |
| CAN isolation | ISO1044BDWR | 2 | FROZEN prototype |
| Isolated DC/DC | MEE1S2405SC | 6 | FROZEN prototype / datasheet verification |
| 3.3 V LDO | TLV70033DCKR | 6+ | FROZEN prototype |
| Main contactor | LC1D32BD | 2 | FROZEN prototype |
| Main MOSFET | CSD18540Q5B | 4 | prototype |
| Flyback diode | 1N4007 class | 4 | prototype |
| PSU | 2904621 | 1 | FROZEN prototype |
| MCB | A9F74440 | 1 | CANDIDATE / installation check |
| Type 2 socket | 1052448 | 1 | FROZEN prototype |
| PCB connector | 1757048 | 12 | FROZEN prototype |
| DIN terminal | 3211813 | 12 | FROZEN prototype |
| HV divider 470 kΩ | 1% | 24 | FROZEN value |
| HV divider 10 kΩ | 1% | 6 | FROZEN value |
| CP 2.74 kΩ | 1% | 2 | FROZEN value |
| CP 882 Ω | 1% | 2 | FROZEN value |
| CP 246 Ω | 1% | 2 | FROZEN value |
| CP 1.30 kΩ | 1% | 2 | FROZEN value |
| PP 220 Ω | 1% | 2 | FROZEN value |
| PP 680 Ω | 1% | 2 | FROZEN value |
| PP 1.50 kΩ | 1% | 2 | FROZEN value |
| PP 2.70 kΩ | 1% | 2 | FROZEN value |
| PP 10 kΩ | 1% | 2 | FROZEN value |
| CAN termination | 120 Ω | 4 | FROZEN value |
| E-stop | industrial, 2NC minimum | 1 | HOLD exact MPN |
| SPD | Type 2 appropriate to final system | 1 | HOLD |
| RCD/DC detection | EVSE-appropriate | 1 | HOLD |
| Load stages | 22 kW total | 1 set | HOLD final architecture |
| Fans | industrial 24 V | 2+ | HOLD exact MPN |
| Enclosure | metal/IP-rated | 1 | HOLD exact MPN |

---

# 26. Assembly sequence

1. Mount enclosure and DIN rail.
2. Install PE bar first.
3. Install input terminals.
4. Install MCB/protection hardware.
5. Install main contactors.
6. Install 24 V PSU.
7. Install load switching hardware.
8. Install PCB-A/B/C.
9. Install Type 2 socket.
10. Install low-voltage harnesses.
11. Install measurement harness.
12. Install CP/PP harness.
13. Install safety/E-stop harness.
14. Verify PE continuity.
15. Verify insulation/isolation before applying mains.
16. Power only the 24 V SELV domain.
17. Commission safety logic.
18. Commission measurement electronics.
19. Commission CP/PP.
20. Perform no-load mains test.
21. Perform controlled low-current load test.
22. Increase load in staged increments.
23. Validate emergency shutdown.
24. Validate contactor feedback.
25. Validate Zone A/B measurement.
26. Perform phase-angle calibration.
27. Perform long-duration thermal test.

---

# 27. Prototype inspection checklist

## Mechanical
- [ ] enclosure dimensions verified
- [ ] PCB standoffs secure
- [ ] Type 2 socket mechanically locked
- [ ] cable strain relief installed
- [ ] HV/SELV compartments separated
- [ ] fans have unobstructed airflow

## Electrical
- [ ] PE continuity verified
- [ ] no SELV-to-HV unintended connection
- [ ] polarity verified
- [ ] contactor terminal torque verified
- [ ] conductor cross-section verified
- [ ] protection devices installed
- [ ] E-stop opens safety chain
- [ ] contactor feedback detects welded/stuck state

## Measurement
- [ ] six voltage channels
- [ ] six current channels
- [ ] six isolation barriers
- [ ] six isolated supplies
- [ ] ADC synchronization
- [ ] calibration coefficients loaded
- [ ] independent reference instrument available
- [ ] phase error recorded

## EV interface
- [ ] CP State A
- [ ] CP State B
- [ ] CP State C
- [ ] CP State D
- [ ] CP 1 kHz PWM
- [ ] CP fault E
- [ ] PP open
- [ ] PP 220 Ω
- [ ] PP 680 Ω
- [ ] PP 1.5 kΩ
- [ ] PP fault/short
- [ ] Type 2 lock feedback

## Thermal
- [ ] contactor coil temperature
- [ ] PSU temperature
- [ ] PCB temperature
- [ ] load temperature
- [ ] enclosure temperature
- [ ] fan failure test
- [ ] over-temperature shutdown

---

# 28. M2.6 release gates

M2.6 is considered technically complete when:

- exact prototype MPN baseline exists;
- CP state simulator is fully defined;
- PP simulator is fully defined;
- main contactor driver is defined;
- input protection candidate exists;
- connector/harness baseline exists;
- PCB dimensions and stack-up exist;
- initial placement exists;
- trace rules exist;
- thermal calculations exist;
- creepage/clearance worksheet exists;
- production-style BOM exists;
- assembly sequence exists;
- inspection checklist exists.

M2.6 does **not** authorize mains energisation.

---

# 29. M2.7 next milestone

M2.7 shall produce:

1. complete KiCad project file tree;
2. 15 schematic sheets converted from engineering worksheets into actual CAD sheets;
3. footprints and symbols;
4. PCB-A placement and routing;
5. PCB-B placement and routing;
6. PCB-C placement and routing;
7. DIN-rail power assembly drawing;
8. harness drawings;
9. complete netlist;
10. ERC/DRC rules;
11. manufacturing BOM;
12. pick-and-place data where applicable;
13. prototype assembly drawing;
14. bring-up firmware pin map;
15. first electrical test procedure.

**M2.7 remains blocked from production release until the safety/protection and isolation review is passed.**

---

## 30. Engineering source verification

The concrete component choices in this milestone were cross-checked against current manufacturer information:

- TI TIDA-010939 confirms IEC 61851 Control Pilot support in an EVSE reference design. 
- TI's EVSE reference documentation provides the CP state resistor values used as the prototype simulation baseline. 
- Schneider Electric identifies LC1D32BD as a 32 A, 3-pole, 24 VDC-coil contactor. 
- TI identifies TMCS1123 as an 80 ARMS, 250 kHz, reinforced-isolation Hall current sensor family with 8.1 mm minimum creepage/clearance. 
- Phoenix Contact identifies the selected Type 2 socket as a 32 A, 3-phase, 22 kW-class Mode 3 interface with CP/PP. 
- Phoenix Contact identifies PT 6 3211813 as a 6 mm² / 41 A / 1000 V DIN terminal. 
- Phoenix Contact identifies MSTB 2,5/5-ST-5,08 1757048 as a 5-position, 2.5 mm², 12 A PCB connector. 
- Murata identifies MEE1S2405SC as a 24 V → 5 V, 1 W, 200 mA isolated converter. 

All web-verified values above remain subject to final datasheet revision and procurement verification before hardware build.
