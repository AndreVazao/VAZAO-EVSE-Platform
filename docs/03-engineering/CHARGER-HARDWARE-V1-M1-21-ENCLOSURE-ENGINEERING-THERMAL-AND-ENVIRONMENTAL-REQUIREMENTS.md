# Charger Hardware V1 — M1.21 Enclosure Engineering, Thermal and Environmental Requirements

**Status:** CONCEPTUAL ENGINEERING BASELINE — NOT RELEASED FOR FABRICATION  
**Depends on:** M1.19 modular electrical architecture and M1.20 physical panel zoning  
**Scope:** Wallbox, single/dual/quad pedestal, cross-shaped quad pedestal and future MultiStation enclosures.

## 1. Purpose and decision boundary

M1.21 converts the functional zones and assembly concepts from M1.20 into an enclosure-engineering requirements framework. It identifies the mechanical, thermal, environmental, installation, service and abuse-resistance inputs that must be resolved before dimensioned CAD and prototype enclosure release.

This document does **not** select a final enclosure material, supplier, IP/IK rating, dimensions, ventilation method, foundation, anchor, finish or manufacturing process. No thermal simulation or environmental test is claimed. Requirements must be confirmed against the deployment location, applicable standards, selected components and competent engineering review.

## 2. Product configurations and deployment contexts

### 2.1 Physical variants

| Variant | Enclosure problem to solve | Main design driver |
|---|---|---|
| Wallbox — 1 output | Compact wall-mounted enclosure with one repeatable output cell | Substrate/anchor compatibility, cable entry and service access |
| Wallbox — 2 outputs | Two output cells plus shared services | Internal segregation, heat density and two-cable handling |
| Pedestal — 1 output | Freestanding, ground-anchored unit | Foundation, impact exposure, drainage and maintainability |
| Pedestal — 2 outputs | Two user-facing output positions | Access from both sides, cable reach and service access |
| Pedestal — 4 outputs | Four output cells around shared infrastructure | Four concurrent loads, common-cause risks and service access |
| Cross-shaped quad pedestal | Four arms/faces around a central service core | Structural arm loads, vehicle clearances, cable routing and replaceable modules |
| MultiStation | Multiple enclosures coordinated by a local master | Repeatable unit interfaces, site distribution and service isolation |

The cross-shaped arrangement is a product concept, not a frozen geometry. Arm length, orientation, height, foundation, collision envelope and parking-bay relationship require site and mechanical studies.

### 2.2 Deployment contexts

At minimum, evaluate separately:
- **Private/residential:** controlled access, potentially sheltered mounting, owner-maintained installation.
- **Semi-public/commercial:** frequent users, greater service demand, possible exposure to cleaning equipment and accidental impacts.
- **Public/outdoor:** unrestricted access, weather/UV exposure, vandalism, vehicle interaction, accessibility, emergency response and maintainability.

A single enclosure rating or material cannot be assumed suitable for every context. The intended deployment class must be declared before selecting environmental targets.

## 3. Enclosure functional requirements

The enclosure system shall:
1. Protect users and maintain required separation from hazardous electrical parts under normal use and foreseeable service conditions.
2. Preserve the M1.19 boundary between mains distribution, each output's local safety/control, controller/backplane, auxiliary supply, contactor-coil and optional commercial/communications domains.
3. Prevent optional RFID, HMI, payment or communications omissions from creating exposed openings, unsafe access or loss of local safety.
4. Provide controlled access for installation, inspection, replacement and fault diagnosis without requiring unnecessary disturbance of adjacent output cells.
5. Support safe isolation and prove-dead workflow as defined by the final electrical design; enclosure doors/interlocks must not be treated as a substitute for electrical isolation.
6. Provide mechanical retention and strain relief for incoming supply, output cables, antenna/RF cables and communication wiring.
7. Maintain protective-earth continuity and bonding for all conductive accessible parts as required by the final design.
8. Avoid sharp edges, pinch points, trapped water paths and cable bends below the cable manufacturer's minimum radius.
9. Permit identification, warnings, serial/product labels and service instructions to remain legible throughout the declared service life.
10. Allow transport, lifting and installation without loading connectors, glands, hinges or sensitive electronics.

