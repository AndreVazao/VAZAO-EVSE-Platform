#!/usr/bin/env python3
"""Arithmetic guard for the provisional TMCS1123A1 -> THP210 -> ADS131M06 AFE study.

This validates transfer arithmetic and basic DC common-mode screening only. It
does not model FDA loop stability, input-pin differential voltage, power-off
fault currents, noise, thermal SOA, ADC settling, or electrical safety.
"""
from __future__ import annotations

import math

SENSITIVITY_V_PER_A = 0.025
SENSITIVITY_ERROR_FRACTION = 0.004
TARGET_PEAK_A = 70.0
SENSOR_ZERO_V = 2.5
SENSOR_LINEAR_PEAK_A = 96.0
ADC_AVDD_V = 3.3
ADC_PGA1_FSR_V = 1.2
ADC_OUTPUT_COMMON_MODE_V = 2.25
MAX_NOMINAL_ATTENUATION = 0.50


def main() -> int:
    if TARGET_PEAK_A >= SENSOR_LINEAR_PEAK_A:
        raise SystemExit("FAIL: target reaches/exceeds sensor nominal linear range")

    nominal_sensor_delta = TARGET_PEAK_A * SENSITIVITY_V_PER_A
    high_sensitivity = SENSITIVITY_V_PER_A * (1.0 + SENSITIVITY_ERROR_FRACTION)
    screened_sensor_delta = TARGET_PEAK_A * high_sensitivity

    sensor_low = SENSOR_ZERO_V - nominal_sensor_delta
    sensor_high = SENSOR_ZERO_V + nominal_sensor_delta
    if not (0.0 < sensor_low < SENSOR_ZERO_V < sensor_high < 5.0):
        raise SystemExit("FAIL: nominal sensor output screening is outside 0..5 V")

    adc_diff = screened_sensor_delta * MAX_NOMINAL_ATTENUATION
    adc_pin_high = ADC_OUTPUT_COMMON_MODE_V + adc_diff / 2.0
    adc_pin_low = ADC_OUTPUT_COMMON_MODE_V - adc_diff / 2.0
    differential_margin = ADC_PGA1_FSR_V - adc_diff

    if adc_diff >= ADC_PGA1_FSR_V:
        raise SystemExit("FAIL: differential signal exceeds PGA=1 FSR")
    if not (0.0 < adc_pin_low < adc_pin_high < ADC_AVDD_V):
        raise SystemExit("FAIL: ideal ADC pin voltages outside 0..AVDD")

    # THP210 at 5 V: specified input common-mode range is 1 V to 4 V.
    sensor_pair_cm_low = (sensor_low + SENSOR_ZERO_V) / 2.0
    sensor_pair_cm_high = (sensor_high + SENSOR_ZERO_V) / 2.0
    if not (1.0 < sensor_pair_cm_low <= sensor_pair_cm_high < 4.0):
        raise SystemExit("FAIL: TMCS VOUT/VREF pair common-mode outside THP210 5 V screening range")
    if not (1.0 < ADC_OUTPUT_COMMON_MODE_V < 4.0):
        raise SystemExit("FAIL: THP210 VOCM study target outside 1..4 V screening range")
    if differential_margin <= 0.0:
        raise SystemExit("FAIL: no differential headroom")

    print(f"Sensor nominal VOUT at ±{TARGET_PEAK_A:.1f} A: {sensor_low:.4f}..{sensor_high:.4f} V")
    print(f"Sensor differential nominal: ±{nominal_sensor_delta:.4f} V")
    print(f"Sensor differential sensitivity-only high-side screen: ±{screened_sensor_delta:.4f} V")
    print(f"AFE nominal attenuation target: {MAX_NOMINAL_ATTENUATION:.3f}")
    print(f"ADC differential screened magnitude: ±{adc_diff:.4f} V")
    print(f"TMCS pair common-mode screening: {sensor_pair_cm_low:.4f}..{sensor_pair_cm_high:.4f} V (THP210 1..4 V)")
    print(f"Ideal ADC pins around {ADC_OUTPUT_COMMON_MODE_V:.3f} V CM: {adc_pin_low:.4f}..{adc_pin_high:.4f} V")
    print(f"Remaining differential headroom to nominal ±{ADC_PGA1_FSR_V:.2f} V FSR: {differential_margin:.4f} V")
    print("PASS: DC arithmetic/common-mode screening only; THP210 loop, input-pin differential, power sequencing, filter, ADC timing, tolerances and safety remain unverified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
