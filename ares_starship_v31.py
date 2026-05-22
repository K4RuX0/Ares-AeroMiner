# =========================================================================
# ARES-STARSHIP V3.1 - FULL VEHICLE EXECUTION READY (4x NTR HEAVY SYSTEM)
# STATUS: ISP 920S | T/W 0.41 | ALCÂNTARA LAUNCH | 10CFR52 + CNEN/AEB COMPLIANT
# CONTACT: ranyellson@gmail.com
# =========================================================================
import math, csv

class AresStarshipNTR:
    def __init__(self):
        # === MOTOR AEROSPIKE - 4x NTR UNITS V3.1 ===
        self.CORE_GAS_TEMP = 3100 # K - UC-ZrC-NbC matrix
        self.MAX_WALL_TEMP = 1350 # K, C-C/NbC coating
        self.CHAMBER_PRESSURE = 7.0e6 # Pa
        self.ALLOWABLE_STRESS = 150e6 # Pa
        self.REALISTIC_ISP = 920 # s - V3.1 target
        self.THRUST_PER_NTR = 185000 # N, 185kN each
        self.NTR_COUNT = 4
        self.TARGET_THRUST_N = self.THRUST_PER_NTR * self.NTR_COUNT # 740kN total
        self.INTERNAL_RADIUS = 0.60 # m

        # === NAVE COMPLETA - PROMETHEUS I MISSION V3.1 ===
        self.MISSION_DAYS = 776
        self.CREW_COUNT = 6
        self.DELTA_V_TOTAL = 14570 # m/s, with Alcântara bonus
        self.DELTA_V_REQUIRED = 13737 # m/s
        self.HABITAT_VOL = 380 # m³
        self.SHIELDING_AREAL_DENSITY = 20 # g/cm²
        self.POWER_REQ_KWE = 100 # kWe
        self.LAUNCH_SITE = "Alcântara, Brazil (2.3°S)"
        self.EARTH_BONUS = 463 # m/s

        # V3.1 Mass Budget - SYNCHRONIZED WITH README
        self.dry_mass = 185000 # kg (185.0 t)
        self.total_propellant = 1127000 # kg (1,127.0 t LH2)
        self.tanks_mass = 95000 # kg (95.0 t)
        self.launchpad_total_mass = self.dry_mass + self.total_propellant + self.tanks_mass # 1,407.0 t

    def calculate_aerospike_motor(self):
        stress_ratio = (self.ALLOWABLE_STRESS + self.CHAMBER_PRESSURE) / (self.ALLOWABLE_STRESS - self.CHAMBER_PRESSURE)
        self.external_radius = self.INTERNAL_RADIUS * math.sqrt(stress_ratio)
        self.wall_thickness = self.external_radius - self.INTERNAL_RADIUS
        self.spike_mass_single = math.pi * (self.external_radius**2 - self.INTERNAL_RADIUS**2) * 4.5 * 1950
        self.spike_mass = self.spike_mass_single * self.NTR_COUNT
        self.exhaust_velocity = self.REALISTIC_ISP * 9.81
        self.h2_mass_flow = self.TARGET_THRUST_N / self.exhaust_velocity
        self.chamber_mass = math.pi * (self.external_radius**2 - self.INTERNAL_RADIUS**2) * 2.0 * 8190 * self.NTR_COUNT
        return self.wall_thickness, self.spike_mass, self.h2_mass_flow, self.chamber_mass

    def calculate_starship_mass(self):
        self.tw_ratio = self.TARGET_THRUST_N / (self.dry_mass * 9.81) # orbital T/W
        self.engine_out_tw = (self.THRUST_PER_NTR * (self.NTR_COUNT - 1)) / (self.dry_mass * 9.81)
        self.h2_volume = self.total_propellant / 70.85
        self.tank_length = self.h2_volume / (math.pi * 4.5**2) # 9m diameter = 4.5m radius
        self.total_vehicle_height = 4.5 + self.tank_length + 12.0
        return self.launchpad_total_mass, self.tw_ratio, self.total_vehicle_height, self.engine_out_tw

    def generate_all_files(self):
        t, m_s, f, m_c = self.calculate_aerospike_motor()
        m_pad, tw, h, e_out_tw = self.calculate_starship_mass()

        bom_items = [
            ["System", "Item", "Spec", "Mass_kg", "USD", "TRL"],
            ["Propulsion", "Aerospike Chamber Inconel-718", f"{t*1000:.1f}mm wall x4", int(m_c), 4000000, 5],
            ["Propulsion", "Central Spike C-C/NbC Structure", f"4.5m H x4 @1350K", int(m_s), 14000000, 4],
            ["Propulsion", "NTR Reactor UC-ZrC-NbC HALEU Core", f"0.6mDx0.9mL x4 @185kN/3100K", 20000, 32000000, 5],
            ["Propulsion", "LH2 Turbopumps High-Flow Array", f"{f:.1f} kg/s @ 125bar", 8000, 16000000, 6],
            ["Structure", "LH2 Heavy Tank Al-Li (9m)", f"9mD x {self.tank_length:.1f}mH", int(self.tanks_mass), 9000000, 8],
            ["Structure", "ATHENA Habitat Core Module", f"{self.HABITAT_VOL}m³ for 6", 10000, 15000000, 7],
            ["EHS", "Radiation Shield PE+H2O Matrix", f"{self.SHIELDING_AREAL_DENSITY}g/cm²", 8000, 500000, 9],
            ["EHS", "ECLSS Closed-Loop Standard", f"{self.MISSION_DAYS} days", int(6*1.25*self.MISSION_DAYS), 20000000, 6],
            ["Power", "Brayton 100kWe Power System", "45kg/kWe", 4500, 10000000, 6],
            ["Avionics", "ODIN AI Triple Voting Array", "100krad CNEN/AEB", 3800, 1200000, 7],
            ["Thermal", "Radiators Extended Core", "2000m²", 2000, 4000000, 7]
        ]

        total_cost = sum([row[4] for row in bom_items[1:]])
        bom_data = bom_items + [["TOTAL", "", "", int(self.dry_mass), total_cost, ""]]

        try:
            with open("01_BOM_STARSHIP_V3.1.csv", "w", newline='') as file_bom:
                csv.writer(file_bom).writerows(bom_data)

            mass = f"""ARES-STARSHIP V3.1 - MASS BREAKDOWN - Prometheus I Mission

LAUNCH SITE: {self.LAUNCH_SITE} (+{self.EARTH_BONUS} m/s bonus)
LEO TOTAL: {self.launchpad_total_mass/1000:.1f} t
Dry Mass: {self.dry_mass/1000:.1f} t
Propellant LH2: {self.total_propellant/1000:.1f} t
Tanks: {self.tanks_mass/1000:.1f} t
T/W RATIO (orbital): {tw:.2f}
Engine-Out T/W: {e_out_tw:.2f} (3 engines)
Total Height: {h:.1f} m

Propulsion: {self.NTR_COUNT}x NTR @ {self.THRUST_PER_NTR/1000:.0f}kN = {self.TARGET_THRUST_N/1000:.0f}kN Total
Delta-V available: {self.DELTA_V_TOTAL} m/s | Required: {self.DELTA_V_REQUIRED} m/s
Margin: {self.DELTA_V_TOTAL - self.DELTA_V_REQUIRED} m/s
Isp: {self.REALISTIC_ISP}s @ {self.CORE_GAS_TEMP}K
Mission Duration: {self.MISSION_DAYS} days | Crew: {self.CREW_COUNT}
Habitat Volume: {self.HABITAT_VOL} m³ | {self.HABITAT_VOL/self.CREW_COUNT:.0f} m³/crew

Key Ratios:
- Propellant Fraction: {self.total_propellant/self.launchpad_total_mass*100:.1f}%
- Shielding: {self.SHIELDING_AREAL_DENSITY} g/cm² PE+H2O
- Transit: 119 days to Mars
- Tank Volume: {self.h2_volume:.1f} m³ LH2 @ 70.85 kg/m³
"""
            with open("02_MASS_BREAKDOWN_V3.1.txt", "w") as file_mass:
                file_mass.write(mass)

            pitch = f"""ARES-STARSHIP V3.1 - INVESTOR ONE PAGER - Prometheus I

Problem: Chemical Mars = 9 months, high radiation.
Solution: 740kN (4x 185kN NTR) Nuclear Aerospike, 119-day transit from Alcântara.

Technical Edge:
- Thrust: {self.NTR_COUNT}x {self.THRUST_PER_NTR/1000:.0f}kN = {self.TARGET_THRUST_N/1000:.0f}kN | Isp: {self.REALISTIC_ISP}s | T/W: {tw:.2f}
- LEO Mass: {self.launchpad_total_mass/1000:.1f}t | Height: {h:.1f}m | Diameter: 9m
- Crew: {self.CREW_COUNT} | Shielding: {self.SHIELDING_AREAL_DENSITY}g/cm² | Power: 100kWe
- Mission: {self.MISSION_DAYS} days | Habitat: {self.HABITAT_VOL}m³
- Heritage: NERVA + CNEN/AEB + 10CFR52 Compliant
- Redundancy: Engine-out abort with 3x NTR

Business Case:
- Unit Cost: ${total_cost/1e6:.1f}M
- Payload TMI: 71t
- No refuel required - margin {self.DELTA_V_TOTAL - self.DELTA_V_REQUIRED} m/s

Ask: $22M Seed -> TRL-4 demonstrator in 18mo
Contact: ranyellson@gmail.com"""
            with open("03_INVESTOR_PITCH_V3.1.txt", "w") as file_pitch:
                file_pitch.write(pitch)

            print("========================================================================")
            print("ARES-STARSHIP V3.1 - PROMETHEUS I SYNC COMPLETE")
            print("========================================================================")
            print(f"1. BOM: ${total_cost/1e6:.1f}M")
            print(f"2. Mass: {self.launchpad_total_mass/1000:.1f}t | Delta-V: {self.DELTA_V_TOTAL} m/s")
            print(f"3. Pitch: {self.TARGET_THRUST_N/1000:.0f}kN | {self.CREW_COUNT} crew | Alcântara")
            print("========================================================================")
        except IOError as e:
            print(f"File writing error: {e}")

if __name__ == "__main__":
    AresStarshipNTR().generate_all_files()