## 4. Preliminary zoning translation from M1.20

| Zone | Enclosure implication | Required evidence before freeze |
|---|---|---|
| Incoming supply/isolation | Dedicated entry, bend radius, gland/strain relief and safe access | Supply cable specification, installation method and isolation arrangement |
| Main distribution | Protected compartment/segregation and service access | Final device envelopes, heat loss, clearances and fault containment |
| Per-output protection | Repeatable cells and clear identification | Selected protective devices, terminal access and wiring schedule |
| Output switching | Coil/control separation, feedback access and heat management | Contactor data, duty, inrush, switching losses and replacement envelope |
| Metering | Stable mounting, readable/serviceable interfaces and signal routing | Selected meter, terminals, CT arrangement if applicable and metrology boundary |
| Local EVSE control | Protected low-voltage area with defined wiring routes | Controller, CP/PP, RCM, temperature and feedback interfaces |
| Shared controller/cluster | Central service zone with backplane limits respected | Exact cluster topology, bus and peripheral power budget |
| Auxiliary power | Segregated supply and service access | Complete load schedule, PSU losses, protective coordination and thermal data |
| Safety sensing/interlocks | Sensor placement representative of actual hot spots and door conditions | Sensor type, location, fault response and validation plan |
| Communications/service | Antenna placement, RF path and accessible service connectors | Radio approvals, antenna cable limits, EMC and coverage tests |
| Optional commercial modules | Reserved bays, blanking covers and safe cable provisions | Module dimensions, heat, access and omission-state validation |
| PE/bonding | Bonding points protected from corrosion/loosening | Material/finish compatibility, bonding hardware and continuity test |

The physical layout must retain segregation and service access when optional modules are absent. A blanking cover is part of the enclosure configuration, not an afterthought.

## 5. Thermal engineering method

### 5.1 Heat sources to inventory

Create a component-level loss register for every variant. Include, where applicable:
- contactor coil and switching/contact losses;
- protective devices and distribution terminals;
- meter voltage circuits and internal dissipation;
- controller, backplane and communication modules;
- 12 V power supply and conversion losses;
- RCM, sensors, I/O and auxiliary loads;
- cable and busbar losses within the enclosure;
- payment/HMI/display and radio modules;
- solar gain through exposed surfaces and heat conducted from the mounting surface.

Do not infer heat dissipation from electrical rating alone. Obtain manufacturer loss/dissipation data for the exact selected SKU and operating condition. Where data is absent, record the gap and measure it on a controlled bench setup.

### 5.2 Calculation framework

For each operating scenario, establish:

- (P_{loss,total} = \sum P_{loss,i}), including justified cable/busbar losses.
- Component operating temperature from the manufacturer's stated reference point and permitted ambient range.
- Enclosure internal air and surface temperatures using a documented thermal model or validated test.
- Derating for ambient temperature, grouping, mounting orientation and ventilation conditions.
- Worst-case simultaneous output duty, not only single-output operation.

The thermal assessment shall consider at least:
1. standby/idle;
2. one output at declared maximum continuous load;
3. all outputs at declared maximum simultaneous load where the electrical/site design permits it;
4. load-management transitions and repeated switching;
5. communications/HMI/payment modules operating at their highest declared duty;
6. high ambient temperature and direct solar exposure for outdoor variants;
7. blocked or degraded ventilation/filter condition where ventilation is used;
8. foreseeable single-fault conditions that can create abnormal heating.

No numerical enclosure temperature or dissipation result is established by M1.21 because final component losses, enclosure geometry, ambient envelope and duty cycle are not yet frozen.

### 5.3 Cooling strategy comparison

