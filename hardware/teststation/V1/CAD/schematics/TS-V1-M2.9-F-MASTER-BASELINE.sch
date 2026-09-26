EESchema Schematic File Version 4
LIBS:power
LIBS:device
LIBS:Connector_Generic
LIBS:MCU_ST_STM32G4
LIBS:Interface_CAN_LIN
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
Sheet 1 8
Title "VAZAO EVSE TestStation V1"
Date "2026-09-26"
Rev "M2.9-F"
Comp "VAZAO EVSE"
Comment1 "Engineering prototype schematic baseline"
Comment2 "NO MAINS ENERGIZATION"
Comment3 "Derived netlist must be reviewed before PCB update"
Comment4 "M2.9-F"
$EndDescr
Text Notes 800 900 0 120 ~ 24
VAZAO EVSE TESTSTATION V1 — MASTER SCHEMATIC BASELINE
Text Notes 800 1200 0 70 ~ 12
M2.9-F: functional electrical hierarchy; exact manufacturer symbols/pin assignments remain under controlled verification.
Text Notes 800 1600 0 70 ~ 12
ZONE A: L1/L2/L3 voltage + current measurement
Text Notes 800 1850 0 70 ~ 12
ZONE B: L1/L2/L3 voltage + current measurement
Text Notes 800 2100 0 70 ~ 12
MEASUREMENT: 6 isolated voltage channels + 6 current channels + synchronized ADCs
Text Notes 800 2350 0 70 ~ 12
CONTROL: STM32G474 + safety STM32G031 + CAN isolation
Text Notes 800 2600 0 70 ~ 12
EV INTERFACE: IEC 61851 CP/PP, contactor control, safety feedback
Text Notes 800 2850 0 70 ~ 12
POWER: 24 V SELV distribution; independent isolated 5 V supplies for AMC1311 channels
Text Notes 800 3400 0 70 ~ 12
NET HIERARCHY
Text Notes 1000 3700 0 60 ~ 12
A_L1_VP / A_L1_VN -> AMC1311B-A1 -> ADC_A_CH0
Text Notes 1000 3900 0 60 ~ 12
A_L2_VP / A_L2_VN -> AMC1311B-A2 -> ADC_A_CH1
Text Notes 1000 4100 0 60 ~ 12
A_L3_VP / A_L3_VN -> AMC1311B-A3 -> ADC_A_CH2
Text Notes 1000 4300 0 60 ~ 12
A_L1_I / A_L2_I / A_L3_I -> TMCS1123 x3 -> ADC_A_CH3..CH5
Text Notes 1000 4600 0 60 ~ 12
B_L1_VP / B_L1_VN -> AMC1311B-B1 -> ADC_B_CH0
Text Notes 1000 4800 0 60 ~ 12
B_L2_VP / B_L2_VN -> AMC1311B-B2 -> ADC_B_CH1
Text Notes 1000 5000 0 60 ~ 12
B_L3_VP / B_L3_VN -> AMC1311B-B3 -> ADC_B_CH2
Text Notes 1000 5200 0 60 ~ 12
B_L1_I / B_L2_I / B_L3_I -> TMCS1123 x3 -> ADC_B_CH3..CH5
Text Notes 1000 5550 0 60 ~ 12
ADC_A / ADC_B -> SPI -> STM32G474
Text Notes 1000 5750 0 60 ~ 12
STM32G474 -> ISO1044 -> CAN SERVICE
Text Notes 1000 5950 0 60 ~ 12
STM32G031 -> CP PWM / CP feedback / PP sense / safety
Text Notes 1000 6150 0 60 ~ 12
Safety -> E-STOP / K_MAIN_FB / K_LOAD_FB / watchdog
Text Notes 800 6700 0 80 ~ 16
STATUS: FUNCTIONAL BASELINE ONLY — NOT ERC/DRC — NOT FOR FABRICATION
$EndSCHEMATC
