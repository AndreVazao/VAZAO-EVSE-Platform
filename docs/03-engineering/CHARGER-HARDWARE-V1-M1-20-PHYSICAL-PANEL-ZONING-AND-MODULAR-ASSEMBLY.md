# Charger Hardware V1 — M1.20 Physical Panel Zoning and Modular Assembly

**Status:** CONCEPTUAL MECHANICAL / ELECTRICAL LAYOUT BASELINE  
**Date:** 2026-11-12  
**Scope:** Physical zoning, modular panel organisation, repeatable output-cell assembly and service access for Single, Dual, Quad and Wallbox variants.  
**Depends on:** M1.6–M1.19, especially the modular output-cell architecture and interface boundaries.

> This document is a layout and assembly concept. It is not a dimensioned enclosure drawing, mounting-plate drilling plan, certified clearance study, wiring instruction, production assembly pack or permission to energise.

## 1. Purpose

Translate the functional architecture into a repeatable physical arrangement that can be adapted to the product family without mixing safety-critical power distribution, low-voltage control, metering, communications and optional commercial modules.

The physical design shall:
- make every output cell identifiable and serviceable;
- keep shared infrastructure distinct from repeated per-output hardware;
- provide deliberate segregation between mains and SELV/control interfaces;
- reserve defined space and interfaces for optional modules without requiring unsafe field improvisation;
- support assembly, inspection, testing and replacement;
- allow enclosure geometry to scale without assuming that the same mounting plate fits every variant.

## 2. Layout principles

1. **Functional zoning before dimensions:** establish what belongs together before assigning coordinates or rail lengths.
2. **One output = one identifiable physical cell:** use consistent labels and repeated subassemblies.
3. **Shared services are visibly shared:** upstream distribution, site measurement, cluster controller and network infrastructure must not be mistaken for per-output devices.
4. **Segregation is designed, not improvised:** mains, SELV, communications and protective wiring routes require documented separation based on applicable standards and actual device instructions.
5. **PE/bonding is continuous and inspectable:** provide accessible bonding points and a verifiable protective-conductor path.
6. **Service without disturbing adjacent outputs:** where practicable, a technician should be able to isolate and inspect one output branch without dismantling unrelated output cells.
7. **Optional means physically planned:** unused module positions have covers, labels and safe termination/blanking provisions; no exposed live terminals or loose unprotected harnesses.
8. **Thermal and EMC behaviour are layout inputs:** spacing, cable routing, ventilation and metalwork must be verified with the selected components.
9. **No generic clearance assumptions:** manufacturer clearances, creepage/clearance, heat dissipation and applicable assembly standards govern the final layout.
10. **As-built traceability:** the final physical assembly must match approved drawings and configuration records.

## 3. Physical zones

The zones below are functional areas. They may be separate compartments, mounting regions or segregated rail sections depending on the final enclosure and applicable requirements.

| Zone ID | Zone name | Typical contents | Physical rules |
|---|---|---|---|
| Z01 | Incoming supply / isolation | Supply entry, main isolation and upstream protective devices | Controlled access, guarded terminals, cable anchorage and clear identification |
| Z02 | Main distribution | Distribution blocks and outgoing branch feeds | Short, traceable routes to branch protection; no unprotected cross-routing |
| Z03-n | Output branch protection | Protective devices for output n | Repeated and clearly labelled; branch identity follows connector identity |
| Z04-n | Output switching / power interface | Contactor, feedback accessories and output power terminals | Keep each output's switching group identifiable; follow exact device thermal/spacing instructions |
| Z05-n | Metering | Output-specific meter or measurement components | Meter-to-output identity physically unambiguous; preserve certified measurement boundary |
| Z06-n | Local EVSE control | Local controller/interface, CP/PP, locking and local inputs | Keep controller and its output-specific interfaces associated with the same cell |
| Z07 | Shared controller / cluster | Gateway, cluster controller and supported backplane modules | Clearly identify shared dependency; respect bus limits and manufacturer's mounting/accessory instructions |
| Z08 | Auxiliary power | Approved power supplies, fusing and distribution for each auxiliary domain | Separate budgets and labels for controller bus, auxiliary 12 V, coils and safety domains |
| Z09 | Safety sensing / interlocks | RCM interfaces, temperature, door/interlock and emergency interfaces as designed | Avoid routing or service arrangements that bypass protective functions |
| Z10 | Communications / service | Ethernet, RS-485, LTE/Wi-Fi, service switch and antenna interfaces | Segregated routing, strain relief, EMC treatment and service access |
| Z11 | Optional commercial modules | RFID, HMI, payment and customer-facing interfaces | Optional modules cannot occupy or compromise protective-device access |
| Z12 | PE / bonding | PE bar, enclosure/door bonds and protective conductor terminations | Accessible, mechanically robust, labelled and testable; never treated as a switched functional circuit |

