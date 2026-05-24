    def generate_all_files(self):
        wall_t, spike_m, real_isp, thrust_n, tc_k, power_w = self.calculate_stp_aerospike_physics(distance_au=1.0)
        
        lunar_fuel_kg, lunar_margin_kg, lunar_ok = self.evaluate_rocket_equation(self.LUNAR_PAYLOAD, self.LUNAR_DELTA_V_REAL, real_isp)
        mars_fuel_kg, mars_margin_kg, mars_ok = self.evaluate_rocket_equation(self.MARS_PAYLOAD, self.MARS_DELTA_V_REAL, real_isp)
        
        lch4_volume_m3 = self.TOTAL_PROPELLANT / self.METHANE_DENSITY
        tank_length = lch4_volume_m3 / (math.pi * 4.5**2)
        total_height = 4.5 + tank_length + 12.0
        orbital_tw = thrust_n / (self.dry_mass * self.G0)
        engine_out_tw = (thrust_n / 2) / (self.dry_mass * self.G0) 

        # === FILE GENERATION 01: BILL OF MATERIALS (BOM) ===
        bom_items = [
            ["System", "Item", "Spec", "Mass_kg", "USD", "TRL_2030"],
            ["Propulsion", "Aerospike Chamber Expansion Line", f"{wall_t*1000:.1f}mm Ta4HfC5 Matrix x2", int(spike_m*0.3), 2500000, 7],
            ["Propulsion", "Inner Engine Iridium Film Coating", "Anti-corrosive chemical barrier", 150, 4500000, 8],
            ["Propulsion", "Inflatable Parabolic Mirror Array", "1250m2 Mylar Coated x2 Units", 1200, 3100000, 7],
            ["Propulsion", "LCH4 Turbopumps High-Density Array", "15.0 kg/s flow operational", 3500, 7000000, 8],
            ["Structure", "LCH4 Cryogenic Tank Al-Li (9m)", f"9mD x {tank_length:.1f}mH Heavy Duty", int(self.tanks_mass), 6500000, 9],
            ["Structure", "ATHENA Habitat Core Module", f"{self.HABITAT_VOL}m3 Internal Vol", 10000, 15000000, 8],
            ["Thermal", "Active ZBO Pulse Tube Cryocoolers", "2.5 kW Active Helium Loop Array", 1800, 3800000, 7],
            ["Thermal", "MLI + Silica Aerogel Insulation Shield", "0.001 Transmittance Factor Matrix", 2200, 1200000, 9],
            ["EHS", "ECLSS Regenerative Closed-Loop", "90% Water & Oxygen Recycling", 4500, 12000000, 7],
            ["Avionics", "ODIN AI Navigation & Autonomous Core", "Radiation Hardened Avionics Architecture", 1500, 2100000, 8]
        ]
        
        total_cost = sum([int(row[4]) for row in bom_items[1:]])
        bom_data = bom_items + [["TOTAL", "COMPLETE VEHICLE V4.0", "STP METHANE CONFIG", int(self.dry_mass), total_cost, ""]]

        try:
            with open("01_BOM_STARSHIP_V3.1.csv", "w", newline='') as file_bom:
                csv.writer(file_bom).writerows(bom_data)

            # === FILE GENERATION 02: MASS BREAKDOWN REPORT ===
            lunar_zbo_kwh, lunar_zbo_kw = self.calculate_zbo_thermal_leak(self.LUNAR_DAYS, distance_au=1.0)
            mars_zbo_kwh, mars_zbo_kw = self.calculate_zbo_thermal_leak(self.MARS_DAYS, distance_au=1.2) 

            mass_report = f"""ARES-SPACE TRANSPORT V4.0 - REALISTIC EXECUTION DESIGN - TARGET 2030
PROPULSION CONFIGURATION: SOLAR THERMAL PROPULSION (STP) VIA INFLATABLE CONCENTRATORS
INDUSTRIAL SYNC: ANTICORROSIVE IRIDIUM COATING & ACTIVE ZERO BOIL-OFF SYSTEM

LAUNCH SITE INTERFACE: {self.LAUNCH_SITE}
LAUNCHPAD INJECTION CAPACITY (LEO TOTAL): {self.launchpad_total_mass/1000:.1f} t
Airframe Dry Mass: {self.dry_mass/1000:.1f} t
Optimized Liquid Methane Mass (LCH4): {self.TOTAL_PROPELLANT/1000:.1f} t
Al-Li Cryogenic Shell Tank Mass: {self.tanks_mass/1000:.1f} t
Thrust-to-Weight Ratio (LEO Orbital T/W): {orbital_tw:.2f}
Cluster Redundancy Profile (Engine-Out T/W - 1/2 Active): {engine_out_tw:.2f}
Total Calculated Vehicle Structural Height: {total_height:.1f} m
Required Internal Tank Core Volume: {lch4_volume_m3:.1f} m3

------------------------------------------------------------------------
SOLAR THERMAL EXPANSION ENGINE PRODUCT SPECIFICATIONS
------------------------------------------------------------------------
Active Expanding Nozzles: {self.ENGINE_COUNT}x STP Linear Aerospike Arrays
Combined Gross Thrust (LEO Core): {thrust_n/1000:.1f} kN
Calculated Vacuum Specific Impulse (Isp): {real_isp:.1f} s
Expansion Chamber Working Temperature: {tc_k:.1f} K
Net Absorbed Solar Thermal Power Core: {power_w/1e6:.2f} MW
Chemical Wall Shielding: {self.CHAMBER_COATING}

------------------------------------------------------------------------
PHASE I: LUNAR MISSION LOGISTICS (AUTONOMOUS CISLUNAR ROUND-TRIP)
------------------------------------------------------------------------
Allocated Delivery Payload (Lunar Payload): {self.LUNAR_PAYLOAD/1000:.1f} t
Required Kinetic Delta-V (With Gravity Losses): {self.LUNAR_DELTA_V_REAL} m/s
Computed Liquid Methane Consumption Fleet: {lunar_fuel_kg/1000:.1f} t
Remaining Fuel Tank Margin Overhead: {lunar_margin_kg/1000:.1f} t
Active Thermal Fuel Preservation (ZBO): {lunar_zbo_kw:.2f} kWe Steady
Total Lunar Cooling Mission Power Consumption: {lunar_zbo_kwh:.1f} kWh
PHASE I KINETIC CLOSURE VIABILITY: {"APPROVED FOR FLIGHT" if lunar_ok else "REJECTED - MASS OVERFLOW"}

------------------------------------------------------------------------
PHASE II: INTERPLANETARY MISSION PROMETHEUS I (DEEP-SPACE MARS TRANSIT)
------------------------------------------------------------------------
Trans-Mars Injection Payload (TMI Payload): {self.MARS_PAYLOAD/1000:.1f} t
Required LEO Escape Maneuver Delta-V: {self.MARS_DELTA_V_REAL} m/s
Escape Burn Methane Mass Consumption: {mars_fuel_kg/1000:.1f} t
Retained Mars Injection Fuel Safeguard: {mars_margin_kg/1000:.1f} t
Active Transit Thermal Fuel Preservation (ZBO): {mars_zbo_kw:.2f} kWe
Total Interplanetary Journey ZBO Power Draw: {mars_zbo_kwh:.1f} kWh
PHASE II KINETIC CLOSURE VIABILITY: {"APPROVED FOR FLIGHT" if mars_ok else "REJECTED - MASS OVERFLOW"}

Structural Configuration Coefficients:
- Propellant Mass Fraction Over Gross Weight: {self.TOTAL_PROPELLANT/self.launchpad_total_mass*100:.1f}%
- Insulation Thermal Matrix Density: Silica Aerogel Integrated Multi-Layer Shield
- ATHENA Onboard Human Habitable Volume: {self.HABITAT_VOL} m3
"""
            with open("02_MASS_BREAKDOWN_V3.1.txt", "w") as file_mass:
                file_mass.write(mass_report)

            # === GENERATION: FILE 03 - INVESTOR PITCH (ONE-PAGER) ===
            pitch = f"""ARES-SPACE TRANSPORT V4.0 - INVESTOR ONE PAGER - TARGET 2030

Problem: Heavy cislunar and interplanetary transport using traditional chemical propulsion 
forces massive, inefficient propellant-depot architectures. Fission alternatives meet absolute 
geopolitical, regulatory, and financial barriers that stall execution timelines.

Solution: A Reusable Deep-Space Cargo Freighter powered by Solar Thermal Propulsion (STP) and Liquid Methane. 
Drastically drops refueling launch chains, operating clean from Alcantara Space Center, Brazil.

Technical Competitive Edge (Challenging Aerospace Giants by 2030):
- Low CAPEX Framework: Zero radioactive containment requirements or nuclear handling overheads.
- Anti-Corrosive Barrier: Atomic Iridium layer bonded over Ta4HfC5 ceramic grants instant engine reusability.
- Zero Fuel Waste: High-TRL Active Zero Boil-Off (ZBO) mechanical cryocoolers preserve propellant mass indefinitely.
- Verified Kinetics: Delivers a real {real_isp:.1f}s specific impulse with a {thrust_n/1000:.1f} kN LEO core burn.
- Versatile Revenue Generation: Single modular design executing two high-yield milestones:
  * Phase I (Moon Market): Delivers {self.LUNAR_PAYLOAD/1000:.0f}t of net payload and returns to LEO on a zero-refuel round-trip.
  * Phase II (Mars Market): Stabilizes a high-energy Trans-Mars Injection delivering {self.MARS_PAYLOAD/1000:.0f}t payload.

Financial & Operating Modeling:
- Projected Vehicle Unit Production Cost: \${total_cost/1e6:.1f}M
- Regulatory Profiling: 100% radiation-free lifecycle, fast-tracking environmental approvals.

Funding Request: Seed round to finalize and space-test a vacuum deployment TRL-7 inflatable mirror demonstrator.
Systems Engineering Direct Contact: ranyellson@gmail.com"""
            with open("03_INVESTOR_PITCH_V3.1.txt", "w") as file_pitch:
                file_pitch.write(pitch)

            print("========================================================================")
            print("ARES-SPACE TRANSPORT V4.0 - AUTOMATED GENERATOR COMPLETE")
            print("========================================================================")
            print(f"1. BOM COMPILATION SUCCESS (01_BOM_STARSHIP_V3.1.csv): \${total_cost/1e6:.1f}M")
            print(f"2. SYSTEMS MASS REPORT SUCCESS (02_MASS_BREAKDOWN_V3.1.txt): {real_isp:.1f}s Isp")
            print(f"3. EXECUTIVE INVESTOR PITCH SUCCESS (03_INVESTOR_PITCH_V3.1.txt): Synced")
            print("========================================================================")
        except IOError as e:
            print(f"Critical I/O error writing mission files: {e}")

if __name__ == "__main__":
    AresSpaceTransportV4().generate_all_files()
