# Bill of Materials

Status key: **Ordered**, **Planned**, **Have**, **Printed**

## Mechanical hardware

| Item | Qty | Use | Supplier | Price | Status |
|---|---|---|---|---|---|
| 625ZZ bearing, 5 x 16 x 5 mm (pack of 10) | 1 pack | Rocker and bogie pivots, differential bar | ManoMano | £9.99 | Ordered |
| M5 A2 socket cap kit (12/16/20/25 mm, nyloc + plain nuts, washers) | 1 kit | Pivot axles, brackets | Nuts of Chorley | £14.40 | Ordered |
| M5 x 30 mm A2 socket cap (20 pcs) | 1 pack | Bogie pivots (confirm length after bogie design) | TBC | TBC | Planned |

## Drive

| Item | Qty | Use | Supplier | Price | Status |
|---|---|---|---|---|---|
| N20 12 V 200 RPM gearmotor with Hall encoder (1:150) | 6 | Wheel drive + odometry | Waveshare | ~£5.18 each | Planned |
| TB6612FNG dual motor driver | 3 | One channel per motor | TBC | TBC | Planned |

## Electronics and power

| Item | Qty | Use | Supplier | Price | Status |
|---|---|---|---|---|---|
| Raspberry Pi 5 (4 GB) | 1 | ROS 2, vision, navigation | TBC | ~£54 | Planned |
| Raspberry Pi Camera Module 3 | 1 | Vision | TBC | ~£24 | Planned |
| Raspberry Pi Pico | 1 | Motor PWM, encoders, battery monitoring | TBC | TBC | Planned |
| 3S LiPo, 1500-2200 mAh | 1 | Main battery | TBC | TBC | Planned |
| 3S to 5 V / 5 A buck converter | 1 | Pi 5 supply | TBC | TBC | Planned |

## Printed parts

| Part | Qty | Material | Status |
|---|---|---|---|
| Bearing fit test block | 1 | PLA | Designed, awaiting printer induction |
| Rocker_L | 1 | PLA (PETG if available) | Designed |
| Rocker_R | 1 | PLA (PETG if available) | Designed |
| Pivot spacers (5.5 ID x 7.5 OD) | ~8 | PLA | Planned |

Print settings for structural parts: 0.4 mm nozzle, 0.2 mm layers, 4 walls, 30-40% infill. Bearing seat and bolt hole fits set by `fit_seat` and `fit_clear` after the test print.
