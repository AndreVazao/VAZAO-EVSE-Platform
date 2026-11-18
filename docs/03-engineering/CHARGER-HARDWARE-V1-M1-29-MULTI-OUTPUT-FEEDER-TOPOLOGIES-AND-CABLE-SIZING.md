# VAZÃO EVSE — Charger Hardware V1
## M1.29 — Multi-output feeder topologies and cable-sizing framework

**Status:** DESIGN REQUIREMENT BASELINE — NO CABLE CROSS-SECTION OR PROTECTIVE DEVICE RELEASED  
**Date:** 2026-11-18  
**Applies to:** dual-output and quad-output AC chargers, wallbox and pedestal variants, and the upstream distribution interface of MultiStation systems.  
**Depends on:** M1.19 electrical boundaries, M1.20 panel zoning, M1.21 enclosure requirements, M1.22 CAD input matrix, M1.26 validation tooling, M1.27 component register and M1.28 CHARX controller audit.

## 1. New mandatory product requirement

A dual-output or quad-output charger must support engineering evaluation of more than one incoming supply arrangement. The product design must not assume that one feeder per charging output is always available, nor assume that a single shared feeder is always preferable.

For every product variant, the electrical design package must include at least:

- **Independent feeders:** two or four separate supply circuits arrive from the upstream distribution board, one dedicated final circuit per charging output.
- **Common feeder:** one appropriately sized incoming feeder arrives at the charger or its associated distribution enclosure, then feeds individually protected output branches.
- **Common feeder with managed demand:** a common feeder supplies several outputs while a local, fail-safe load-management function enforces a defined maximum demand at the feeder boundary.
- **Hybrid arrangement:** where the site design requires it, more than one feeder group supplies subsets of outputs; every group has its own defined protection, isolation and load limit.

These are alternative site/product interface architectures. They must be represented in the wiring schedule, protection coordination, terminal plan, cable entry arrangement, enclosure/CAD model and installation documentation.

## 2. Portuguese installation guidance and design interpretation

The Portuguese CTE 64 / IEP *Guia Técnico das instalações elétricas para alimentação de veículos elétricos*, Edition 3 (2023-09-14), approved by DGEG as an informative/orienting guide, interprets the RTIEBT and specifically addresses EV charging installations:

- Section 3.1.2 states that supply may be single-phase or three-phase and that design power is selected from the EV charging requirement.
- Section 3.1.3 sets simultaneity at 1.00 for circuits directly feeding individual EV connection points. For circuits feeding multiple connection points, a factor below 1.00 may be used only when a load-control system is installed.
- Section 3.1.5 says each EV connection is to be made by a dedicated circuit; the EV circuit should not normally be affected by failure of other circuits.
- The guide states a 5% maximum voltage drop between the installation origin and the EV connection point.
- Section 4.3 refers overcurrent protection to RTIEBT sections 43 and 533 and gives 2.5 mm² as a minimum conductor cross-section for the dedicated EV circuit. This minimum is not a design recommendation for a 32 A feeder and never replaces current-carrying capacity, voltage-drop, short-circuit or protective-device calculations.

The guide is informative and does not replace the applicable RTIEBT, current applicable harmonised standards, project-specific design, utility requirements or qualified electrical review. The actual edition and applicability of each standard/regulation must be confirmed at design release.

Primary references:
1. IEP / CTE 64, Guia Técnico das instalações elétricas para alimentação de VE, Edition 3 (2023): https://www.iep.pt/wp-content/uploads/2023/10/Guia-VE-Ed.3-2023.pdf
2. RTIEBT, Portaria n.º 949-A/2006, including conductor section selection principles: https://dgsl.pt/legislacao/portaria_949-a-2006
3. IEC 60364-7-722:2018 official publication page: https://webstore.iec.ch/en/publication/29958
4. Schneider Electric Electrical Installation Guide — EV charging design and simultaneity: https://www.electrical-installation.org/enwiki/EV_charging_-_electrical_installation_design
5. Schneider Electric Electrical Installation Guide — cable selection and installation methods: https://www.electrical-installation.org/enwiki/General_method_for_cable_sizing

## 3. Reference current model for the V1 22 kW output

For the existing three-phase reference output:

- Nominal system: 230/400 V AC, 3-phase + neutral + PE.
- Maximum reference output: 22 kW class.
- Output current reference: 32 A per phase at 400 V three-phase.
- Apparent power from the Portuguese guide's 32 A / 230/400 V table: 22.170 kVA per output.

The following figures are **feeder-current planning values**, not cable sizes and not a statement that every variant must operate all outputs simultaneously.

| Charger | Number of 22 kW-class outputs | Unmanaged simultaneous design current at 400 V 3-phase | Approx. apparent power |
|---|---:|---:|---:|
| Single | 1 | 32 A/phase | 22.17 kVA |
| Dual | 2 | 64 A/phase | 44.34 kVA |
| Quad | 4 | 128 A/phase | 88.68 kVA |

For a balanced 3-phase load, the current values are per phase in the shared upstream feeder. They are not to be added as 32 A × 3 phases when selecting a three-phase feeder. The final calculation must account for actual power factor, efficiency where relevant, phase allocation, harmonics, neutral loading, auxiliary loads and the exact charger configuration.

If outputs are configured for single-phase operation, calculate phase-by-phase current and worst-case imbalance; a single aggregate kW figure is not enough. The product's load-balancing policy must distribute phases where the hardware supports it, but must never assume perfect balance without proof.

## 4. Architecture A — independent incoming feeders

Conceptual arrangement for four outputs:

```text
UPSTREAM DISTRIBUTION BOARD
  ├── Feeder A + protection/isolation ──> Output 1 local protection ──> EVSE 1
  ├── Feeder B + protection/isolation ──> Output 2 local protection ──> EVSE 2
  ├── Feeder C + protection/isolation ──> Output 3 local protection ──> EVSE 3
  └── Feeder D + protection/isolation ──> Output 4 local protection ──> EVSE 4
```

For a dual charger, use two independent feeder paths; for a quad charger, use four. Each feeder is designed for the maximum configured current of its output, normally 32 A/phase for the 22 kW reference output unless the product variant is explicitly configured lower.

Requirements:
- Each feeder has an identified origin, protective device, isolation method, cable route, length and termination.
- Each output has its own final-circuit protection and EV-specific residual-current/DC-fault protection strategy as required by the applicable design.
- A fault on one feeder/output should not unintentionally remove other independent outputs; verify selectivity and common upstream protection.
- The machine must support separate incoming cable entries/glands, terminal compartments, strain relief, PE bonding and segregation.
- If all feeders share an enclosure, the incoming terminal and isolation layout must prevent unsafe cross-connection and permit safe maintenance of one output while the others remain live, if that maintenance mode is intended and formally assessed.
- If a single common emergency disconnect is provided, its scope must be clearly documented; it does not replace individual protective devices.

Advantages: straightforward per-output capacity and isolation; faults can be more local; useful where the site already provides separate circuits.

Costs/limitations: more cable routes, more upstream protective ways, more installation labour and more enclosure entries/termination space.

## 5. Architecture B — one common incoming feeder with internal distribution

Conceptual arrangement:

```text
UPSTREAM DISTRIBUTION BOARD
  └── COMMON FEEDER (sized for aggregate permitted demand)
        │
        └── Charger main isolator / main protection
              │
              └── Rated distribution block / busbar
                    ├── Output 1 branch protection ──> EVSE 1 local safety + contactor + connector
                    ├── Output 2 branch protection ──> EVSE 2 local safety + contactor + connector
                    ├── Output 3 branch protection ──> EVSE 3 local safety + contactor + connector
                    └── Output 4 branch protection ──> EVSE 4 local safety + contactor + connector
```

Requirements:
- The common feeder, its upstream protective device, main isolator, internal distribution block/busbar, supports, terminals and enclosure thermal design must be rated for the maximum permitted aggregate demand.
- Every output branch must retain its required individual overcurrent protection and EV-specific residual-current/DC-fault protection. The protective device may be located upstream or inside the EVSE only where the applicable standard and product construction permit it; the protection boundary must be explicit.
- Internal branch wiring is sized independently from the incoming feeder. It is not automatically the same cross-section as the feeder.
- The common feeder and internal busbar must be evaluated for short-circuit withstand, let-through energy, protective coordination, terminal temperature and fault propagation.
- Provide a defined main isolation point and output branch isolation/maintenance procedure.
- A common feeder does not mean a common unprotected connection feeding all contactors directly.
- A common neutral or shared protective device arrangement must be engineered for the actual RCD topology; do not share neutrals across independently protected circuits unless the protection design explicitly supports it.
- PE continuity and bonding are maintained; PE is never switched by normal output contactors.