A zone may contain multiple subassemblies only where separation, thermal, access and wiring requirements are demonstrated. A drawing shall explicitly show zone boundaries and any permitted crossings.

## 4. Conceptual panel arrangement

### 4.1 Single / Wallbox

Functional arrangement, not a scale drawing:

~~~text
+--------------------------------------------------+
| CUSTOMER / SERVICE INTERFACE (if fitted)         |
| RFID / HMI / PAYMENT / COMMS — OPTIONAL          |
+--------------------------+-----------------------+
| LOW-VOLTAGE CONTROL      | LOCAL EVSE CELL 01    |
| controller / interfaces  | CP/PP / lock / inputs |
| comms / service          | meter data interface |
+--------------------------+-----------------------+
| AUXILIARY POWER DOMAINS  | OUTPUT SWITCHING 01  |
| controller / 12V / coil  | contactor / feedback |
+--------------------------+-----------------------+
| MAIN DISTRIBUTION        | BRANCH PROTECTION 01  |
| isolation / distribution | output branch 01     |
+--------------------------+-----------------------+
| INCOMING SUPPLY / PE & BONDING / CABLE ENTRY     |
+--------------------------------------------------+
~~~

Wallbox packaging may place these functions on different planes or in separate compartments. The functional boundaries and service requirements remain the same.

### 4.2 Dual

~~~text
+--------------------------------------------------+
| OPTIONAL CUSTOMER / SHARED COMMS MODULES         |
+--------------------------+-----------------------+
| SHARED CONTROL / CLUSTER | SHARED AUXILIARY       |
+--------------------------+-----------------------+
| OUTPUT CELL 01           | OUTPUT CELL 02        |
| local EVSE / meter       | local EVSE / meter    |
| switching / feedback     | switching / feedback  |
+--------------------------+-----------------------+
| BRANCH PROTECTION 01     | BRANCH PROTECTION 02  |
+--------------------------+-----------------------+
| MAIN ISOLATION / DISTRIBUTION / GRID SENSE       |
+--------------------------------------------------+
| INCOMING SUPPLY / PE & BONDING                   |
+--------------------------------------------------+
~~~

### 4.3 Quad

~~~text
+--------------------------------------------------+
| CUSTOMER / OPTIONAL RFID / HMI / PAYMENT         |
+--------------------------+-----------------------+
| SHARED CONTROLLER CLUSTER | COMMS / SERVICE       |
| topology subject to proof | segregated interfaces |
+--------------------------+-----------------------+
| OUTPUT CELL 01            | OUTPUT CELL 02       |
| EVSE / meter / switching  | EVSE / meter / switch|
+--------------------------+-----------------------+
| OUTPUT CELL 03            | OUTPUT CELL 04       |
| EVSE / meter / switching  | EVSE / meter / switch|
+--------------------------+-----------------------+
| BRANCH PROTECTION 01–04 / AUXILIARY DISTRIBUTION  |
+--------------------------------------------------+
| MAIN ISOLATION / DISTRIBUTION / OPTIONAL GRID MTR|
+--------------------------------------------------+
| INCOMING SUPPLY / PE & BONDING                   |
+--------------------------------------------------+
~~~

The quad diagram is a conceptual zoning pattern only. It does not establish enclosure shape, component orientation, heat paths, conductor lengths or physical clearances. The preferred cross-shaped pedestal is a product/mechanical option to be validated separately.

## 5. Repeatable output-cell assembly

Each output cell should be developed as a controlled subassembly with a unique identifier, for example OUT-01…OUT-04. The final naming convention must be consistent across schematic, panel layout, harness labels, firmware configuration, meter mapping and service documentation.

| Assembly item | Physical grouping | Assembly / inspection requirement |
|---|---|---|
| Branch protection | Output branch zone | Correct branch ID, device orientation and access |
| Contactor and feedback | Output switching zone | Coil/control wiring distinct from switched power; verify mechanical and electrical compatibility |
| Meter / CT components | Metering zone | Serial and channel mapped to same output; CT secondary safeguards if CT topology is selected |
| EVSE controller/interface | Local control zone | Exact manufacturer mounting and connector instructions; no guessed pinout |
| CP/PP and locking interface | Local control / connector route | Protected harness, strain relief and documented connector identity |
| RCM / temperature / interlock | Safety zone | Sensor identity, cable route and fault response traceable to output |
| Type 2 connector/cable | External output interface | Mechanical retention, ingress protection, bend radius and thermal requirements verified |
| Labels and test points | Accessible service face | Safe access and no exposure to hazardous live parts during routine service |

A removable subassembly is acceptable only if its connectors, isolation procedure, protective conductor continuity and reassembly checks are fully specified. Do not use a removable control module as a means of interrupting PE continuity.

## 6. Shared assemblies

