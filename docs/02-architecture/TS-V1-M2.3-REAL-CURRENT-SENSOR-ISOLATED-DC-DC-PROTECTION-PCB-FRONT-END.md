

## 24. 2026-11-13 correction — current-sensor thermal rating is not measurement range

The earlier statements in Sections 2.2 and 2.3 that the 80 A RMS family capability makes 32 A comfortably measurable are incomplete and must not be used to approve the selected sensitivity variant. The 80 A RMS figure is a current-path/thermal capability under specified conditions; it is not the sensor's linear analogue measurement range.

The exact BOM item at the time of correction is TMCS1123A3AQDVGR (75 mV/A). TI specifies only ±32 A instantaneous linear range at 5 V and an asymmetric −32 A to +9.3 A range at 3.3 V. A 32 A RMS sinusoidal current reaches 45.25 A peak. Therefore the A3 variant does not meet the existing 32 A RMS sinusoidal measurement requirement in its linear range.

The project has opened a review-only design-envelope proposal:
`hardware/teststation/V1/CAD/review/physical-symbol-migration/M2.9-K-CURRENT-CHANNEL-DESIGN-ENVELOPE-PROPOSAL-2026-11-13.md`.

That proposal uses ±70 A instantaneous measurement as a provisional target and identifies TMCS1123A1AQDVGR at 5 V as the preferred candidate for the next analogue-front-end study. It does not select or authorize a BOM substitution. The 40 A RMS/10 s and 48 A RMS/1 s values are analysis scenarios only; no thermal safe-operating-area or overload withstand has been established. The ADS131M06 interface must include designed attenuation and common-mode translation; direct A1 output connection to the 3.3 V ADC is not approved.

This correction supersedes the earlier implication that 32 A was automatically inside the measurement envelope because of the family 80 A RMS rating. No production schematic, BOM, wiring, PCB or firmware was changed. No fabrication, energization or overload testing is authorized by this document.