For an unmanaged quad at 4 × 32 A three-phase, the common feeder's planning demand is 128 A per phase (about 88.68 kVA balanced). For an unmanaged dual at 2 × 32 A, it is 64 A per phase (about 44.34 kVA balanced). These figures do not select the cable cross-section or breaker.



## 5A. Common upstream trunk with external branching (site distribution)

The phrase “one main cable that then branches to four” also covers a distribution arrangement where the common trunk does **not** enter the charger cabinet. The main feeder may run from the site switchboard to an intermediate distribution board/branch enclosure near the charging equipment, then split into separately protected outgoing circuits to the four outputs or four individual charging units.

Conceptual arrangement:

```text
SITE MAIN SWITCHBOARD
  └── COMMON TRUNK FEEDER (aggregate permitted demand)
        │
        └── LOCAL DISTRIBUTION / BRANCH ENCLOSURE
              ├── Branch circuit 1 + protection/isolation ──> Output / charger 1
              ├── Branch circuit 2 + protection/isolation ──> Output / charger 2
              ├── Branch circuit 3 + protection/isolation ──> Output / charger 3
              └── Branch circuit 4 + protection/isolation ──> Output / charger 4
```

This is a distinct physical layout from a single feeder entering the quad charger and splitting on its internal busbar, even though the aggregate current calculation can be similar. It is also applicable to a row/cluster of separate single-output or dual-output units. The design record must identify exactly where the branch point is located: main switchboard, local QVE/sub-board, external junction/distribution enclosure, or inside the EVSE product.

Requirements:
- The common trunk is sized for the maximum aggregate demand permitted downstream, including all branch circuits and any other loads connected to that trunk.
- The branch enclosure and its incoming/outgoing terminals, busbar, protective devices, isolation, short-circuit rating and environmental/IP requirements are selected for the installation location.
- Each outgoing EV branch has its own defined protective boundary and dedicated circuit arrangement; branch cable sections are calculated separately from the trunk.
- The common trunk and branch circuits must be coordinated for fault protection and selectivity. A fault on one branch should not unnecessarily disconnect unrelated branches where the protection design can provide discrimination.
- The route length for voltage-drop calculations is split into trunk and each branch; total drop to each EV connection is the sum of the relevant upstream and branch segments.
- If a load manager controls a group of branches, its measurement point and enforced limit must cover the complete common trunk boundary, including other loads where present.
- Neutral and PE distribution, earthing arrangement, common RCD interactions, and any shared protective conductor arrangement must be designed explicitly. Never infer that a common trunk permits arbitrary shared neutrals.
- The site CAD/layout and the charger product CAD must distinguish external distribution hardware from components supplied inside the EVSE.

This topology is added to the mandatory comparison set for quad charger installations and MultiStation/park distribution. It does not reduce the required independent protection and local safety of each charging output.

## 6. Architecture C — common feeder with managed maximum demand

A common feeder may be designed for a lower maximum demand than the arithmetic sum of all output ratings only if an approved load-control system guarantees that the feeder limit cannot be exceeded.

Mandatory conditions:
1. Define a fixed feeder current/power limit for each phase, with a documented commissioning value and controlled configuration access.
2. Measure or otherwise reliably establish feeder current at the correct electrical boundary; individual output current measurement alone is not enough if other loads exist on the feeder.
3. Allocate current across outputs using per-phase constraints and output ratings.
4. Include measurement accuracy, response time, control-loop delay, communication loss, restart, stale data, sensor failure and actuator failure in the worst-case analysis.
5. Define a deterministic safe response: on loss or invalidity of the feeder measurement/control function, new sessions are inhibited and active outputs are curtailed/stopped so the feeder cannot exceed its approved safe limit. A cloud/CPMS connection is not an acceptable sole load-limit mechanism.
6. Prevent a user/operator setting from raising the limit above the cable/protection/site-approved maximum.
7. Ensure local output safety and individual branch protection remain independent of the load manager.
8. Test simultaneous connection, abrupt load steps, one controller offline, master restart, bus failure, phase imbalance and sensor disconnection.
9. The load limit must be secured against unauthorised changes and recorded in commissioning documentation.

