EESchema Schematic File Version 4
LIBS:TS-V1-M2.9-F-MASTER-BASELINE-cache
EELAYER 29 0
EELAYER END
$Descr A4 11693 8268
Sheet 1 1
Title "VAZAO EVSE TestStation V1"
Date "2026-09-26"
Rev "M2.9-H"
Comp "VAZAO EVSE"
Comment1 "Connected-net and power baseline"
Comment2 "NO MAINS ENERGIZATION"
Comment3 "ERC/DRC pending"
Comment4 "M2.9-H"
$EndDescr
Text Notes 700 700 0 110 ~ 22
VAZAO EVSE TESTSTATION V1 — M2.9-H CONNECTIVITY BASELINE
Text Notes 700 1050 0 60 ~ 12
ZONE A/B measurement, isolated supplies, ADC SPI, MCU control, CAN isolation, CP/PP and safety nets.
Text Notes 900 1500 0 55 ~ 11
ZONE A VOLTAGE: A_L1_VP/A_L1_VN -> AMC1311-A1 -> ADC_A_CH0
Text Notes 900 1700 0 55 ~ 11
ZONE A VOLTAGE: A_L2_VP/A_L2_VN -> AMC1311-A2 -> ADC_A_CH1
Text Notes 900 1900 0 55 ~ 11
ZONE A VOLTAGE: A_L3_VP/A_L3_VN -> AMC1311-A3 -> ADC_A_CH2
Text Notes 900 2150 0 55 ~ 11
ZONE A CURRENT: A_L1_I/A_L2_I/A_L3_I -> TMCS1123-A1/A2/A3 -> ADC_A_CH3..CH5
Text Notes 900 2450 0 55 ~ 11
ZONE B VOLTAGE: B_L1/B_L2/B_L3 -> AMC1311-B1/B2/B3 -> ADC_B_CH0..CH2
Text Notes 900 2700 0 55 ~ 11
ZONE B CURRENT: B_L1_I/B_L2_I/B_L3_I -> TMCS1123-B1/B2/B3 -> ADC_B_CH3..CH5
Text Notes 900 3100 0 55 ~ 11
ISOLATION: 24V_SELV -> MEE1S2405SC x6 -> independent ISO_5V_x / ISO_GND_x
Text Notes 900 3350 0 55 ~ 11
ADC CONTROL: ADC_A/B SPI + DRDY + SYNC/RESET -> STM32G474
Text Notes 900 3600 0 55 ~ 11
CAN: STM32G474 -> ISO1044 -> CANH/CANL
Text Notes 900 3850 0 55 ~ 11
EV CONTROL: STM32G031 -> CP_PWM / CP_FB / PP_SENSE / contactor commands
Text Notes 900 4100 0 55 ~ 11
SAFETY: E-STOP -> independent energy removal + ESTOP_OK / K_MAIN_FB / K_LOAD_FB
Text Notes 900 4450 0 55 ~ 11
POWER: 24V input protection -> 24V distribution -> 3.3V measurement/control rails
Text Notes 900 4700 0 55 ~ 11
DECOUPLING: local ceramic bypass at every IC supply; final values follow exact manufacturer recommendations.
Text Notes 900 5200 0 65 ~ 13
M2.9-H STATUS: CONNECTIVITY CONTRACT — NOT ERC CLEAN — NOT DRC CLEAN — NOT FOR FABRICATION
$EndSCHEMATC