Shared components must be visibly distinguished from output-specific components:

- incoming supply termination and main isolation;
- main distribution and optional grid-infeed measurement;
- shared controller/gateway cluster and its manufacturer-defined backplane;
- approved auxiliary power supplies and domain distribution;
- network/communications infrastructure;
- optional common RFID/payment/HMI infrastructure, only where multi-output behaviour is supported and validated;
- PE bar and enclosure bonding network.

A shared item creates a common-cause dependency. The design record shall state which outputs are affected by its loss, what safe state follows, how the fault is detected and how service recovery is controlled.

For CHARX, retain the documented distinction between local SEC-1000 output modules and shared SEC-3xxx cluster role. Do not place unrelated peripheral loads on the 6 A nominal controller backplane. Do not claim that shared RFID, common meter, controller or bus failure is isolated until the corresponding tests pass.

## 7. Segregation and cable-routing concept

The final layout shall provide separate, identifiable routes for:

1. mains incoming and branch power conductors;
2. switched output conductors to each charging connector;
3. PE and bonding conductors;
4. contactor coil and feedback circuits;
5. SELV controller and sensor interfaces;
6. RS-485 meter/RFID and other communications;
7. Ethernet and external network connections;
8. customer-facing HMI/payment/RFID harnesses.

Crossings should be minimised and controlled. Where crossings or shared ducts are unavoidable, demonstrate compliance with applicable insulation, separation, EMC and manufacturer requirements. Do not assume that different voltage classes may share a duct merely because wires are individually insulated.

Cable ducts, glands, bend radii, conductor support, ferrules, terminals, shielding and segregation distances remain design outputs based on actual components and standards. No numerical separation is specified here.

## 8. Thermal, EMC and environmental layout

The mechanical/electrical layout review must include:

- component heat losses and simultaneous worst-case operating profile;
- contactor and protective-device temperature rise under continuous duty;
- power-supply derating and ventilation requirements;
- ambient temperature, solar loading and installation orientation;
- airflow path and prevention of hot-air recirculation;
- separation of heat sources from meters, controllers and temperature-sensitive electronics;
- EMC routing for switching, power, RS-485, Ethernet and antenna coax;
- surge protection placement and conductor routing based on the approved protection concept;
- enclosure IP/IK, corrosion, condensation, UV and water ingress;
- cable-entry sealing, drainage/condensation strategy and service-door exposure.

No thermal performance, IP/IK rating or EMC compliance is inferred from this conceptual layout. These require enclosure and component data plus appropriate verification.

## 9. Access, isolation and maintainability

The assembly shall support a documented safe service procedure:

- identify the unit and output before intervention;
- isolate and secure the appropriate supply using the approved isolation procedure;
- verify absence of voltage using the approved method and equipment;
- maintain required PE/bonding and protective barriers;
- provide access to device markings, terminals and manufacturer-required service clearances;
- avoid placing optional modules in front of protective devices or service-critical terminals;
- allow replacement of a meter/controller/peripheral without changing another output's identity or configuration;
- record removed/installed serial numbers, firmware and test results;
- perform required inspection and functional checks before returning an output to service.

The exact isolation points, lockout/tagout procedure, safe working distances and test method must be defined by the qualified installation/service design and local rules.

## 10. Optional module bays and blanking strategy

Provide planned mounting and interface provisions for optional RFID/NFC, Ethernet, LTE, Wi-Fi, HMI, payment, telemetry and service modules. Each bay shall define:

- mechanical envelope and mounting method;
- connector/harness identity and keying;
- approved power domain and load budget;
- data interface and isolation requirements;
- antenna and EMC needs where applicable;
- blanking cover and unused-connector protection;
- firmware/configuration state when absent;
- installation and replacement instructions.

An unused bay must remain electrically safe, mechanically closed and environmentally sealed to the declared enclosure rating. Do not leave loose harnesses, unprotected terminals or software dependencies on absent modules.

## 11. Variant assembly matrix

| Feature | Single | Dual | Quad | Wallbox |
|---|---:|---:|---:|---:|
| Output cells | 1 | 2 | 4 | 1 (baseline) |
| Branch protection groups | 1 | 2 | 4 | 1 |
| Local EVSE functions | 1 | 2 | 4 | 1 |
| Output switching/feedback groups | 1 | 2 | 4 | 1 |
| Per-output meter provision | 1 | 2 | 4 | 1 |
| Shared controller/gateway | Optional / topology dependent | Optional / topology dependent | Candidate cluster, validation required | Optional / topology dependent |
| Grid-infeed measurement | Optional | Optional | Optional | Optional |
| RFID/HMI/payment provision | Optional | Optional/shared only after validation | Optional/shared only after validation | Optional |
| Enclosure / mounting | Variant-specific | Variant-specific | Pedestal/cross layout candidate | Wall-mounted, variant-specific |

