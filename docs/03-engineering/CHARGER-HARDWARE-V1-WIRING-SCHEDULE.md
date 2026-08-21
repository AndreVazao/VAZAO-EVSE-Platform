# VAZÃO EVSE Charger Hardware V1 — Wiring Schedule

## 1. Naming convention

- `X` — terminal/connectivity point
- `QF` — protective/isolation device
- `FI` — residual-current protection/monitoring function
- `SPD` — surge protective device
- `PS` — power supply
- `KM` — power contactor
- `M` — energy/current measurement
- `MCU` — EVSE control MCU
- `CPU` — application/communications processor
- `RFID` — RFID/NFC reader
- `T` — temperature sensor
- `J` — connector/interface

## 2. Functional wiring schedule

| ID | From | To | Function |
|---|---|---|---|
| W-001 | X1 | QF1 | protected mains input path |
| W-002 | QF1 | FI/EV protection | residual-current protection path |
| W-003 | protection stage | distribution | protected AC distribution |
| W-004 | distribution | PS1 | auxiliary AC supply |
| W-005 | distribution | KM1 | EV power feed |
| W-006 | KM1 | M1 | metered EV power path |
| W-007 | M1 | J1 Type 2 | EV power output |
| W-008 | PE terminal | enclosure | protective bonding |
| W-009 | PE terminal | J1 Type 2 PE | protective earth |
| W-010 | PS1 | MCU/CPU | SELV control power |
| W-011 | MCU | KM1 driver | contactor command |
| W-012 | KM1 aux | MCU | contactor feedback |
| W-013 | J1 CP/PP | EVSE CP/PP interface | pilot/proximity interface |
| W-014 | M1 communication | MCU/CPU | energy measurement data |
| W-015 | RFID | CPU/MCU | authentication data |
| W-016 | CPU | Ethernet/LTE/Wi-Fi | external communications |
| W-017 | T1/T2 | MCU | thermal monitoring |

## 3. Important implementation rule

The table is a **functional wiring schedule**, not a terminal-by-terminal release drawing. Final conductor cross-sections, protective-device ratings, terminal numbers, ferrules, insulation levels, clearances and creepage distances must be released from the final schematic and installation calculation.

## 4. Quad expansion

For channels B–D, repeat the channel-specific elements:

- contactor;
- measurement;
- Type 2 CP/PP interface;
- temperature monitoring;
- local safety state;
- output protection as required.

The Master Controller communicates with each channel controller and applies the site power budget.

## 5. Commissioning checks

Before energization, the approved test procedure shall verify continuity, PE integrity, insulation, protective-device operation, contactor operation, CP/PP state transitions, metering, emergency/fault behaviour and communication loss.
