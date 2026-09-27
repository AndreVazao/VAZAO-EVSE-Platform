# ADR-002 — Local Safety Control Boundary

**Status:** Accepted baseline  
**Date:** 2026-09-27

## Decision

VAZÃO EVSE chargers shall keep the minimum safety-critical charging control local to the EVSE controller and dedicated EVSE interface.

The CPMS is not part of the safety-critical chain.

## Why

The product requirements explicitly include operation during Internet/server outages. Therefore the machine cannot depend on cloud availability to remain electrically safe or to decide whether a safety fault is acted upon.

## Consequences

### Positive
- safe offline behaviour;
- predictable local state machine;
- reduced dependence on communications;
- easier fault isolation;
- reusable architecture for single, dual and quad chargers.

### Negative
- more logic and validation inside the charger;
- more rigorous firmware testing;
- local event persistence is required;
- controller hardware must be designed for industrial operation.

## Rejected approach

A design in which the cloud directly authorises or maintains the power contactor without a local safety boundary is rejected.

## Standards context

The architecture will be reviewed against the applicable editions of IEC 61851 and the installation requirements applicable to EV charging. IEC identifies IEC 61851-1 as covering EVSE operating characteristics, vehicle connection and electrical safety; IEC 60364-7-722 addresses circuits supplying EVs.
