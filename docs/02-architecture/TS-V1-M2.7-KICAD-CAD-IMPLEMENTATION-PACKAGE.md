<!-- Exact path: docs/02-architecture/TS-V1-M2.7-KICAD-CAD-IMPLEMENTATION-PACKAGE.md -->

# VAZAO EVSE TestStation V1 — M2.7
## KiCad CAD Implementation Package

**Status:** CAD implementation baseline  
**Branch:** `feat/charger-hardware-v1`  
**Scope:** convert M2.5/M2.6 engineering definitions into a controlled KiCad project structure.

> This milestone defines the CAD implementation contract and release structure. It does not claim that a PCB has passed ERC/DRC, electrical safety review, manufacturing review, or mains validation.

---

## 1. M2.7 objective

M2.7 establishes the exact CAD project structure that the TestStation PCB work must follow.

The design is split into:

- PCB-A — TS-MEASURE
- PCB-B — TS-SAFE
- PCB-C — TS-EV
- PCB-D — TS-POWER/LOAD

PCB-D remains an industrial DIN-rail / point-to-point assembly because the 32 A mains/load path should not be forced onto a conventional low-voltage PCB.

KiCad supports physical stackup definition, net classes, custom design rules and DRC constraints; these are therefore treated as controlled project data rather than informal notes. citeturn0search2turn0search48

---

# 2. Repository CAD tree

The target CAD tree is:

```
hardware/
└── teststation/
    └── V1/
        └── CAD/
            ├── README.md
            ├── project/
            │   ├── TS-V1.kicad_pro
            │   ├── TS-V1.kicad_sch
            │   ├── TS-V1.kicad_prl
            │   └── TS-V1.kicad_dru
            ├── symbols/
            │   └── VAZAO_TS.kicad_sym
            ├── footprints/
            │   └── VAZAO_TS.pretty/
            ├── 3d/
            ├── sheets/
            │   ├── 00-COVER-INDEX.kicad_sch
            │   ├── 01-POWER-INPUT.kicad_sch
            │   ├── 02-POWER-PROTECTION.kicad_sch
            │   ├── 03-ZONE-A.kicad_sch
            │   ├── 04-ZONE-B.kicad_sch
            │   ├── 05-CURRENT-SENSORS.kicad_sch
            │   ├── 06-VOLTAGE-SENSORS.kicad_sch
            │   ├── 07-ADC-MEASUREMENT-MCU.kicad_sch
            │   ├── 08-TS-SAFE.kicad_sch
            │   ├── 09-TS-CONTACTORS.kicad_sch
            │   ├── 10-TS-EV-CP.kicad_sch
            │   ├── 11-TS-EV-PP.kicad_sch
            │   ├── 12-TS-COMMS-CAN.kicad_sch
            │   ├── 13-24VDC.kicad_sch
            │   ├── 14-THERMAL-FANS.kicad_sch
            │   └── 15-TEST-POINTS.kicad_sch
            ├── pcb/
            │   ├── TS-MEASURE.kicad_pcb
            │   ├── TS-SAFE.kicad_pcb
            │   └── TS-EV.kicad_pcb
            ├── power/
            │   ├── TS-POWER-WIRING.dxf
            │   ├── TS-POWER-WIRING.pdf
            │   └── TS-POWER-BOM.csv
            ├── harness/
            │   ├── H-HV.dxf
            │   ├── H-MEASURE.dxf
            │   ├── H-SAFE.dxf
            │   ├── H-EV.dxf
            │   ├── H-COMMS.dxf
            │   └── H-CTRL.dxf
            ├── manufacturing/
            │   ├── BOM.csv
            │   ├── PNP.csv
            │   ├── FAB-NOTES.md
            │   └── ASSEMBLY.md
            └── verification/
                ├── ERC-CHECKLIST.md
                ├── DRC-CHECKLIST.md
                ├── ISOLATION-CHECKLIST.md
                ├── MEASUREMENT-CHECKLIST.md
                └── BRINGUP-PROCEDURE.md
```

This tree is the source-of-truth structure for the CAD release.

---

# 3. Reference design hierarchy

The 15-sheet hierarchy from M2.5 is retained.

## Sheet 00 — COVER/INDEX

Contains:

- project name;
- hardware revision;
- CAD revision;
- board list;
- document status;
- safety warnings;
- sheet index;
- revision history.

## Sheet 01 — POWER-INPUT

Contains:

- L1/L2/L3/N/PE;
- input terminals;
- Q0/main isolation;
- supply monitoring;
- PE entry;
- voltage sensing branch feeds.

