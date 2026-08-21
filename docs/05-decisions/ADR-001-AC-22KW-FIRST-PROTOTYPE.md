# ADR-001 — AC 22 kW as the First VAZÃO EVSE Charger Prototype

**Status:** Accepted for V1 engineering  
**Date:** 2026-08-21

## Context

VAZÃO EVSE needs a credible first hardware prototype that can demonstrate the core product architecture without the cost and complexity of a DC fast charger.

## Decision

The first hardware baseline will be an **AC Type 2 EVSE in the 22 kW class**, with one charging output.

The architecture will be modular from the beginning so that the same channel can be reused for dual and quad products.

## Reasons

- Lower development complexity than DC fast charging.
- Directly validates the Master/Channel architecture.
- Validates CP/PP, RFID, metering, local safety, communications and offline behaviour.
- Allows the VAZÃO EVSE TestStation to become a practical validation tool early.
- Provides a credible foundation for wallbox, pedestal and MultiStation products.

## Consequences

### Positive

- manageable prototype scope;
- reusable electronics;
- earlier software integration;
- lower capital requirement;
- simpler path to controlled laboratory testing.

### Negative

- does not validate DC power electronics;
- certification and metrology requirements remain substantial;
- final production hardware requires professional electrical and EMC engineering.

## Rejected approach

Starting with a 60–150 kW DC charger is rejected for V1 because it would consume capital and engineering effort before the core VAZÃO EVSE control/software architecture is proven.

## Next decision gates

1. Freeze electrical topology.
2. Select certified protection and measurement architecture.
3. Freeze controller interfaces.
4. Build low-voltage control prototype.
5. Build controlled mains/power prototype under qualified supervision.
6. Validate with VAZÃO EVSE TestStation.
7. Only then duplicate the channel into dual/quad products.