Counts describe functional provisions, not a released BOM. The meter row means one attributable channel per output where the use case requires commercial measurement; it does not select a meter model.

## 12. Mechanical data required before dimensioned CAD

The following inputs are mandatory before creating a dimensioned panel or enclosure:

1. Selected components and manufacturer outline drawings.
2. Manufacturer mounting orientation, spacing, ventilation and terminal access requirements.
3. Enclosure internal dimensions, material, wall thickness and door geometry.
4. Mounting plate thickness, DIN rail type/length and fastener system.
5. Cable entry locations, gland sizes, bend radii and strain-relief requirements.
6. Heat-loss data and thermal simulation/test conditions.
7. IP/IK target and environmental installation class.
8. PE/bonding details for enclosure, doors, removable panels and external connector bodies.
9. Segregation/clearance requirements from applicable standards and device instructions.
10. Maintenance access, lifting/handling, anti-vandalism and public-access constraints.
11. Type 2 socket/cable mounting envelope and mechanical loads.
12. Production tolerances, corrosion protection and assembly sequence.

Do not create a drilling template or dimensioned SVG from placeholder component sizes. The existing conceptual zoning drawings remain non-dimensional until these inputs are available.

## 13. Assembly sequence — controlled concept

A future production work instruction should be derived from the approved CAD and wiring pack. The conceptual sequence is:

1. Inspect enclosure, mounting plate, protective bonding points and mechanical finish.
2. Install PE/bonding hardware and verify continuity at the defined inspection stage.
3. Fit rails, ducts, barriers and approved distribution hardware.
4. Install incoming isolation and main distribution components.
5. Install output branch protection and uniquely labelled output subassemblies.
6. Install switching, feedback, metering and local EVSE modules according to approved drawings.
7. Install auxiliary power domains and protected distribution.
8. Install shared controller/communications modules and optional service bays.
9. Route and terminate conductors by voltage/function domain using the approved wiring schedule.
10. Apply wire, terminal, device, output and warning labels.
11. Perform independent visual, mechanical, PE/bonding, wiring and torque inspections.
12. Execute the approved unenergised/SELV tests and controlled bench validation.
13. Close the enclosure only after inspection records and deviations are accepted.
14. Complete the as-built configuration and test dossier.

This sequence is not a field instruction and does not define safe work on live equipment. Mains work must be performed by competent personnel under an approved procedure.

## 14. CAD and drawing deliverables required next

Before a production assembly release, create and cross-reference:

- dimensioned enclosure general arrangement for each mechanical variant;
- dimensioned mounting-plate layout with component footprints from manufacturer drawings;
- zoning and segregation drawing;
- DIN rail and duct schedule;
- PE/bonding and protective conductor drawing;
- harness and cable-route drawing;
- output-cell assembly drawing and bill of materials;
- door/customer interface drawing;
- gland/cable-entry drawing;
- assembly and inspection work instruction;
- as-built label and configuration schedule.

Each drawing shall have a revision, author/reviewer, source component revisions, status and approval record. Conceptual drawings must be watermarked or clearly labelled NOT FOR CONSTRUCTION.

## 15. Open issues and release gates

| Gate | Required evidence | Status |
|---|---|---|
| P1 Product envelope | Approved dimensions, mounting and service envelope | OPEN |
| P2 Component footprints | Exact manufacturer outline drawings and mounting data | OPEN |
| P3 Segregation | Applicable standard review and dimensioned separation study | OPEN |
| P4 Thermal | Loss budget, airflow design and thermal verification | OPEN |
| P5 PE/bonding | Complete bonding drawing and continuity test plan | OPEN |
| P6 Cable routing | Approved wire classes, ducts, glands, bend radii and routes | OPEN |
| P7 Serviceability | Access/isolation review and maintainability assessment | OPEN |
| P8 Variant reuse | Single/Dual/Quad/Wallbox assembly comparison | DOCUMENTED / REVIEW OPEN |
| P9 CAD | Dimensioned drawings from selected components | NOT STARTED |
| P10 Assembly validation | Inspection and bench records against released drawings | NOT STARTED |

## 16. M1.20 conclusion

M1.20 translates the M1.19 functional architecture into a physical zoning and modular assembly concept. It distinguishes shared infrastructure from repeated output cells, establishes layout/segregation/thermal/service requirements, and defines the mechanical evidence required before dimensioned CAD.

**Decision:** accept the zoning model as a conceptual basis for detailed mechanical design and review. Preserve independent output identity and local safety boundaries across all variants.

**Not released:** enclosure dimensions, component coordinates, drilling, terminal layout, wire routing, clearances, production assembly instructions or BOM freeze.

**Explicitly not authorised:** mains energisation, fabrication release, installation, commercial billing or deployment. Qualified design review and the M1.18 validation gates remain mandatory.
