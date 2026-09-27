# VAZÃO EVSE Charger Hardware V1 — Safety Chain

## Objective

The charger must remain safe when:
- the CPMS is unreachable;
- the local network is unavailable;
- the application is unavailable;
- a software service crashes;
- a communication module is removed;
- a measurement becomes invalid;
- an internal thermal or protective fault occurs.

## Safety ownership

### Hardware / dedicated EVSE interface
Responsible for:
- CP/PP electrical interface;
- contactor drive conditions;
- contactor feedback;
- protective input states;
- critical fault handling.

### MCU1
Responsible for:
- EVSE state machine;
- authorisation state;
- charging command;
- measurement acquisition;
- local logging;
- offline operation.

### CPMS
Responsible for:
- fleet management;
- commercial rules;
- remote commands;
- user/account context;
- reporting;
- configuration distribution.

The CPMS shall never be the sole mechanism preventing hazardous energisation.

## Contactor command policy

KM1 may close only when all required permissives are true, including:
1. EVSE self-test passed;
2. no critical protective fault;
3. valid vehicle state;
4. valid CP/PP interface state;
5. local charging authorisation;
6. valid measurement subsystem;
7. no emergency/maintenance lockout;
8. contactor feedback is consistent.

Any critical fault shall remove the contactor command.

## Feedback

The production design should verify the actual contactor state using auxiliary contacts or an equivalent safety-rated feedback mechanism.

A commanded-open / feedback-closed mismatch shall enter FAULT.

## Watchdog

MCU1 shall have an independent watchdog. A software lock-up must not leave the charging output commanded indefinitely.

The final hardware should also evaluate whether a hardware-level timeout / interlock is required for the chosen contactor and EVSE interface architecture.

## Communications failure

When CPMS connectivity is lost:
- an active session may continue under the locally stored policy, if safe and authorised;
- new sessions may be allowed only according to local offline policy;
- billing/event data shall be queued locally;
- critical safety events shall remain locally actionable;
- reconnection shall reconcile events idempotently.

## Important engineering gate

This document defines safety intent, not a certified functional-safety design. The final circuit must undergo electrical safety, EMC, insulation, thermal, fault-injection and compliance review before mains operation or production.