| Strategy | Advantages | Risks / evidence required |
|---|---|---|
| Passive natural convection | No fan power or moving parts; simpler maintenance | Requires adequate surface area, orientation and validated temperature margins |
| Ventilated enclosure | Can increase heat exchange | Ingress path, filter maintenance, dust, insects, water spray and acoustic/service issues |
| Forced-air fan | Higher controllable airflow potential | Fan failure, filter blockage, noise, power, monitoring and safe degraded operation |
| Heat exchanger / sealed cooling | Can preserve a more controlled enclosure boundary | Cost, additional failure modes, condensate management and maintenance |
| Component/layout optimisation | Reduces local heat density and hot spots | May increase enclosure volume or cable length; must preserve segregation |

Start with layout optimisation and passive cooling as the reference study, not as a predetermined solution. Any fan-dependent design needs a defined failure response and maintenance interval. A sealed enclosure is not automatically thermally suitable.

## 6. Environmental protection and materials

### 6.1 Environmental exposure register

For each deployment class, declare and validate:
- ambient operating and storage temperature range;
- humidity, condensation and thermal cycling;
- rain, wind-driven rain, splash, hose/cleaning exposure and drainage;
- dust, sand, insects and biological contamination;
- UV and solar radiation;
- salt atmosphere, coastal corrosion and industrial pollutants;
- vibration, transport shock and repeated door/cable handling;
- impact, vandalism and accidental vehicle contact;
- altitude and any resulting thermal/electrical derating;
- cleaning chemicals and maintenance products.

Ingress protection and impact ratings must be selected from the actual exposure/risk assessment and applicable product standards. No IP or IK class is approved in this milestone. A rating claim must apply to the complete assembled enclosure, including doors, glands, connectors, vents, blanking plates and installation interfaces—not just an empty enclosure catalogue entry.

### 6.2 Material options — evaluation only

| Material family | Potential benefits | Evaluation points |
|---|---|---|
| Powder-coated steel | Strength, familiar fabrication and bonding options | Coating damage, edge corrosion, coastal suitability, weight and repair |
| Stainless steel | Corrosion resistance options and robust construction | Grade/finish selection, cost, galvanic interfaces, fabrication and bonding |
| Aluminium | Lower mass and good fabrication/thermal potential | Corrosion/galvanic compatibility, structural stiffness, coating and bonding |
| Engineering polymer | Electrical insulation and corrosion resistance potential | UV ageing, fire behaviour, impact/creep, thermal limits, vandal resistance and repairability |
| Hybrid construction | Can combine structural and RF/electrical advantages | Joint sealing, galvanic corrosion, bonding continuity and assembly complexity |

Selection must consider structural loads, fire behaviour, UV ageing, corrosion category, thermal performance, EMC/RF needs, protective bonding, manufacturability, repair, lifecycle cost and local supply. No material is selected by this document.

### 6.3 Condensation and water management

IP protection does not prove immunity to internal condensation. The design shall assess:
- temperature cycling and moisture trapped during assembly;
- water paths at cable entries, doors, roof/cap and base;
- drainage routes that do not discharge onto live electrical parts, connectors or foundations;
- pressure equalisation membranes where justified;
- anti-condensation heating or humidity control only where supported by a measured need and a safe failure analysis;
- corrosion protection at cut edges, fasteners, hinges and bonding points.

Drainage, vents and membranes must be included in the complete enclosure ingress validation. Do not drill ad hoc drainage holes into a rated enclosure.

## 7. Mechanical installation and structural interfaces

### 7.1 Wallbox

Inputs required:
- permissible wall/substrate types and minimum substrate strength;
- mounting bracket and anchor loads, including cable pull and foreseeable impact;
- enclosure mass including installed modules and cable accessories;
- wall flatness, rear ventilation/thermal conduction and water run-off;
- cable entry direction, conduit/gland compatibility and installation bend radius;
- installer access to isolation, terminals and service parts;
- mounting height and accessibility requirements for the target market.

Anchors and substrate capacity must be engineered for the actual wall and installation. No generic anchor specification is released.

### 7.2 Pedestal

Inputs required:
- foundation type, soil/site assumptions and anchoring arrangement;
- overturning, wind, impact and cable-pull loads;
- baseplate, anchor access and corrosion separation;
- drainage and avoidance of standing water around the base;
- lifting/handling points and transport orientation;
- replaceable impact protection/bollards where site risk requires;
- service access without excavation or removal of unrelated output cells.

