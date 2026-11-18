# VAZÃO EVSE Charger Hardware V1 — M1.31 Distribution Architecture and Product Capacity Matrix

**Status:** product-family architecture and calculation inputs. No installation capacity, feeder, protective device, cable section or production rating is approved.

## 1. Purpose

M1.31 links the product family (Wallbox, pedestal and MultiStation) to the M1.29 feeder topologies and M1.30 per-circuit calculation records. It defines how to compare variants without treating connector count, charger nameplate power, site contracted power and dynamically available power as interchangeable values.

The matrix is parametric. A product may be built for a declared maximum per output and a declared aggregate limit; neither is assumed to be 22 kW merely because 22 kW / 32 A three-phase is a useful reference case. The final rating is constrained by the EVSE design, supply arrangement, protective architecture, thermal design, installation and applicable approval.

## 2. Product-family coverage

| Product family | Physical arrangement | Output count | Distribution boundary to model |
|---|---|---:|---|
| Wallbox single | Wall-mounted, one output | 1 | Incoming terminals, local protection/distribution and one output cell |
| Wallbox dual | Wall-mounted, two outputs | 2 | Common or independent incoming supply; separately defined output branches |
| Pedestal single | One pedestal, one output | 1 | Incoming feeder and local output cell |
| Pedestal dual | One pedestal, two outputs | 2 | Independent, common-internal or hybrid feeder arrangement |
| Pedestal quad | One pedestal, four outputs | 4 | Independent, common-internal, hybrid or externally distributed supply |
| Cross-shaped quad | Four arms / four output positions | 4 | Central distribution location and four mechanically distinct branch routes; exact geometry remains CAD evidence-dependent |
| MultiStation / parking group | Multiple charger units and outputs | Variable | Site trunk, external distribution board(s), branch circuits and site-level load-management boundary |

Output count is not proof of simultaneous full-power capability. Every product datasheet and installation design must separately state per-output maximum and aggregate enforced maximum.

## 3. Required capacity dimensions

For every product variant, define and retain separate fields for:

1. **Per-output electrical rating:** phase arrangement, nominal voltage, maximum current per phase, maximum apparent/active power, power factor assumptions and supported operating modes.
2. **Installed aggregate rating:** arithmetic sum of output nameplates, used as an equipment capacity descriptor, not automatically as the permitted simultaneous demand.
3. **Enforced aggregate maximum:** maximum input current/power permitted at the charger or site boundary, by phase. It may be lower than the installed aggregate only when the local load-control architecture is installed, secured, monitored and shown to fail safely.
4. **Available site capacity:** supply/contracted capacity remaining after other site loads and any required reserve. This is a site input, not a charger product property.
5. **Actual allocation:** instantaneous per-output current/power allocation. It is a control value and does not replace fixed protective-device and cable design requirements.
6. **Supply phase allocation:** phase mapping for each output, including single-phase output distribution, phase imbalance and neutral current.

Do not represent an installed nameplate sum as a continuous site demand if a validated local controller imposes a lower cap. Conversely, do not use a software setting, cloud instruction or typical utilisation factor to justify a smaller feeder unless the physical/local enforcement and fail-safe behaviour are evidenced.

## 4. Parametric electrical model

Use one current value per phase and per circuit segment. For output i, define:
- I_i,L1, I_i,L2, I_i,L3: maximum configured current drawn on each phase;
- P_i: output active power under the stated voltage, phase and power-factor assumptions;
- I_site,max,Lx: locally enforced maximum current at the site/charger supply boundary on phase x;
- I_other,Lx: other site load on phase x, measured or designed as applicable;
- I_EVSE,available,Lx: capacity allocated to EVSE on phase x.

The site allocation must satisfy, for each phase x:
- sum(I_i,Lx) ≤ I_EVSE,available,Lx
- I_other,Lx + sum(I_i,Lx) ≤ I_site,max,Lx.

For a balanced three-phase output, a planning relationship is:
S ≈ √3 × U_LL × I_line
and P ≈ √3 × U_LL × I_line × cosφ.
For a single-phase output:
S ≈ U_LN × I
and P ≈ U_LN × I × cosφ.

Use the actual supply voltage, phase arrangement, power factor and manufacturer/standard calculation method. These equations do not account by themselves for harmonic effects, unbalance, voltage variation, conversion losses or detailed cable/protection requirements.

### Reference-only scenario

For comparison only, if each output is configured at 32 A, 400 V line-to-line, three-phase:
- one output: 32 A per phase, approximately 22.17 kVA;
- two simultaneous outputs at full rating: 64 A per phase, approximately 44.34 kVA;
- four simultaneous outputs at full rating: 128 A per phase, approximately 88.68 kVA.

These values describe this particular reference scenario, not a universal Wallbox, pedestal or EVSE rating. They do not choose cable sections, protection ratings, busbars or supply capacity.

## 5. Product/topology comparison matrix

