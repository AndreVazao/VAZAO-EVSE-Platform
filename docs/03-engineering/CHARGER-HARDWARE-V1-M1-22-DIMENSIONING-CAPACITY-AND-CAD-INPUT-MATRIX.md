# Charger Hardware V1 — M1.22 Dimensioning, Capacity and CAD Input Matrix

**Status:** CAD-READINESS FRAMEWORK — DIMENSIONS AND COMPONENT ENVELOPES NOT FROZEN  
**Depends on:** M1.19 electrical boundaries, M1.20 panel zoning/assembly and M1.21 enclosure engineering  
**Scope:** Wallbox 1/2 output, pedestal 1/2/4 output, cross-shaped quad pedestal and future MultiStation.

## 1. Purpose

M1.22 defines a controlled method to translate the conceptual electrical and enclosure architecture into dimensioned mechanical CAD. It creates a capacity model, component-envelope register, usable-volume rules, access/service envelopes, cable-routing inputs, variant comparison and evidence gates.

It deliberately does not invent enclosure dimensions, component sizes, clearances, weights, cable radii, mounting coordinates or material thicknesses. Those values must come from exact manufacturer drawings, approved electrical design, site requirements, calculations or physical measurements. Until those sources are available, the corresponding fields remain OPEN and CAD may only show labelled conceptual zones.

## 2. Dimensioning principles

1. **Envelope before enclosure:** collect exact component dimensions and required service clearances before sizing the cabinet.
2. **Usable volume, not external volume:** wall thickness, doors, seals, stiffeners, rails, ducts, bend radii, access and thermal separation reduce usable space.
3. **Electrical segregation is a hard constraint:** no space optimisation may collapse the M1.19 separation between mains, per-output safety/control, auxiliary power, controller/backplane, coil and optional service domains.
4. **Serviceability is modelled:** component replacement, tool access, terminal access, door swing and safe isolation must be represented in CAD.
5. **Variants share repeatable cells:** common output-cell geometry is preferred, but shared infrastructure must not compromise per-output safety or maintainability.
6. **Optional modules are real configurations:** model installed module, reserved bay and approved blanking configuration; do not leave undefined voids.
7. **Worst-case configuration governs:** evaluate fully populated, highest-loss, maximum cable and simultaneous-output configurations.
8. **Source every dimension:** record source document, revision, page/figure, SKU or measurement method.
9. **No scale-based approval:** illustrative diagrams are not manufacturing drawings.
10. **Freeze by gate:** dimensioned CAD starts only when its inputs are sufficiently complete and reviewed.

## 3. CAD coordinate and envelope convention

Use a documented coordinate system for each enclosure:
- Origin at a defined mechanical datum (for example, a fixed mounting or base reference), explicitly stated in the CAD drawing.
- X/Y/Z axes and positive directions identified.
- Separate datums for enclosure body, door, mounting interface and service panel where required.
- Every component represented by a manufacturer-derived bounding envelope, including terminal projections, connectors, cable entry and service-removal direction.
- Every reserved service/clearance region represented as a distinct CAD envelope, not hidden inside the component solid.
- Cable routes represented by minimum bend-radius envelopes and installation/termination allowance from the cable manufacturer.
- Tolerance stack and fabrication process allowance recorded separately from nominal dimensions.

The origin convention is a modelling rule, not a prescribed physical orientation. A consistent datum must be selected for each variant before dimensioned CAD begins.

## 4. Component-envelope register

Create one controlled record per exact component SKU. Minimum fields:

| Field | Required content |
|---|---|
| Component ID | Stable project reference, e.g. KM1 / EM1 / SEC1 |
| Function / domain | M1.19 electrical domain and M1.20 physical zone |
| Manufacturer / exact SKU | No family-level substitution |
| Datasheet / drawing revision | Link, revision and retrieval date |
| Body envelope | Width × height × depth from manufacturer |
| Terminal envelope | Terminal projection and access direction |
| Connector envelope | Mating connector, plug removal and cable exit |
| Mounting | DIN rail, panel, bracket, stud or other exact method |
| Service envelope | Tool, hand and replacement/removal clearance |
| Thermal data | Dissipation, ambient limit and derating conditions |
| Mass | Exact component mass including relevant accessories |
| Cable requirements | Entry direction, conductor range, bend radius and strain relief |
| Segregation | Required electrical separation/partition from approved design |
| Orientation | Permitted mounting orientation and derating |
| Evidence state | VERIFIED / PARTIAL / OPEN / REJECTED |
| CAD object | Native model/drawing source and revision |

