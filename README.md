# ARES-AEROMINER TRANSPORT — Project Prometheus I




| 📦 Technology | 📜 License | ⚙️ Status | 📍 Launch Site |
| :---: | :---: | :---: | :---: |
| **Python 3.10+** | **MIT License** | **Conceptual Design** | **Alcantara, Brazil** |

---

**ARES V4.0** is an open-source conceptual architecture and numerical simulation suite for a high-efficiency, reusable deep-space cargo freighter. Originally engineered with nuclear propulsion, the design has been fully upgraded to Version 4.0 to meet commercial viability, fast-track regulatory clearance, and sustainability targets for the **2030** flight window.

The spacecraft operates across a standardized two-stage mission roadmap: **Phase I (Lunar Mission)**, validating cislunar logistics on an autonomous round-trip profile, and **Phase II (Mars Mission - Project Prometheus I)**, executing high-energy interplanetary transport. The vehicle launches and refuels at the **Alcantara Space Center (CLA), Brazil**.

---

## 🚀 Version 4.0 Technical Innovations

To maximize cost-effectiveness and eliminate the core engineering bottlenecks of previous iterations, the V4.0 architecture implements four foundational pillars:

1. **Solar Thermal Propulsion (STP):** Complete replacement of heavy nuclear reactors with high-precision inflatable parabolic concentrators. The system captures raw solar flux to superheat the propellant, generating a real vacuum specific impulse ($I_{sp}$) of **620 seconds** without radiological safety liabilities or massive radiation shielding weight penalties.
2. **Liquid Methane ($LCH_4$) Migration:** Propellant optimized from molecular hydrogen to high-density liquid methane (422.6 kg/m³). This drastically reduced tank volume inside the 9-meter diameter hull—stabilizing total vehicle height at **49.3 meters**—while securing cheap fuel procurement and enabling future Mars atmospheric ISRU (Sabatier Reaction).
3. **Zero-Corrosion Core (Target 2030):** The thermal absorption and expansion chamber utilizes a refractory **Tantalum-Hafnium Carbide ($Ta_4HfC_5$)** ceramic matrix lined with an atomic thin-film of **Iridium**. This completely eliminates fuel-induced oxidation and chemical erosion under 3200 K operating conditions.
4. **Active Zero Boil-Off (ZBO) Technology:** To halt cryo-fuel evaporation over deep-space transits, the hull integrates 60-layer Multi-Layer Insulation (MLI) coupled with active **Pulse Tube Cryocoolers**. The closed-loop helium system draws a steady 2.5 kWe to maintain methane liquified indefinitely.
---

## 📐 Technical Specifications & Mass Budget




| Parameter | Nominal Value (V4.0) | Engineering Rationale |
| :--- | :--- | :--- |
| **Total Height** | 49.3 meters | Compacted airframe optimized for liquid methane density. |
| **Fuselage Diameter** | 9.0 meters | Maintained compatibility with heavy-lift booster interfaces. |
| **Ship Dry Mass** | 120.0 metric tons | Alleviated mass distribution; completely free of nuclear shielding. |
| **Max Propellant Mass ($LCH_4$)** | 1130.0 metric tons | Maximum volumetric capacity of the primary cryogenic tank shell. |
| **Engine Configuration** | 2x STP Aerospike Units | 1/2 dynamic cluster redundancy yielding 185 kN per nozzle. |
| **Total Vacuum Thrust (LEO)** | 370 kN ($2 \times 185 \text{ kN}$) | Combined engine output calibrated for 1.0 AU solar flux. |
| **Payload Capacity (Phase I - Moon)**| **55.0 metric tons** | Cislunar round-trip margin without refueling depots. |
| **Payload Capacity (Phase II - Mars)**| **71.0 metric tons** | Pure payload injection toward Mars via high-energy LEO escape. |

---

## 📂 Simulation Code Architecture

The repository is 100% modular, written in Python to validate and optimize kinetic orbital parameters:

*   **`propulsion_system.py`**: Models real STP aerospike physics via isentropic gas equations, tracking vector thrust and dynamic solar flux decay based on distance from the Sun.
*   **`thermal_management.py`**: Governs cryogenic storage thermodynamics, monitoring active ZBO power draw against MLI transmittance.
*   **`trajectory_solver.py`**: Processes numerical Tsiolkovsky rocket equations, calculating mass fractions and mission viability for both Lunar and Mars trajectories independently.

---

## 🛠️ Running the Simulation Suite

Ensure you have Python 3.10+ installed on your local terminal. Clone the repository and execute the main mission runner:

```bash
# Run the integrated V4.0 systems simulation
python main.py
```

---

## 🗺️ Systems Engineering Roadmap (Target 2030)

- [x] Propulsion Matrix Pivot (Nuclear Fission → Green Solar Thermal Expansion)
- [x] Volumetric Tank Optimization & Flight Stabilization for Liquid Methane
- [x] Numerical Modeling of Active Cryogenic Zero Boil-Off (ZBO) Systems
- [ ] Integration of the **ODIN** Flight Computer Onboard Electrical Power Subsystem (EPS)
- [ ] Fine Aerodynamic Simulation of Aerocapture Entry Trajectories for Earth and Mars Atmospheric Interfaces
