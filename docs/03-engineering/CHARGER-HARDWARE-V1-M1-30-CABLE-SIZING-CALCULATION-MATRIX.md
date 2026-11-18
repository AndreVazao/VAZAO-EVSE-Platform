# VAZÃO EVSE Charger Hardware V1 — M1.30 Cable Sizing Calculation Matrix

**Status:** calculation framework and evidence record only. No cable, protection device or installation design is approved.

## 1. Purpose and boundary

M1.30 turns the M1.29 feeder topology requirement into a repeatable, auditable calculation record. Each physical circuit is calculated independently: each incoming feeder, common trunk, hybrid group feeder, internal branch and external outgoing branch receives its own record. The record links each branch to its parent circuit so that voltage drop can be accumulated from the installation origin to the EV connection point.

This milestone does not choose a cable section, cable family, breaker, RCD, busbar, terminal or gland. It does not replace the applicable RTIEBT, IEC/HD standards, manufacturer tables or a qualified electrical designer. A schema-valid record is not proof that the calculation is correct.

## 2. Topology coverage

| Topology | Records required |
|---|---|
| Independent feeders | One record per dedicated feeder and one per downstream branch where applicable |
| Common feeder, split inside charger | One common feeder record plus one individually protected branch record per output |
| External common trunk | One site trunk record, one record per outgoing branch, plus any upstream/other load circuit in the distribution design |
| Hybrid groups | One record per group feeder and one per output branch |
| Managed common feeder | Same circuit records as the physical topology; additionally evidence the locally enforced maximum demand and failure response |

Do not collapse a trunk and its branches into a single fictitious route. The voltage drop to output *n* is the trunk drop plus the drop on branch *n* (and any other series segment). Branches are not summed as if they were in series. The common feeder current is based on the highest aggregate demand that the system can actually permit, phase by phase.

## 3. Required input set — one record per circuit

### Electrical duty
- Circuit ID, origin, destination, parent circuit and topology.
- Single/three-phase arrangement, nominal voltage, frequency, number of loaded phases and power factor.
- Maximum design current per phase, including simultaneous downstream demand and any enforceable local load limit.
- Declared charger/output configuration and operating envelope; identify phase imbalance and harmonic assumptions.

### Cable and installation
- Copper or aluminium; cable type/standard, insulation and temperature rating; core count and loaded conductors.
- Candidate conductor section; neutral and PE sections recorded separately where applicable.
- Actual one-way route length for this circuit segment.
- Reference installation method and exact installation conditions: conduit, trunking, tray, wall, thermal insulation, buried duct/direct burial or free air.
- Ambient/soil temperature, soil thermal resistivity when relevant, grouping count/spacing, solar exposure and other applicable correction conditions.
- Manufacturer minimum bend radius, cable outside diameter, conductor class, lug/ferrule compatibility, gland range, terminal limits and mechanical protection.

### Protection and fault conditions
- Protective device exact manufacturer/model, type, rating, curve/settings and breaking capacity.
- Prospective short-circuit current at the relevant point; fault-loop/earth-fault impedance and required disconnection time.
- Upstream/downstream protection coordination and selectivity.
- RCD/DC residual-current protection architecture for the EVSE output; this is not replaced by feeder overcurrent sizing.
- Earthing arrangement, PE continuity/bonding and neutral loading/harmonics.

### Evidence
- Exact manufacturer cable datasheet/table and revision used for ampacity, resistance and reactance.
- Source for each correction factor and its applicability.
- Protection-device datasheet and relevant trip/let-through data.
- Route drawing or measured route record; do not substitute straight-line map distance for installed cable length.
- Reviewer identity/date and approval reference. Independent competent review is mandatory before design release.

## 4. Calculation sequence

1. **Establish design current (IB).** Calculate per phase from the actual configured load and simultaneous demand. For a managed feeder, use only a maximum demand limit enforced locally by a secured control function with a validated fail-safe response. Do not apply diversity because typical users are unlikely to charge simultaneously.
2. **Select candidate cable data.** Obtain base ampacity (Iz-table), resistance and reactance from the exact cable manufacturer's documentation or applicable standard table for the cable construction and installation method. Record the source and revision.
3. **Apply correction factors.** Calculate corrected ampacity from the applicable temperature, grouping, soil and other factors. The calculation record must show every factor and source; do not apply a factor twice or use factors outside their stated scope.
4. **Check protective coordination.** Demonstrate the applicable relationship, normally IB ≤ In ≤ Iz (corrected), together with the protective-device conventional operating-current condition where required by the governing standard. Confirm breaking capacity and coordination with upstream/downstream devices.
5. **Calculate voltage drop.** Use the actual route length and operating-temperature conductor resistance. For a balanced three-phase circuit, a common engineering form is ΔU = √3 × I × L × (R cosφ + X sinφ). For a single-phase two-wire circuit, a common form is ΔU = 2 × I × L × (R cosφ + X sinφ). Use consistent units (R and X in Ω/km, L in km); confirm the selected method against the applicable cable/standard calculation method. Include upstream series segments and confirm total origin-to-EV-point voltage drop against the project allocation and applicable Portuguese guidance. Do not automatically allocate the full 5% to every segment.
6. **Check short-circuit thermal withstand.** Where the adiabatic method is applicable, verify S ≥ I√t/k using the correct conductor/insulation material constant, fault current and protective clearing time. Where device current limitation or other methods govern, use manufacturer data and the applicable standard instead. Also verify automatic disconnection and earth-fault loop conditions.
7. **Verify neutral and PE.** Assess phase imbalance, harmonics and neutral current. Size PE and verify bonding/continuity under the applicable rules; do not infer PE size solely from phase conductor size without checking the permitted method and conditions.
8. **Verify physical installation.** Check terminal conductor material/class and section range, lug, gland, cable diameter, bend radius, pulling/installation limits, enclosure thermal interaction and maintainable segregation.
9. **Compare standard sections.** Start with candidate standard sections from the selected cable family. Reject any candidate failing any check. Select the smallest candidate that passes all checks with documented margin, unless reliability, future expansion or mechanical constraints justify a larger section.
10. **Independent review.** A qualified reviewer checks inputs, sources, formulas, protection coordination and installation assumptions. Only then may the record status progress beyond study/review pending.