## Sheet 02 — POWER-PROTECTION

Contains:

- MCB candidate;
- SPD placeholder;
- residual-current protection placeholder;
- protection coordination notes;
- branch identification.

The MCB remains installation-dependent. No generic 40 A device is to be treated as an approved final protection selection.

## Sheet 03 — ZONE-A

Contains:

- VA_L1;
- VA_L2;
- VA_L3;
- IA_L1;
- IA_L2;
- IA_L3;
- contactor state;
- test points.

## Sheet 04 — ZONE-B

Same structure as Zone A.

Zone A is always interpreted as the **pre-EVSE / supply-side measurement boundary**.

Zone B is always interpreted as the **post-EVSE / EVSE-side measurement boundary**.

---

# 4. Measurement CAD

## 4.1 Voltage channels

Six independent channels:

```
A-L1 -> divider -> AMC1311B-A1 -> ISO-A1 -> ADC
A-L2 -> divider -> AMC1311B-A2 -> ISO-A2 -> ADC
A-L3 -> divider -> AMC1311B-A3 -> ISO-A3 -> ADC

B-L1 -> divider -> AMC1311B-B1 -> ISO-B1 -> ADC
B-L2 -> divider -> AMC1311B-B2 -> ISO-B2 -> ADC
B-L3 -> divider -> AMC1311B-B3 -> ISO-B3 -> ADC
```

Each isolated channel gets its own MEE1S2405SC converter.

Murata specifies MEE1S2405SC as a 24 V-input, 5 V-output, 1 W isolated converter with 200 mA maximum output and 1000 V isolation. citeturn0search50

## 4.2 Current channels

```
A-L1 -> TMCS1123A3AQDVGR -> ADC
A-L2 -> TMCS1123A3AQDVGR -> ADC
A-L3 -> TMCS1123A3AQDVGR -> ADC

B-L1 -> TMCS1123A3AQDVGR -> ADC
B-L2 -> TMCS1123A3AQDVGR -> ADC
B-L3 -> TMCS1123A3AQDVGR -> ADC
```

The six channels must use identical logical naming so firmware can process Zone A and Zone B through the same measurement pipeline.

---

# 5. ADC channel map

## ADC-01 — Zone A

| ADC channel | Signal |
|---|---|
| CH0 | VA_L1 |
| CH1 | VA_L2 |
| CH2 | VA_L3 |
| CH3 | IA_L1 |
| CH4 | IA_L2 |
| CH5 | IA_L3 |

## ADC-02 — Zone B

| ADC channel | Signal |
|---|---|
| CH0 | VB_L1 |
| CH1 | VB_L2 |
| CH2 | VB_L3 |
| CH3 | IB_L1 |
| CH4 | IB_L2 |
| CH5 | IB_L3 |

The ADS131M06 is a six-channel simultaneous-sampling ADC and supports channel-to-channel phase-delay calibration, making it appropriate for the phase-angle measurement architecture. citeturn0search0

---

# 6. CP CAD

The CP implementation follows the IEC 61851 architecture represented in TI's current EVSE reference design.

TI documents:

- 1 kHz pilot;
- State B = 2.74 kΩ;
- State C = 882 Ω;
- State D = 246 Ω;
- 1.3 kΩ branch in the typical CP circuit;
- ADC feedback for CP voltage.

citeturn0search49turn0search51

## Net names

```
CP_EXT
CP_DRV
CP_SENSE
CP_STATE_B
CP_STATE_C
CP_STATE_D
CP_FAULT_E
CP_FAULT_F
CP_GND
```

No CP external pin connects directly to an MCU GPIO.

---

# 7. PP CAD

Net names:

```
PP_EXT
PP_SELECT_220
PP_SELECT_680
PP_SELECT_1K5
PP_SELECT_2K7
PP_SELECT_10K
PP_OPEN
PP_SHORT
PP_SENSE
```

The PP resistor bank is explicitly a **simulation mechanism**. It must not be used to infer a production vehicle-cable rating without the exact applicable Type 2 coding table.

---

# 8. Safety CAD

Sheet 08 and 09 shall be treated as safety-critical.

## Inputs

```
E_STOP_NC_A
E_STOP_NC_B
DOOR_INTERLOCK
LOAD_OVERTEMP
K_MAIN_AUX
K_LOAD_AUX
POWER_FAULT
WATCHDOG_OK
```

## Outputs

```
K_MAIN_DRV
K_ZONE_A_DRV
K_ZONE_B_DRV
K_LOAD_DRV
FAN_ENABLE
SAFE_STATUS
FAULT_LATCH
```

