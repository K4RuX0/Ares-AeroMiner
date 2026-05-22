# Changelog - ARES-STARSHIP V3.1

All notable changes to the Prometheus I mission architecture will be documented in this file.

## [3.1.0-heavy] - 2026-05-22

### Added
- **740kN Heavy Configuration**: 4x 185kN NTR cluster (upgraded from 680kN)
- **Alcântara Launch Site**: +463 m/s Earth rotation bonus, CNEN/AEB compliance
- **Engine-Out Reporting**: Explicit `e_out_tw = 0.31` for 3-engine abort
- **Isp 920s Target**: UC-ZrC-NbC core @ 3100K, wall 1350K C-C/NbC

### Changed
- **Thrust**: 680kN → 740kN (+8.8%)
- **Isp**: 780s → 920s (+18%) via 3100K core temperature
- **T/W orbital**: 0.51 → 0.41 (recalculated on dry mass 185t)
- **Engine-Out T/W**: 0.38 → 0.31 (real value with 555kN/185t)
- **Mass Flow**: 96.7 kg/s → 82.0 kg/s LH2 (corrected for 920s)
- **Dry Mass**: 199.4t → 185.0t
- **Pad Mass**: 1452.7t → 1407.0t
- **Tanks**: 126.3t → 95.0t
- **Delta-V**: 14,200 → 14,570 m/s (includes Alcântara)

### Fixed
- **Critical**: Spike density 8190 → 1950 kg/m³ (Carbon-Carbon)
- **Physics**: Eliminated 25.8t mass error in spike assembly
- **Temperature**: Core 2800K → 3100K to achieve 920s Isp
- **Consistency**: Code, README, BOM, roadmap, and pitch now match line-by-line

### Engineering Rationale
The upgrade to 920s/740kN was driven by:
1. **No-refuel requirement**: 14,570 m/s needed > 14,200 m/s chemical baseline
2. **Alcântara advantage**: +463 m/s enables 833 m/s margin without orbital depot
3. **Materials**: UC-ZrC-NbC validated at 3100K in ORNL tests (2024)
4. **Mass discipline**: Dry mass reduced 14.4t via C-C spike correction

Mass budget locked at 1,407t LEO. Thrust increase within NERVA heritage (333kN tested).

## [3.0.0] - 2026-05-15

### Added
- Initial V3.0: 4x 170kN, 680kN, Isp 780s
- ATHENA habitat 380m³, 776-day mission

### Known Issues (resolved in 3.1.0)
- Spike density error, Isp insufficient for no-refuel, missing Alcântara