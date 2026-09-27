# VAZÃO EVSE Charger Hardware V1 — Terminal and Wiring Schedule

**Status:** engineering interface schedule; not an installation certificate.

## Main interfaces

| Interface | From | To | Signal / purpose |
|---|---|---|---|
| X-T1 | installation | QF1 | L1/L2/L3/N/PE |
| X-T2 | QF1/RCD1 | TB1 | protected supply |
| X-T3 | TB1 | PS1 | auxiliary supply |
| X-T4 | TB1 | KM1 | EV power path |
| X-T5 | KM1/EM1 | X1 | Type 2 power |
| X-C1 | PS1 | MCU1 | low-voltage power |
| X-C2 | MCU1 | EVSE1 | CP/PP control interface |
| X-C3 | MCU1 | KM1 driver | contactor command |
| X-C4 | KM1 | MCU1 | contactor feedback |
| X-C5 | EM1 | MCU1 | metering data |
| X-C6 | MCU1 | COM1 | local communications |
| X-C7 | MCU1 | RFID1 | user identification |
| X-C8 | MCU1 | HMI1 | status / user feedback |
| X-P1 | PE bar | chassis | protective bonding |
| X-P2 | PE bar | X1 | Type 2 protective earth |

## Wiring policy

Final wire cross-sections, insulation systems, terminal ratings, ferrules, torque values, short-circuit withstand and routing shall be selected from the final component datasheets and installation design.

Do not treat this schedule as permission to energise a prototype.

## Expansion to two/four outputs

The common architecture shall be replicated per charging point:
- one dedicated EVSE interface;
- one charging-output switching path;
- one metering channel/subsystem as required;
- one connector interface;
- independent local state and fault handling.

A park-level Master Controller may coordinate current allocation between channels, but each EVSE channel retains local safety authority.