Foundation and anchor design are site-dependent and require competent structural review.

### 7.3 Cross-shaped quad pedestal

Specific issues to resolve:
- central service core with protected access and separation from user-facing interfaces;
- structural load path from each arm to the core/base, including asymmetric impact and cable pull;
- four charging faces and their vehicle/parking clearances;
- cable reach, cable storage, connector retention and prevention of trip/vehicle conflicts;
- thermal interaction between four output cells under simultaneous duty;
- routing of power, CP/PP, metering, communications and PE/bonding without creating unserviceable crossings;
- replacement of one arm/interface without dismantling the entire station, if feasible;
- drainage at arm/core junctions and the base;
- access for emergency isolation and maintenance while minimising public access to hazardous compartments.

The cross layout must be compared against a conventional four-face pedestal using serviceability, structural complexity, footprint, cable management, accessibility, thermal behaviour, transport and total installed cost. No geometry or preference is frozen.

## 8. Security, public interaction and maintainability

Evaluate:
- lock type, key/control policy and emergency/service access;
- hinge retention, door restraint and anti-tamper fasteners;
- resistance to forced opening and access to live parts;
- cable strain relief, connector retention and replaceable wear parts;
- separation of public controls/connectors from service compartments;
- label visibility, vandal-resistant display/window and replaceability;
- safe handling of sharp or damaged enclosure panels;
- spare-part availability and field replacement time;
- access to fuses/protective devices without disturbing metrology seals or safety-critical wiring;
- prevention of water ingress during service with doors open, where relevant.

The final design must define who may open each compartment, which isolation procedure applies and what seals must be preserved. Mechanical locks are not electrical safety devices.

## 9. Variant requirement matrix

| Requirement | Wallbox 1 | Wallbox 2 | Pedestal 1/2 | Pedestal Quad | Cross Quad | MultiStation |
|---|---|---|---|---|---|---|
| Wall/substrate study | Required | Required | N/A | N/A | N/A | Site-dependent |
| Foundation/anchoring study | N/A | N/A | Required | Required | Required | Site-dependent |
| Per-output thermal case | Required | Required | Required | Required | Required | Per unit |
| Simultaneous-output thermal case | N/A/one | Two outputs | Per selected count | Four outputs | Four outputs | Site aggregate |
| Outdoor exposure assessment | By deployment | By deployment | By deployment | By deployment | By deployment | By deployment |
| Public tamper/impact assessment | By deployment | By deployment | By deployment | Required if public | Required if public | By site |
| Central service-core study | N/A | Shared area | Optional | Required | Required | Master/site cabinet |
| Replaceable output cell | Preferred | Preferred | Preferred | Required design objective | Required design objective | Required design objective |
| Site vehicle/cable envelope | Required | Required | Required | Required | Critical | Required |

“N/A” only applies to the stated physical configuration; deployment-specific requirements may still introduce equivalent constraints.

## 10. Verification and environmental test plan

Testing is **NOT STARTED**. The following is a proposed plan to be refined after design inputs are frozen:

| Stage | Verification | Minimum retained evidence |
|---|---|---|
| E0 | Requirements and component-data review | Approved requirements, datasheets, loss register, risk assessment |
| E1 | Mechanical fit and access mock-up | CAD review, service-access photos, measured clearances |
| E2 | Thermal instrumentation plan | Sensor map, calibration records, measurement uncertainty |
| E3 | Controlled thermal operation | Ambient and hot-spot traces, output duty, switching profile, pass/fail limits |
| E4 | Environmental ingress/condensation | Test configuration, exposure record, inspection and functional results |
| E5 | Corrosion/material/UV qualification | Material certificates, coating data and applicable test reports |
| E6 | Mechanical/impact/vibration | Fixture, load/impact profile, deformation and post-test inspection |
| E7 | Serviceability and maintainability | Timed service tasks, access findings, seal/label inspection |
| E8 | Design review and closure | Deviations, corrective actions, independent approval and release record |