## 5. Important formula and unit controls

- Three-phase voltage drop expression above assumes a balanced load and a consistent per-phase conductor R/X model. Manufacturer/standard methods may require different treatment of conductor arrangement, temperature, power factor or harmonics.
- Single-phase expression includes the outgoing and return conductor path through the factor 2.
- For branched systems, calculate each segment with its own current and length; sum only the voltage drops along the actual path to the endpoint.
- Ampacity is not obtained from conductor area alone. The selected table must match cable construction, conductor material, insulation, number of loaded conductors and installation reference method.
- A load manager does not reduce branch protection requirements or remove per-output EVSE safety functions.
- PE is never switched by normal EV contactor operation. Neutral switching/arrangement follows the earthing and protection design.

## 6. Machine-readable record

Schema: `schemas/electrical/cable-sizing-record.schema.json`

One JSON record is required per physical circuit segment. It captures topology, parent circuit, supply, duty current, cable construction, installation conditions, route length, voltage-drop budget, protective device, ampacity evidence, fault checks, review and release state.

The schema checks record shape and selected data constraints only. It does not calculate ampacity, validate the engineering formula, authenticate a datasheet, prove the route length, verify correction factors or certify a design. A future automated calculator must consume traceable manufacturer/standard inputs rather than embedding generic ampacity tables.

## 7. Calculation matrix — records to be completed

| Product / scenario | Circuit records | Current basis | Status |
|---|---|---|---|
| Dual, independent feeders | Feeder 1, feeder 2; output segments as applicable | Per-output configured current | Inputs not supplied |
| Dual, common internal feeder | Common feeder + output 1 branch + output 2 branch | Aggregate permitted demand; branch per output | Inputs not supplied |
| Quad, independent feeders | Four feeder records | Per-output configured current | Inputs not supplied |
| Quad, common internal feeder | Common feeder + four output branches | Aggregate permitted demand; branch per output | Inputs not supplied |
| Quad, external trunk | Site trunk + four external branches + any additional series segment | Aggregate downstream demand; each branch individually | Inputs not supplied |
| Quad, two hybrid groups | Two group feeders + four output branches | Per-group aggregate demand | Inputs not supplied |
| Managed common feeder | Physical feeder/branch records plus load-manager evidence | Enforced per-phase maximum | Limit and fail-safe evidence not supplied |

## 8. Data not to be invented

Until a real installation is defined, these remain unknown: route lengths, installation method, cable family, conductor material, ambient/soil conditions, grouping, thermal correction factors, fault level, loop impedance, protective-device model/settings, exact charger output current, power factor, harmonics, neutral loading, earthing arrangement and voltage-drop allocation.

The 32 A/output, 64 A/phase dual and 128 A/phase quad figures in M1.29 are only the unmanaged 32 A three-phase planning scenario. They are not universal product ratings and do not determine a cable section.

## 9. Release gates

| Gate | Required evidence | State |
|---|---|---|
| M30-1 | Product variant and actual maximum current per output confirmed | OPEN |
| M30-2 | Physical feeder topology and branch point confirmed | OPEN |
| M30-3 | Route lengths and installation reference methods surveyed | OPEN |
| M30-4 | Cable manufacturer's ampacity/R/X data and correction factors sourced | OPEN |
| M30-5 | Protective-device and prospective fault data confirmed | OPEN |
| M30-6 | Ampacity, coordination and voltage-drop calculations completed for every segment | NOT STARTED |
| M30-7 | Short-circuit, disconnection, neutral, PE and selectivity checks passed | NOT STARTED |
| M30-8 | Terminals, glands, bend radius and thermal/mechanical fit checked | NOT STARTED |
| M30-9 | Independent qualified electrical review signed | OPEN |
| M30-10 | Approved circuit schedule and installation drawings issued | BLOCKED |

## 10. Safety and release statement

M1.30 is a calculation governance and record-definition milestone. It is not a cable sizing result, installation design, procurement instruction, construction package or energisation approval. No cable cross-section or protective-device rating is selected. Every real installation must be calculated and reviewed by a competent qualified electrical designer against current Portuguese requirements and applicable standards before procurement, installation or energisation.