| Product | Independent incoming feeders | Common feeder split inside product | Hybrid groups | External common trunk |
|---|---|---|---|---|
| Wallbox single | One feeder | Not applicable except internal distribution | Not applicable | Possible at site level |
| Wallbox dual | One per output | One common feeder + two protected branches | Two groups only if separately justified | Possible at site level |
| Pedestal single | One feeder | Not applicable except internal distribution | Not applicable | Possible at site level |
| Pedestal dual | One per output | One common feeder + two protected branches | Two groups | Possible at site level |
| Pedestal quad | Four feeders | One common feeder + four protected branches | Two groups of two or another defined grouping | One site trunk + four branches or group branches |
| Cross-shaped quad | Four feeders, with route entry positions defined | Central common feeder + four protected arm branches | Defined feeder groups with distinct arm routes | External site trunk to central/local distribution then four branches |
| MultiStation | Dedicated feeders per unit/group | Not generally a single charger-internal bus; model at each unit boundary | Site feeder groups | Primary site-level architecture: trunk(s), local DB(s), branches |

Topology selection must consider not only electrical current but also fault containment, maintenance isolation, cable routing, voltage drop, protection selectivity, physical entry positions, service access, expansion and cost. No topology is selected for all products by default.

## 6. Load-management architecture requirements

A load-management design must identify:

- measurement location(s): site incomer, charger common feeder, group feeder and/or per-output meter;
- which currents are measured per phase and how stale, missing or implausible values are detected;
- allocation policy, priorities, minimum current constraints and behaviour when available power is insufficient;
- local controller ownership, communications path and independent local EVSE safety controller per output;
- behaviour on loss of meter, controller, internal bus, communications, network, CPMS, power supply or restart;
- secured configuration, commissioning controls, audit trail and prevention of unauthorised limit increases;
- response time and transient overshoot limits, with evidence from bench/system testing;
- whether the limit is enforced locally at the equipment/site boundary, not merely requested by a cloud service.

A site-level energy-management system may coordinate multiple chargers, but it cannot be the sole safety mechanism. Loss of the load manager must drive the system to a predefined safe operating envelope. That envelope must be calculated and validated; it is not automatically zero current or full nameplate.

## 7. Per-variant design record checklist

| Record field | Required content | State |
|---|---|---|
| Product identity | Family, variant, revision, output count, deployment context | OPEN |
| Per-output rating | Phase, voltage, maximum current/power, power factor basis | OPEN |
| Aggregate rating | Sum of output nameplates, with assumptions | OPEN |
| Aggregate enforced limit | Per-phase maximum and enforcement boundary | OPEN |
| Site capacity | Supply capacity, other loads, reserve and phase constraints | OPEN |
| Feeder topology | Independent/common internal/hybrid/external trunk | OPEN |
| Circuit schedule | One M1.30 record per physical feeder/trunk/branch | OPEN |
| Protection boundary | Upstream/downstream devices, isolation and selectivity | OPEN |
| Phase allocation | Phase map, balance, neutral/harmonic assessment | OPEN |
| Load manager | Metering, allocation, local enforcement and failure states | OPEN |
| Thermal/mechanical | Busbar, terminals, cable entries, routing and heat | OPEN |
| Verification | Calculation, fault injection, functional and independent review | OPEN |

## 8. Interfaces to other engineering documents

- M1.19: functional architecture, per-output safety boundary and local control.
- M1.20/M1.21: panel zoning, enclosure, thermal, environment and service requirements.
- M1.22: CAD input matrix; must represent the selected feeder entry/branch topology and physical routing.
- M1.29: feeder topology definitions and external common-trunk distinction.
- M1.30: per-circuit cable sizing records and calculation gates.
- Electrical schematic: one-line distribution boundary, protective-device location, phase mapping, branch IDs and load-management measurement points.
- BOM: cable, glands, terminals, busbars, protection and external distribution items remain topology-dependent until design approval.

## 9. M1.31 release gates

| Gate | Evidence required | State |
|---|---|---|
| M31-1 | Product family and output count baseline confirmed | OPEN |
| M31-2 | Per-output phase/current/power ratings declared for each variant | OPEN |
| M31-3 | Installed aggregate vs enforced aggregate capacity distinguished | OPEN |
| M31-4 | Supply phase allocation and site capacity model defined | OPEN |
| M31-5 | Feeder topology selected per variant/deployment use case | OPEN |
| M31-6 | Load-manager measurement, enforcement and fail-safe evidence defined | OPEN |
| M31-7 | M1.30 records completed for every physical circuit segment | BLOCKED |
| M31-8 | One-line diagrams, protection boundary and phase schedules reviewed | OPEN |
| M31-9 | Thermal/mechanical/CAD interfaces reconciled | OPEN |
| M31-10 | Independent competent electrical design review | OPEN |

## 10. Release statement

M1.31 is a parametric product-family distribution and capacity framework. It does not declare all outputs simultaneously available at full power, assign a site supply rating, select a feeder topology for every installation, calculate cable sections, approve protective devices or release a production design. All numeric ratings beyond the explicitly identified 32 A / 400 V three-phase reference scenario must come from a declared product variant and verified design inputs. Installation-specific electrical design and independent competent review remain mandatory before procurement, fabrication, installation or energisation.