The Portuguese Guide Edition 3 explicitly permits a simultaneity factor below 1.00 for circuits feeding multiple connection points only when a load-control system is installed. The design must therefore document the control system and the resulting maximum demand rather than apply a discretionary diversity percentage.

**Important:** a common feeder with load management is not allowed to be sized from a hoped-for average use profile. It is sized from the highest enforceable current limit, plus the applicable design and correction factors, and must remain safe under credible control faults.

## 7. Architecture D — hybrid feeder groups

The product may support group feeds, for example:
- Quad: two incoming feeders, each supplying two outputs.
- Quad: one feeder for three outputs plus one independent feeder for a priority output.
- Dual: two independent feeders or one common feeder.

Every group is treated as its own feeder system. The cable, protection, isolation, distribution and load-control boundary is documented per group. Do not infer that a group of two outputs can be sized at 32 A merely because only one vehicle is expected to charge at a time; that reduction requires an enforced load-control limit.

## 8. Cable cross-section calculation — mandatory method

The project will not publish a universal cross-section table such as “32 A = X mm²” without installation assumptions. For every incoming feeder and every output branch, the design record must contain:

### 8.1 Electrical design inputs
- System voltage and frequency; single-phase or three-phase.
- Number of phases, neutral and PE; conductor arrangement and earthing system (TT/TN as applicable).
- Rated/configured maximum current per output and per phase.
- Simultaneity/load-management limit at the relevant feeder boundary.
- Power factor and load characteristics where needed.
- Feeder length and branch lengths, including one-way route length and route segments.
- Maximum permitted voltage drop budget allocated to this feeder/branch.
- Prospective short-circuit current at origin and end of circuit; earth-fault loop/impedance where applicable.
- Protective-device type, rating, curve/setting, breaking capacity and coordination.
- Required disconnection time and verification method.

### 8.2 Cable and installation inputs
- Copper or aluminium conductor.
- Insulation type and permitted conductor operating temperature.
- Cable type, number of cores and conductor cross-section.
- Installation reference method for every route segment (conduit, trunking, tray, wall, insulation, underground duct, free air, etc.).
- Ambient air/soil temperature, thermal insulation and soil thermal resistivity where applicable.
- Number of grouped circuits/cables, spacing and grouping correction.
- Number of loaded conductors, neutral harmonic loading and phase imbalance.
- Exposure to solar radiation, water, UV, corrosion, mechanical impact, vibration and fire requirements.
- Cable manufacturer's minimum bend radius, terminal capacity and permitted conductor class.
- Route-specific mechanical protection and support spacing.

### 8.3 Required checks
For each candidate cross-section:
1. Corrected current-carrying capacity after all relevant correction factors.
2. Coordination between design current, protective-device rating and corrected cable capacity.
3. Voltage drop from installation origin to the EV connection point; verify the Portuguese guide's 5% ceiling and any stricter project/site budget.
4. Short-circuit thermal withstand and protective-device disconnection.
5. Earth-fault loop/automatic disconnection and PE continuity.
6. Neutral sizing for the actual harmonic and phase-balance conditions.
7. PE sizing and bonding under the applicable rules.
8. Terminal compatibility, lug/ferrule selection, gland range, bending space and installation feasibility.
9. Thermal interaction with adjacent feeders, busbars and enclosure components.
10. Protection selectivity/discrimination and fault containment between outputs.

The selected cross-section is the smallest standard size that passes **all** checks with documented margin, not the size that passes ampacity alone. A larger size may be required by voltage drop, short-circuit protection, terminal range, mechanical conditions or future load configuration.

## 9. Preliminary current scenarios — not cable recommendations

Assumption for comparison only: each output is configured as 32 A, three-phase, 400 V, and all outputs are allowed to operate simultaneously.