A family brochure or approximate catalogue picture is not sufficient for final envelope acceptance. If a manufacturer STEP model conflicts with its dimensioned drawing, record the discrepancy and obtain clarification; do not silently choose one.

## 5. Usable-space and capacity calculation

For each zone, calculate usable capacity only after modelling its actual boundaries.

A simple volume estimate is not a substitute for packing validation. The following accounting should be retained:

- (V_{gross}): internal geometric volume bounded by the enclosure.
- (V_{structure}): volume occupied by rails, plates, stiffeners, ducts, partitions, door structures and other fixed features.
- (V_{restricted}): reserved volumes for electrical segregation, airflow, drainage, cable bend radii and safety/service access.
- (V_{components}): component body and connector envelopes.
- (V_{reserve}): explicitly reserved growth/service capacity.

The residual (V_{free}=V_{gross}-V_{structure}-V_{restricted}-V_{components}) is a bookkeeping indicator only. It does not prove that the remaining space is geometrically usable or that components can be assembled and serviced. CAD collision checks, routing checks and access simulations are mandatory.

For a zone, record both:
- **Area/volume occupancy:** component envelopes versus available zone envelope.
- **Functional fit:** mounting, terminal access, cable entry, heat removal, door closure, service removal and segregation.

No universal fill percentage is imposed. Reserve capacity must be justified by identified future modules, wiring growth, thermal needs and service operations; arbitrary percentages must not be presented as engineering rules.

## 6. Functional capacity model by variant

| Variant | Repeated output cells | Shared infrastructure | Capacity issues to prove |
|---|---:|---|---|
| Wallbox 1 | 1 | Incoming distribution, auxiliary, communications/service as configured | Single-cell fit, wall mounting, connector/cable access and thermal margin |
| Wallbox 2 | 2 | Shared incoming, controller/service and optional communications | Two-cell segregation, shared-service access, simultaneous heat and two cable paths |
| Pedestal 1 | 1 | Base entry, service compartment and optional modules | Foundation/base interface, drainage, access and cable reach |
| Pedestal 2 | 2 | Shared distribution/service core | Opposing-face access, cable routes, common heat and replacement path |
| Pedestal Quad | 4 | Shared supply, cluster/controller, auxiliary and service core | Four-cell fit, four cable exits, central access, shared heat and common-cause separation |
| Cross Quad | 4 | Central core plus four arms/faces | Arm structural envelopes, central core capacity, arm routing, four user interfaces and impact/cable loads |
| MultiStation | Per declared station | Site/master distribution and communications | Site-level power, isolation, cable corridors, service zones and expansion strategy |

Output-cell count is not proof of controller autonomy. The CHARX quad study remains a shared cluster with unresolved common dependencies and the documented 6 A nominal backplane limit. Physical layout must not imply independent operation until the relevant electrical and fault tests establish it.

## 7. Zone capacity and placement schedule

Populate the following schedule for each variant:

| Zone | Items to envelope | Placement constraints | Required CAD evidence |
|---|---|---|---|
| Incoming supply/isolation | Cable gland, isolation device, terminals | Entry path, conductor bend radius, safe access | Entry section and service view |
| Main distribution | Busbars/distribution blocks/protection | Segregation, touch protection, heat and fault containment | Panel layout and clearances |
| Output protection | Per-output protective devices | Repeatable cell, labels, terminal access | Cell detail and replacement envelope |
| Switching | Contactors and feedback devices | Heat, coil wiring, terminal access, removal direction | Front/side view and service envelope |
| Metering | Exact meter/CT/terminals as selected | Metrology boundary, seals, signal routing | Meter detail and sealing access |
| Local EVSE control | Controllers, CP/PP and RCM interfaces | Low-voltage segregation, signal integrity and access | Control-zone detail |
| Shared cluster | SEC-3xxx/SEC-1000 study modules and backplane | 6 A nominal bus constraint, approved mounting and access | Cluster assembly and bus routing |
| Auxiliary power | PSU, protection and distribution | Load budget, heat, segregation and replacement | Power-zone detail |
| Safety/interlocks | Sensors, interlocks, stop devices | Representative sensor position and safe access | Sensor location and cable route |
| Communications | Ethernet/LTE/Wi-Fi/antenna | RF path, antenna separation, connector access | Antenna and service envelope |
| Optional commercial | RFID/HMI/payment/indicators | Public interaction, optional bay and blanking | Each approved configuration |
| PE/bonding | PE bar, bonding straps and studs | Continuity, corrosion, inspection and service | Bonding map and hardware detail |

