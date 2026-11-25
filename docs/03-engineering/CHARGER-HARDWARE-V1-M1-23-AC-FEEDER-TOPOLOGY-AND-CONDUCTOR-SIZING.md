# VAZÃO EVSE Charger Hardware V1 — AC Feeder Topology and Conductor Sizing Design Basis (M1.23)

**Status:** DESIGN-BASIS / INPUT MATRIX — NOT A CABLE SIZING APPROVAL  
**Date:** 2026-11-25  
**Applies to:** single, dual and quad AC chargers, including wallbox and pedestal variants  
**Related user requirement:** dual/quad products must allow either independent incoming electrical feeders or one common incoming feeder that distributes locally to all outputs.

## 1. Decision captured

The product architecture must not assume that every dual/quad charger receives one cable per output, nor assume that one shared cable is always used. Both physical installation arrangements are first-class design alternatives:

- **Independent feeder topology:** two incoming feeders for a dual charger; four incoming feeders for a quad charger.
- **Common feeder topology:** one incoming feeder to a local distribution assembly, then two or four separately protected output branches.

The selected topology is an installation/product-variant decision and must be explicit in the quote, single-line diagram, CAD, installation plan and cable schedule.

## 2. Reference output envelope

The current V1 reference is 400 V AC three-phase, up to 32 A per output for the 22 kW class.

For the conservative simultaneous-demand envelope, before applying an approved local load limit:

| Charger | Output channels | Maximum reference current per channel | Aggregate common-feeder current envelope |
|---|---:|---:|---:|
| Single | 1 | 32 A | 32 A |
| Dual | 2 | 32 A | 64 A |
| Quad | 4 | 32 A | 128 A |

These are design-current envelopes based on arithmetic addition of channel currents. They are not breaker ratings, cable recommendations, or proof that a particular installation can deliver the associated power.

A local load-management system may impose a lower configured aggregate limit, but the common feeder can only rely on that limit after its local enforcement, sensor integrity, controller failure response, restart behavior and commissioning test have been defined. A CPMS/cloud command alone must never be the only protection against feeder overload.

## 3. Topology comparison

| Topic | Independent incoming feeders | One common feeder + local distribution |
|---|---|---|
| Dual | 2 incoming feeders, one per output | 1 incoming feeder, 2 protected branches |
| Quad | 4 incoming feeders, one per output | 1 incoming feeder, 4 protected branches |
| Trunk sizing | Each feeder calculated for its output | Common trunk calculated for aggregate permitted demand |
| Branch sizing | Each output feeder separately calculated | Every outgoing branch separately calculated |
| Isolation | Independent upstream circuit isolation | Common upstream isolation plus per-branch isolation/protection |
| Installation | More cable routes and terminations | Fewer site cable routes; more internal distribution hardware |
| Load management | Optional for feeder sizing only if upstream circuits already sized for each channel | Can reduce permitted aggregate demand only with validated local enforcement and defined fail-safe behavior |
| Failure impact | Fault may be confined to one feeder/output depending on protection | Common feeder/distribution fault can affect all outputs |
| Enclosure | Requires space for multiple incoming glands/terminals | Requires space and thermal/short-circuit rating for common distribution assembly |

Neither topology is universally superior. Compare installation cost, serviceability, fault containment, enclosure space, cable route, local supply capacity and protection coordination.

## 4. What determines each conductor cross-section

The design must calculate **every common trunk, independent feeder and output branch separately**. The conductor section in mm² is not determined by output power alone.

Required inputs:

1. Design current and maximum simultaneous demand.
2. Supply voltage, phase count, frequency and earthing arrangement.
3. Conductor material (copper/aluminium), insulation and temperature rating.
4. Cable construction and number of loaded conductors.
5. Installation/reference method: clipped direct, conduit, trunking, tray, buried, thermally insulated or other applicable method.
6. Ambient air or soil temperature and all grouping/spacing/thermal correction factors.
7. Route length and permissible voltage drop in normal and starting/transient conditions where relevant.
8. Prospective short-circuit current, protective-device clearing time and conductor adiabatic withstand.
9. Protective device type, rating, curve/settings, breaking capacity, selectivity and coordination.
10. Neutral current, harmonic content and whether neutral reduction is permitted (never assume).
11. PE conductor sizing, fault-loop impedance and automatic disconnection requirements.
12. Terminal, distribution block, gland, connector and device conductor acceptance ranges.
13. Local Portuguese installation requirements and applicable editions of relevant IEC/HD standards.
14. Environmental/mechanical constraints, fire performance and installation route.

The governing section is the smallest standard conductor size that satisfies **all** applicable checks after correction factors and is accepted by every connected terminal/gland. The design calculation and reviewer must be recorded.

## 5. Calculation workflow

For each topology and each variant:

1. Establish the maximum allowed simultaneous current per output.
2. Establish the aggregate feeder current; do not apply diversity or software limits without a documented engineering basis.
3. Select the installation method and cable type from actual site conditions.
4. Calculate current-carrying capacity after all derating factors.
5. Check voltage drop over the actual route length.
6. Check short-circuit thermal withstand and protective-device disconnection time.
7. Check protective-device coordination, breaking capacity and discrimination.
8. Verify neutral and PE sizing independently.
9. Verify terminal/distribution assembly current and short-circuit ratings.
10. Record assumptions, calculation evidence, revision, reviewer and approval.

## 6. Load-management constraints

For a shared feeder designed below the full arithmetic aggregate envelope, the design dossier must demonstrate:

- local current measurement of the relevant feeder phases;
- deterministic local current allocation to all output channels;
- a defined maximum current limit and response time;
- behavior on sensor open/short, communication loss, controller reboot, watchdog timeout and corrupted configuration;
- safe fallback that cannot allow the aggregate demand to exceed the feeder's approved limit;
- no dependency on cloud/CPMS availability for electrical limit enforcement;
- commissioning test proving the limit under simultaneous output demand.

If these conditions are not satisfied, use the full simultaneous-demand envelope for the common feeder calculation.

## 7. Required design deliverables

- Independent-feeder single-line diagram for dual and quad.
- Common-feeder/local-distribution single-line diagram for dual and quad.
- Cable schedule covering all trunks and branches with calculated mm², material, length and installation method.
- Protective-device schedule and coordination report.
- Distribution block/busbar ratings and short-circuit withstand evidence.
- Load-management functional specification and failure-mode table where used.
- Site installation calculation and approval record.
- CAD gland/terminal layout for both entry arrangements.

## 8. Release gates and explicit non-decisions

M1.23 does **not** assign cable cross-sections, breaker ratings, RCD types, terminal block ratings or a preferred topology. No example value in this document may be used to purchase cable or install a charger.

The following remain OPEN:
- exact supply architecture and rated current per product variant;
- independent versus common feeder selection per installation;
- local load-management hardware and failure behavior;
- installation method, cable route and length;
- cable material/insulation and conductor section;
- neutral and PE sizing;
- protective-device coordination and short-circuit calculation;
- terminal/distribution assembly selection.

A suitably qualified electrical designer must complete and approve the site-specific calculation before manufacture or installation.

## 9. Next step

M1.24 shall define the feeder/load-management functional interface and produce the dual/quad single-line alternatives, keeping all cable sizes marked TBD until installation calculations and product ratings are available.