Software shall never be the sole means of removing hazardous energy.

The E-stop chain must have a hardwired de-energisation path independent of normal application software.

---

# 9. Net classes

KiCad net classes shall be configured as follows.

| Net class | Default width | Default clearance | Use |
|---|---:|---:|---|
| SIGNAL | 0.20 mm | 0.20 mm | MCU/GPIO |
| SPI | 0.20 mm | 0.20 mm | ADC |
| CAN | 0.25 mm | 0.20 mm | CAN |
| LV-3V3 | 0.50 mm | 0.20 mm | 3.3 V |
| LV-5V | 0.75 mm | 0.25 mm | isolated 5 V |
| LV-24V | 1.00 mm | 0.30 mm | control |
| COIL-24V | 1.50 mm | 0.30 mm | contactor coil |
| CP | 0.50 mm | 0.50 mm | CP |
| PP | 0.50 mm | 0.50 mm | PP |
| HV-MEASURE | not routed on common PCB | ≥8 mm target prototype | hazardous sensing |
| HV-POWER | not routed on PCB-A/B/C | installation-specific | mains |

KiCad documentation confirms that net classes define clearance, track width, via sizes and related routing defaults, while minimum constraints and custom rules can override them. citeturn0search2

---

# 10. PCB-A placement

Board:

**160 × 100 mm**

Major placement:

| Area | Position |
|---|---|
| Zone A isolation | left 0–60 mm |
| Zone B isolation | right 70–130 mm |
| ADC | centre |
| measurement MCU | upper-right |
| service/CAN | upper edge |
| calibration connector | lower edge |

The six isolation barriers must not be allowed to merge their floating references through copper, mounting hardware or connector shields.

---

# 11. PCB-B placement

Board:

**120 × 80 mm**

Zones:

- safety MCU: centre;
- E-stop inputs: left;
- contactor outputs: right;
- feedback inputs: lower;
- CAN/service: upper.

The safety board must be physically separated from the measurement ADC analogue area.

---

# 12. PCB-C placement

Board:

**120 × 80 mm**

Zones:

- Type 2 connector interface: board edge;
- CP generation: centre-left;
- CP sensing: centre;
- PP resistor bank: centre-right;
- fault injection: lower;
- locking actuator: upper.

The external Type 2 connector wiring must be mechanically strain-relieved and isolated from the PCB control circuitry.

Phoenix Contact identifies connector 1052448 as Type 2, Mode 3 Case B, 32 A AC, 480 V, with CP and PP signal contacts and a 12 V locking actuator. citeturn0search1

---

# 13. PCB-D power assembly

PCB-D is intentionally **not** a conventional FR-4 PCB.

Architecture:

```
AC INPUT
  |
  +-- PE BAR
  |
  +-- Q0
  |
  +-- MCB / PROTECTION
  |
  +-- K_MAIN
  |
  +-- ZONE-A
  |
  +-- EVSE UNDER TEST
  |
  +-- ZONE-B
  |
  +-- K_LOAD
  |
  +-- STAGED LOAD
```

All 32 A-class paths use correctly rated industrial conductors, terminals, contactors and protection.

---

# 14. Harness naming

## H-HV

```
HV-01 L1
HV-02 L2
HV-03 L3
HV-04 N
HV-05 PE
```

## H-MEASURE

```
VA_L1
VA_L2
VA_L3
VB_L1
VB_L2
VB_L3
IA_L1
IA_L2
IA_L3
IB_L1
IB_L2
IB_L3
```

## H-SAFE

```
E_STOP
DOOR
OVERTEMP
K_MAIN_FB
K_LOAD_FB
SAFE_STATUS
```

## H-EV

```
CP
PP
LOCK+
LOCK-
PE
L1
L2
L3
N
```

## H-COMMS

```
CANH
CANL
CAN_GND
SERVICE_TX
SERVICE_RX
RESET
```

---

# 15. Footprint policy

Every production-intent component must have:

1. manufacturer MPN;
2. KiCad symbol;
3. verified land pattern;
4. datasheet package drawing;
5. 3D model where available;
6. courtyard;
7. fabrication dimensions;
8. pin-1 marker;
9. polarity marker;
10. mounting/mechanical restrictions.

No footprint is accepted merely because the library name appears compatible.

---

# 16. ERC rules

ERC must detect at minimum:

- unconnected power inputs;
- unconnected power outputs;
- duplicate power drivers;
- missing PE connection;
- missing CP reference;
- missing ADC reference;
- missing isolated supply;
- MCU output driving another output;
- connector pin without net;
- safety output without feedback input;
- E-stop chain discontinuity.

ERC is not proof of electrical safety.

---

# 17. DRC rules

DRC must check:

- minimum clearance;
- minimum track width;
- minimum via diameter;
- copper-to-edge clearance;
- courtyard overlap;
- hole-to-copper clearance;
- solder mask slivers;
- unconnected copper;
- differential pair constraints where used;
- custom isolation keepouts.

The final minimum clearances must come from the selected PCB manufacturer plus the applicable safety/isolation design requirements.

---

# 18. Isolation keepouts

PCB-A shall have explicit keepout regions around every AMC1311B isolation barrier.

Minimum prototype target:

**8 mm creepage/clearance where the actual device/package and applicable requirements permit/require it.**

This is not a universal certification number. Final values are determined by working voltage, pollution degree, material group, altitude, overvoltage category and the relevant standards/device data.

No copper pour crosses an isolation barrier.

No mounting hole may bridge an isolation barrier unless the mechanical part is demonstrably compatible with the required insulation system.

---

# 19. Stackup

All three signal PCBs:

- 4 layers;
- FR-4;
- 1.6 mm nominal;
- 1 oz copper baseline;
- ENIG preferred for prototype assembly;
- controlled impedance only where required.

Suggested:

```
L1  Signal / Components
L2  GND / reference
L3  Power / secondary routing
L4  Signal / service
```

The actual manufacturer stackup must replace the nominal values before fabrication.

KiCad supports entering the physical layer stackup, dielectric properties and copper thickness directly in Board Setup. citeturn0search52

---

# 20. Manufacturing release files

Before PCB fabrication, each board must produce:

- Gerber;
- drill;
- fabrication drawing;
- assembly drawing;
- BOM;
- pick-and-place;
- 3D preview;
- revision identifier;
- checksum/release manifest.

No Gerber is a production release until:

```
SCHEMATIC
  -> ERC
  -> FOOTPRINT REVIEW
  -> PCB
  -> DRC
  -> ISOLATION REVIEW
  -> BOM REVIEW
  -> MANUFACTURING REVIEW
  -> RELEASE
```

---

# 21. Revision control

Revision format:

```
TS-V1-M2.7-R0
TS-V1-M2.7-R1
TS-V1-M2.7-R2
...
```

Every PCB revision records:

- Git commit;
- KiCad version;
- schematic revision;
- PCB revision;
- BOM revision;
- manufacturer stackup;
- engineer/reviewer;
- unresolved HOLD items.

---

# 22. M2.7 verification gate

M2.7 passes only when:

- [ ] project hierarchy exists;
- [ ] all 15 sheets are represented;
- [ ] all nets have controlled names;
- [ ] symbols have verified packages;
- [ ] footprints have datasheet verification;
- [ ] PCB-A has placement;
- [ ] PCB-B has placement;
- [ ] PCB-C has placement;
- [ ] PCB-D has wiring plan;
- [ ] net classes exist;
- [ ] isolation keepouts exist;
- [ ] ERC rules exist;
- [ ] DRC rules exist;
- [ ] harness pinouts exist;
- [ ] BOM references match schematic references;
- [ ] independent measurement calibration path exists.

---

# 23. M2.8 next step

M2.8 is the **first real PCB routing release**:

1. PCB-A complete placement;
2. PCB-A routing;
3. PCB-B placement/routing;
4. PCB-C placement/routing;
5. exact footprints;
6. exact 3D models;
7. exact manufacturer stackup;
8. ERC run;
9. DRC run;
10. isolation review;
11. manufacturing outputs;
12. assembly drawings;
13. first prototype fabrication package.

The 32 A mains assembly remains a separate industrial wiring drawing and is not converted into a low-voltage PCB merely for convenience.

---

## 24. Source verification

TI's current TIDA-010939 reference design explicitly supports IEC 61851 Control Pilot and publishes design files, including schematic/design guide, assembly drawing, BOM and Gerber data. citeturn0search0

TI's design guide documents the CP state resistance and 1 kHz signalling used by this TestStation's simulator architecture. citeturn0search49

Phoenix Contact's current product page confirms the selected Type 2 socket 1052448 is a 32 A, 480 V AC interface with CP/PP and 12 V locking actuator. citeturn0search1

Murata's current MEE1S2405SC data identifies 24 V input, 5 V output, 1 W maximum, 200 mA maximum output and 1000 V isolation. citeturn0search50