The exact number and physical arrangement of devices per zone remains dependent on approved component selection and the 1/2/4-output configuration. Do not create fictional terminal blocks or protective-device counts.

## 8. Cable routing and service envelopes

For every cable group, record:
- cable identity, function, voltage/domain and segregation class;
- conductor/cable type, outside diameter and manufacturer minimum bend radius;
- route origin/destination and entry/exit direction;
- gland, connector, strain relief and termination envelope;
- expected movement/flexing and replacement path;
- separation from hot components, sharp edges, moving doors and EMC-sensitive signals;
- PE/bonding route and inspection access;
- spare capacity only where justified by a defined configuration.

The CAD model shall include door swing, removable panels, tool approach, terminal access, connector mating/unmating, meter sealing access, controller extraction, fuse/device replacement and cable withdrawal. A component that fits only when adjacent equipment is removed must be marked as a service dependency and assessed.

Do not route or dimension mains conductors from this conceptual matrix. Final wiring and segregation must follow the approved electrical design and exact component documentation.

## 9. Wallbox and pedestal mechanical interfaces

### 9.1 Wallbox
Model:
- mounting datum and bracket envelope;
- actual substrate interface and anchor positions only after structural review;
- enclosure mass and centre of gravity from selected components;
- wall clearance, door opening and service access;
- incoming cable/conduit and output cable exits;
- drainage/run-off and mounting-surface interaction;
- installation tool access and handling path.

### 9.2 Pedestal
Model:
- baseplate and foundation interface;
- anchor pattern only after structural/site calculation;
- cable entry below/through base and segregation;
- drainage and water accumulation risk;
- lifting/handling envelope and centre of gravity;
- bollard/impact-protection interface where required;
- service-door access and replacement path.

### 9.3 Cross-shaped quad pedestal
Model separately:
- central core envelope and access door(s);
- each arm's structural envelope and load path;
- arm-to-core joint and cable transition;
- four connector/cable interfaces and user clearances;
- asymmetric loads, impact zones and foundation reactions;
- service removal of one arm/interface without damaging other output cells;
- thermal coupling between the four arms and core;
- water paths at arm joints and core roof/base.

Compare the cross and conventional pedestal using a weighted decision matrix only after measurable inputs are available. Do not choose the cross layout solely for visual novelty.

## 10. Configuration and optional-module capacity

For each variant, model the following states independently:
1. BASE-PUBLIC / no RFID dependency and no optional payment module.
2. RFID-enabled configuration.
3. Ethernet communication configuration.
4. LTE configuration including antenna and cable route.
5. HMI configuration.
6. Payment terminal/device configuration.
7. Combined communications + RFID + HMI/payment configuration, where electrically and thermally supported.
8. Maintenance/service configuration with access panels open.
9. Unpopulated optional bays with approved blanking covers.

Each state must prove:
- no exposed opening or unsafe access;
- no loss of local safety function;
- acceptable thermal loading;
- no obstruction of cable routes or service access;
- no conflict with metrology seals or protective bonding;
- no unapproved shared supply/backplane loading.

## 11. CAD deliverable structure

