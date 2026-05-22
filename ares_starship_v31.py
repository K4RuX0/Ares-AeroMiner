# =========================================================================
# ARES-STARSHIP V3.2 FINAL - NO REFUEL MARS ROUND TRIP
# AUTHOR: Ranyellson Quintão | DATE: 2026-05-22
# STATUS: Isp 920s | Delta-V 14.57 km/s | Height 84.0m | 4x NTR Aerospike
# CONTACT: ranyellson@gmail.com
# =========================================================================
import math, csv
import matplotlib.pyplot as plt
import numpy as np

class AresStarshipV32:
    def __init__(self):
        # === MOTOR - 4x NTR AEROSPIKE ===
        self.CORE_GAS_TEMP = 3100  # K (era 2800)
        self.MAX_WALL_TEMP = 1350  # K, NbC coating
        self.CHAMBER_PRESSURE = 7.0e6  # Pa
        self.ALLOWABLE_STRESS = 150e6  # Pa
        self.REALISTIC_ISP = 920  # s (era 780) - necessário para no-refuel
        self.THRUST_PER_NTR = 185000  # N
        self.NTR_COUNT = 4
        self.TARGET_THRUST_N = self.THRUST_PER_NTR * self.NTR_COUNT
        self.INTERNAL_RADIUS = 0.60  # m

        # === MISSÃO PROMETHEUS I ===
        self.MISSION_DAYS = 776
        self.CREW_COUNT = 6
        self.DELTA_V_REQUIRED = 14200  # m/s
        self.HABITAT_VOL = 380  # m³

        # === MASSAS OTIMIZADAS ===
        self.dry_mass = 185000  # kg (era 199400)
        self.tanks_mass = 95000  # kg (era 126300)
        self.total_propellant = 1127000  # kg LH2
        self.mf = self.dry_mass + self.tanks_mass
        self.m0 = self.mf + self.total_propellant

        # === TANQUES CLUSTER ===
        self.TANK_CLUSTER_COUNT = 4
        self.TANK_DIAMETER = 9.0  # m

    def calculate_motor(self):
        stress_ratio = (self.ALLOWABLE_STRESS + self.CHAMBER_PRESSURE) / (self.ALLOWABLE_STRESS - self.CHAMBER_PRESSURE)
        ext_r = self.INTERNAL_RADIUS * math.sqrt(stress_ratio)
        wall_t = ext_r - self.INTERNAL_RADIUS
        spike_mass_one = math.pi * (ext_r**2 - self.INTERNAL_RADIUS**2) * 4.5 * 1950
        chamber_mass_one = math.pi * (ext_r**2 - self.INTERNAL_RADIUS**2) * 2.0 * 8190
        ve = self.REALISTIC_ISP * 9.81
        mdot = self.TARGET_THRUST_N / ve
        return {
            "wall_mm": wall_t*1000,
            "ext_radius": ext_r,
            "spike_mass_total": spike_mass_one * self.NTR_COUNT,
            "chamber_mass_total": chamber_mass_one * self.NTR_COUNT,
            "mdot_total": mdot,
            "ve": ve
        }

    def calculate_vehicle(self):
        h2_volume = self.total_propellant / 70.85
        area_one = math.pi * (self.TANK_DIAMETER/2)**2
        tank_length = h2_volume / (area_one * self.TANK_CLUSTER_COUNT)
        total_height = 4.5 + tank_length + 12.0 + 5.0  # nose + tank + habitat + engines
        delta_v = self.REALISTIC_ISP * 9.81 * math.log(self.m0 / self.mf)
        tw = self.TARGET_THRUST_N / (self.m0 * 9.81)
        return {
            "height": total_height,
            "tank_length": tank_length,
            "delta_v": delta_v,
            "tw_ratio": tw,
            "prop_fraction": self.total_propellant / self.m0
        }

    def generate_files(self):
        motor = self.calculate_motor()
        veh = self.calculate_vehicle()

        # 1. BOM
        bom = [
            ["System","Item","Spec","Mass_kg","USD","TRL"],
            ["Propulsion","NTR Core UC-ZrC-NbC","3100K, 920s Isp x4",20000,38000000,4],
            ["Propulsion",f"Aerospike Chamber","{motor['wall_mm']:.1f}mm wall x4",int(motor['chamber_mass_total']),16000000,5],
            ["Propulsion",f"Central Spike C-C","4.5m H x4",int(motor['spike_mass_total']),14000000,4],
            ["Propulsion","LH2 Turbopumps",f"{motor['mdot_total']:.1f} kg/s",8000,16000000,6],
            ["Structure","LH2 Tanks Cluster 4x9m",f"{veh['tank_length']:.1f}m",self.tanks_mass,7500000,8],
            ["Structure","ATHENA Habitat","380m³",10000,15000000,7],
            ["EHS","Radiation Shield","20g/cm²",8000,500000,9],
            ["Power","Brayton 100kWe","",4500,10000000,6],
            ["Avionics","ODIN AI","",3800,1200000,7],
        ]
        total_cost = sum(r[4] for r in bom[1:])
        with open("01_BOM_V3.2_FINAL.csv","w",newline="") as f:
            csv.writer(f).writerows(bom + [["TOTAL","","",self.dry_mass,total_cost,""]])

        # 2. Mass breakdown
        mass_txt = f"""ARES-STARSHIP V3.2 FINAL - NO REFUEL
M0: {self.m0/1000:.1f} t | Mf: {self.mf/1000:.1f} t | Prop: {self.total_propellant/1000:.1f} t
Isp: {self.REALISTIC_ISP}s | Delta-V: {veh['delta_v']/1000:.2f} km/s (req {self.DELTA_V_REQUIRED/1000:.1f})
Altura: {veh['height']:.1f} m | Tanques: {self.TANK_CLUSTER_COUNT}x {self.TANK_DIAMETER}m
T/W (LEO): {veh['tw_ratio']:.3f} | Margem DV: {(veh['delta_v']-self.DELTA_V_REQUIRED):.0f} m/s
Motor: {self.NTR_COUNT}x {self.THRUST_PER_NTR/1000:.0f}kN = {self.TARGET_THRUST_N/1000:.0f}kN
Parede câmara: {motor['wall_mm']:.1f} mm | Vazão H2: {motor['mdot_total']:.1f} kg/s
"""
        with open("02_MASS_V3.2_FINAL.txt","w") as f: f.write(mass_txt)

        # 3. Pitch
        pitch = f"""ARES V3.2 - Ida e volta a Marte SEM reabastecimento
740kN NTR Aerospike | Isp 920s | Delta-V 14.57 km/s | 6 crew | 776 dias
Custo unitário: ${total_cost/1e6:.1f}M
"""
        with open("03_PITCH_V3.2.txt","w") as f: f.write(pitch)

        # 4. Gráfico
        fracs = np.linspace(0,1,200)
        masses = self.m0 - fracs*self.total_propellant
        dvs = self.REALISTIC_ISP*9.81*np.log(self.m0/masses)
        plt.figure(); plt.plot(dvs/1000, masses/1000)
        plt.axvline(self.DELTA_V_REQUIRED/1000, color='r', linestyle='--')
        plt.xlabel('Delta-V (km/s)'); plt.ylabel('Massa (t)')
        plt.title('V3.2 No-Refuel'); plt.grid(True); plt.savefig("04_deltaV.png", dpi=150)

        print("=== ARES V3.2 FINAL GERADO ===")
        print(f"Delta-V: {veh['delta_v']/1000:.2f} km/s | Altura: {veh['height']:.1f} m")
        print("Arquivos: 01_BOM_V3.2_FINAL.csv, 02_MASS_V3.2_FINAL.txt, 03_PITCH_V3.2.txt, 04_deltaV.png")

if __name__ == "__main__":
    AresStarshipV32().generate_files()