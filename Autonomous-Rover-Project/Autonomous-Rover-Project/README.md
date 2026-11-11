# Autonomous Rover Project

A small six-wheel rocker-bogie rover inspired by NASA's Perseverance, built as a ground-up redesign of an earlier Arduino-based version. The aim is a ROS 2-capable platform with wheel odometry and onboard vision.

## Status

| Area | Status |
|---|---|
| Mechanical layout (Fusion 360 skeleton) | In progress |
| Rocker-bogie suspension | In progress |
| Drive electronics (breadboard) | Not started |
| Pico motor firmware | Not started |
| ROS 2 integration | Not started |
| Custom carrier PCB | Planned (phase 2) |

## Architecture

- **High level - Raspberry Pi 5:** ROS 2, camera, navigation, teleoperation over Wi-Fi
- **Low level - Raspberry Pi Pico (MicroPython):** motor PWM, encoder counting, battery monitoring
- **Link:** USB serial between Pi and Pico

## Key specification

| Parameter | Value |
|---|---|
| Footprint | ~260 x 265 mm |
| Suspension | Passive rocker-bogie with differential bar |
| Drive | 6x N20 12 V 200 RPM gearmotors with Hall encoders (1:150, 1050 PPR at output) |
| Steering | Skid steer (corner steering planned for a later revision) |
| Wheels | 60 mm diameter, 25 mm wide |
| Motor drivers | 3x TB6612FNG (one channel per motor) |
| Battery | 3S LiPo, 1500-2200 mAh |
| Pi supply | 3S to 5 V / 5 A buck converter |
| Camera | Raspberry Pi Camera Module 3 |
| Pivot bearings | 625ZZ on M5 axles |

## Repository layout

```
cad/        Fusion 360 exports (.f3d, .step) and scripts
  scripts/  Fusion API scripts (RoverSkeleton generates parameters and layout sketches)
firmware/   Pico MicroPython
ros2_ws/    ROS 2 packages
hardware/   KiCad projects, wiring diagrams
docs/       Build log, BOM, design decisions
```

## CAD workflow

The design is parametric. `cad/scripts/RoverSkeleton` creates the user parameters and reference layout sketches in Fusion 360. Part sketches are dimensioned with parameter expressions rather than projected from the skeleton, so the skeleton can be regenerated without breaking downstream features.