The dimensioned CAD package should be separated into controlled layers/files:
- enclosure outer body and doors;
- structural frame/base/bracket/foundation interface;
- DIN rails, mounting plates and partitions;
- component envelope models with exact SKU metadata;
- electrical segregation and restricted volumes;
- cable routes and bend-radius envelopes;
- thermal airflow/keep-out regions;
- service and removal envelopes;
- labels, HMI, RFID, connector and user-interface cut-outs;
- PE/bonding and grounding hardware;
- optional-module configurations and blanking panels;
- assembly/exploded views and revision-controlled bill of materials.

Native editable CAD is required for engineering release. Rendered images or SVG illustrations may support review but do not replace the source model, dimensioned drawings or manufacturing data.

## 12. Design review and validation checklist

| Check | Acceptance evidence | Status |
|---|---|---|
| Every component has exact SKU and envelope | Manufacturer drawing/STEP + revision | OPEN |
| Terminals/connectors are accessible | CAD access review | OPEN |
| Cable bend radii and entries fit | Cable datasheets + routing model | OPEN |
| Electrical segregation is preserved | Approved electrical layout review | OPEN |
| Service removal is possible | Removal/access simulation | OPEN |
| Thermal keep-outs and airflow are valid | Thermal model/test plan | OPEN |
| Door, seals and blanking fit | Assembly/closure review | OPEN |
| Wall/base/arm loads are addressed | Structural calculation | OPEN |
| Optional configurations are safe | Configuration comparison and inspection | OPEN |
| Tolerance and manufacturing process are defined | Supplier/process drawing review | OPEN |
| Labels and user interfaces are accessible | Human-factors/accessibility review | OPEN |
| CAD source is editable and revision-controlled | Native files and revision record | OPEN |

## 13. Inputs still required

1. Exact controller, meter, RCM, contactor, protective-device, PSU, terminal and connector SKUs.
2. Manufacturer dimensional drawings, STEP models and mounting instructions for those exact SKUs.
3. Final per-output electrical architecture and terminal/wiring schedule.
4. Complete cable schedule, cable diameters, bend radii, glands and connector accessories.
5. Approved segregation, clearance and service-access criteria.
6. Component dissipation, ambient limits and thermal budget from M1.21.
7. Deployment environment, IP/IK/corrosion/UV targets and installation site assumptions.
8. Wallbox substrate or pedestal foundation and structural load cases.
9. User interface dimensions, accessibility and vehicle/parking/cable reach envelope.
10. Service concept, seals, replacement tasks, tool requirements and maintenance intervals.
11. Manufacturing process, material/finish, tolerances and supplier constraints.
12. Required product variants and option combinations to be released.

## 14. M1.22 release gates

- **D1 — Variant freeze:** exact physical variants and option combinations identified.
- **D2 — Component envelope evidence:** exact SKUs and manufacturer drawings available.
- **D3 — Electrical geometry:** approved electrical architecture, segregation and terminal schedule available.
- **D4 — Cable geometry:** exact cables, glands, connectors and bend radii documented.
- **D5 — Capacity proof:** CAD collision, packing, access and removal checks pass.
- **D6 — Thermal integration:** M1.21 loss budget, keep-outs and cooling strategy integrated.
- **D7 — Structural interfaces:** wall bracket/base/foundation/arms reviewed by competent engineer.
- **D8 — Configuration coverage:** optional and base configurations checked for safe blanking and no hidden dependency.
- **D9 — Native CAD control:** editable source, revisions, drawing standards and BOM linkage established.
- **D10 — Independent review:** mechanical, electrical, thermal, service and manufacturing reviews closed.

## 15. Explicit exclusions and status

M1.22 does not release:
- numerical enclosure dimensions, component coordinates or drilling patterns;
- final DIN rail/plate positions, cable routes or terminal numbering;
- component SKUs or production BOM freeze;
- numerical clearances, bend radii or structural loads without source evidence;
- IP/IK rating, material, finish or cooling solution;
- native manufacturing CAD, fabrication drawings or assembly instructions.

**Status: CAD-READINESS FRAMEWORK / OPEN.** Conceptual CAD may continue for communication and review, but must be visibly marked non-manufacturing. Dimensioned CAD and fabrication release remain blocked until the relevant D1–D10 gates close. No physical fit, thermal, environmental or structural test is claimed. No mains energisation, fabrication, installation, billing or commercial deployment is authorised by this milestone.