Thermal tests must use safe, controlled equipment and a test plan approved by competent personnel. Any mains-connected testing remains subject to the separate electrical safety gates; this enclosure document does not authorise energisation.

## 11. Risk register

| Risk | Consequence | Required mitigation/evidence | Status |
|---|---|---|---|
| Underestimated aggregate heat | Component ageing, derating or unsafe temperature | Exact loss data and worst-case multi-output thermal test | OPEN |
| Solar gain ignored | Outdoor overheating | Site ambient/solar envelope and test/model | OPEN |
| Ventilation compromises ingress | Water/dust entry | Complete assembled-enclosure ingress test | OPEN |
| Condensation trapped | Corrosion, tracking or malfunction | Moisture-path design and environmental cycling | OPEN |
| Corrosion at cut edges/bonding | Loss of mechanical/protective continuity | Material/finish system and continuity validation | OPEN |
| Cross-arm impact or fatigue | Structural damage and unsafe access | Structural load cases and physical test | OPEN |
| Inadequate cable management | Trip, vehicle damage or connector strain | Vehicle/cable envelope and retention tests | OPEN |
| Poor service access | Unsafe or costly maintenance | Service mock-up and maintainability review | OPEN |
| Optional bay left open | Ingress/access hazard | Keyed blanking and variant inspection | OPEN |
| Fan/filter failure | Thermal exceedance | Failure detection, derated safe response and maintenance plan | OPEN |

## 12. Inputs required before dimensioned CAD

The following inputs must be supplied or verified:
1. Declared product variants and target deployment environments.
2. Exact component SKUs and manufacturer envelope drawings.
3. Component loss/dissipation data and permitted ambient limits.
4. Electrical clearances, creepage, segregation and service-access requirements from the approved electrical design.
5. Cable types, diameters, bend radii, gland ranges and connector retention details.
6. Required output cable length/reach and vehicle/parking geometry.
7. Metering/sealing access constraints and service replacement strategy.
8. Antenna, display and payment-module mechanical/RF requirements.
9. Target ingress/impact/corrosion/UV requirements justified by risk and standards.
10. Structural load cases, mounting substrate or foundation/site assumptions.
11. Manufacturing process, finish, tolerance and supplier constraints.
12. Maintenance concept, expected service life and replaceable-part strategy.

## 13. M1.21 release gates

- **E1 — Variant definition:** wallbox/pedestal/quad/cross/MultiStation scope and deployment class agreed.
- **E2 — Component envelopes:** exact manufacturer mechanical data available for all frozen candidates.
- **E3 — Thermal budget:** component losses and simultaneous duty cases documented.
- **E4 — Cooling strategy:** selected through evidence and failure analysis, not assumption.
- **E5 — Environmental targets:** ingress, impact, corrosion, UV, temperature and humidity targets justified.
- **E6 — Material/finish:** compatibility, bonding, fire, structural and lifecycle review complete.
- **E7 — Mechanical loads:** wall bracket/foundation/arms/anchors reviewed by competent engineer.
- **E8 — Service/security:** compartment access, locks, seals, emergency/service access and maintainability reviewed.
- **E9 — CAD readiness:** all dimensions, interfaces, cable envelopes and tolerances have traceable sources.
- **E10 — Verification plan:** thermal/environmental/mechanical tests, acceptance limits and evidence retention approved.

## 14. Explicit exclusions and current status

M1.21 does not establish:
- final enclosure dimensions, weight, coordinates or drilling patterns;
- selected material, finish, supplier or manufacturing process;
- an IP/IK rating or corrosion category;
- thermal simulation results, cooling design or maximum operating temperature;
- wall anchors, foundation, arm sections or structural calculations;
- final cable routing, glands, clearances or wiring schedule;
- production CAD, fabrication drawings or assembly release.

**Status: CONCEPTUAL / OPEN.** No enclosure is released for manufacture or installation. No physical, thermal, ingress, impact, corrosion or vibration test is claimed. No mains energisation, fabrication, installation, billing or commercial deployment is authorised by this milestone.
