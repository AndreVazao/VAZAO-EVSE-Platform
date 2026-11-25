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
- `XF` — incoming feeder terminal/assembly
- `XD` — downstream distribution terminal/assembly

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

## 4. Dual/quad feeder and branch schedule — design inputs only

The following rows define the circuits that must exist in the engineering schedule. They do not assign cable sections, protective-device ratings or terminal numbers.

| ID | From | To | Function / design rule |
|---|---|---|---|
| F-001 | Site distribution board | XF-A | Independent feeder for output A |
| F-002 | Site distribution board | XF-B | Independent feeder for output B, when independent topology is selected |
| F-003 | Site distribution board | XF-C | Independent feeder for output C, quad variant only |
| F-004 | Site distribution board | XF-D | Independent feeder for output D, quad variant only |
| F-005 | Site distribution board | XF-MAIN | One common incoming feeder for local distribution topology |
| F-006 | XF-MAIN | XD-A | Protected branch feeder to output A |
| F-007 | XF-MAIN | XD-B | Protected branch feeder to output B |
| F-008 | XF-MAIN | XD-C | Protected branch feeder to output C, quad variant only |
| F-009 | XF-MAIN | XD-D | Protected branch feeder to output D, quad variant only |
| F-010 | Load-management controller / current sensors | Master power-limit input | Enforce configured aggregate limit locally; define fail-safe/default state |

### 4.1 Required cable schedule fields

Every feeder and branch entry must contain: circuit ID, origin/destination, number of phases and conductors, conductor material, insulation, cross-section in mm², route length, installation method, ambient/soil temperature, grouping/derating, design current, protective device, voltage-drop result, short-circuit/adiabatic result, PE/neutral sizing basis, terminal/gland range, calculation reference, reviewer and approval state.

### 4.2 Explicit dual/quad alternatives

- **Independent:** dual = two separately calculated input feeders; quad = four separately calculated input feeders. Each output branch remains individually protected as required.
- **Common:** dual = one common feeder plus two protected branches; quad = one common feeder plus four protected branches. The trunk is calculated for aggregate demand; branches are calculated for their own channel demand.
- The common feeder may be sized against a reduced managed demand only when the local power-limit function, measurement path, watchdog, failure response and commissioning proof are documented. Otherwise use the maximum simultaneous load envelope.
- The schedule must never infer the common-feeder section by multiplying or copying a single-output cable section. Full installation calculation is mandatory.

## 5. Quad expansion

For channels B–D, repeat the channel-specific elements:

- contactor;
- measurement;
- Type 2 CP/PP interface;
- temperature monitoring;
- local safety state;
- output protection as required.

The Master Controller communicates with each channel controller and applies the site power budget.

## 6. Commissioning checks

Before energization, the approved test procedure shall verify continuity, PE integrity, insulation, protective-device operation, contactor operation, CP/PP state transitions, metering, emergency/fault behaviour and communication loss.


## 7. Local load-management signal schedule — M1.24

| ID | From | To | Function / required evidence |
|---|---|---|---|
| LM-001 | Common-feeder phase sensors / meter | Local energy manager | Measure each relevant phase current; verify accuracy, range, polarity and fault diagnostics |
| LM-002 | Independent-feeder sensors / meters (where used) | Local energy manager | Measure per-feeder current where the installation design requires it |
| LM-003 | Local energy manager | Output channel A controller | Send permitted current budget over a validated local interface |
| LM-004 | Local energy manager | Output channel B controller | Send permitted current budget over a validated local interface |
| LM-005 | Local energy manager | Output channels C/D controllers | Repeat for quad variant |
| LM-006 | Output channel controllers | Local energy manager | Return accepted setpoint, actual current, state and fault status |
| LM-007 | Local energy manager watchdog / fault logic | Channel controllers or local inhibit chain | Apply the documented fallback when measurement, control or communications are invalid |

The schedule is functional only. No protocol, terminal, voltage level or device compatibility is assumed. Each selected controller must prove how a current limit is accepted, enforced and acknowledged. If the controller cannot provide this interface, a different controller or an independently validated local control layer is required.