| Scenario | Incoming topology | Feeder current planning basis | Branch current basis |
|---|---|---:|---:|
| Dual A | 2 independent feeders | 32 A/phase each | 32 A/phase each |
| Dual B | 1 common feeder | 64 A/phase | 32 A/phase per output |
| Dual C | 1 managed common feeder | Approved enforced limit (to be defined) | Up to 32 A/phase per output, curtailed by manager |
| Quad A | 4 independent feeders | 32 A/phase each | 32 A/phase each |
| Quad B | 1 common feeder | 128 A/phase | 32 A/phase per output |
| Quad C | 1 managed common feeder | Approved enforced limit (to be defined) | Up to 32 A/phase per output, curtailed by manager |
| Quad D | 2 group feeders | 64 A/phase per group for 2 × 32 A unmanaged | 32 A/phase per output |

If output power is lower than 22 kW, one-phase, or dynamically limited, calculate the actual current per phase from the declared product configuration. Do not reuse the table without updating its assumptions.

## 10. Product design requirements and CAD consequences

The wallbox/pedestal product family must be designed for the following:

- Separate incoming gland/entry zones for 1, 2 or 4 feeder cables, with clear labelling and maintainable routing.
- An alternative larger single-feeder entry suitable for the maximum approved conductor size and cable diameter of the common-feed configuration.
- Optional hybrid/group entry arrangement.
- Adequate bend radius and termination space for the largest candidate feeder; no tight bend directly at the main terminals.
- Main input terminals/distribution block sized for the common-feed maximum and branch terminals sized for each output.
- Main protective/isolation device and output branch protective devices physically segregated and accessible.
- Clear physical separation of incoming high-current distribution from controller, SELV/communications, CP/PP and measurement wiring.
- Thermal design includes main terminals, busbar, branch devices and all simultaneously loaded conductors.
- Labelled cable entry and terminal identifiers that distinguish feeder 1/2/3/4 from branch output 1/2/3/4.
- The CAD model contains separate envelopes for feeder cable approach, bend radius, gland, lug, terminal, isolation handle and service access.
- The wiring schedule and installation manual show both the independent-feeder and common-feeder options, with only approved configurations enabled for each SKU.
- The product cannot be field-reconfigured between topologies by simply moving wires without a documented conversion procedure, correct protective devices and updated commissioning record.

This is now a product-family requirement, not an optional installation note.

## 11. BOM and document-control changes required

BOM should distinguish:
- CABLE-IN-IND: independent incoming feeder set (quantity by output count).
- CABLE-IN-COM: common incoming feeder (one per charger or feeder group).
- CABLE-BRANCH: internal branch conductors from distribution to each output.
- GLAND-IN: incoming cable glands/entry plates for the selected topology.
- TB-IN / BUS-IN: main incoming terminal/distribution system.
- QF-MAIN: upstream/common feeder protection and isolation as designed.
- QF-OUT[n]: individual output branch protective devices.
- PE-BAR / N-BAR: protective and neutral distribution sized and configured for the actual topology.

Exact SKUs, conductor materials, cable sections, protective-device ratings and terminal part numbers remain OPEN until a real installation envelope and qualified calculation are supplied.

## 12. Design gates

| Gate | Required output | State |
|---|---|---|
| F29-1 | Confirm product variants: 1/2/4 outputs, 1P/3P, per-output maximum current | OPEN |
| F29-2 | Define allowed feeder topologies per SKU (independent/common/hybrid/managed) | OPEN |
| F29-3 | Define upstream protection and isolation boundary for each topology | OPEN |
| F29-4 | Define branch protection and EV-specific RCD/DC protection per output | OPEN |
| F29-5 | Complete unmanaged feeder current calculations (32/64/128 A per phase reference) | Reference basis recorded; detailed design OPEN |
| F29-6 | Define and validate load-management maximum feeder limit and safe failure response | OPEN |
| F29-7 | Produce cable sizing calculations for every route scenario and installation method | NOT STARTED |
| F29-8 | Verify voltage drop, short-circuit withstand, disconnection, neutral and PE | NOT STARTED |
| F29-9 | Verify terminal, gland, bend radius and enclosure thermal/mechanical fit in CAD | NOT STARTED |
| F29-10 | Independent qualified electrical design review and release | OPEN |

## 13. Release statement

M1.29 establishes the required dual/quad feeder options and the controlled calculation method. It does not release any cable section, cable type, breaker, RCD, busbar, terminal, gland, installation drawing or wiring procedure. The reference currents are planning arithmetic only. No live installation, mains energisation, fabrication or procurement is authorised by this document.
