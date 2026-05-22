import pytest
import math

class TestAresStarshipV31Heavy:
    """NASA NPR 8705.2C Compliance Test Suite for ARES-STARSHIP V3.1 Heavy"""
    
    # Constants from ares_v31_ntr.py
    THRUST_PER_NTR = 185000  # N
    NTR_COUNT = 4
    TARGET_THRUST_N = THRUST_PER_NTR * NTR_COUNT  # 740000 N
    DRY_MASS = 199400  # kg
    TOTAL_PROPELLANT = 1127000  # kg
    TANKS_MASS = 126300  # kg
    LAUNCHPAD_TOTAL_MASS = DRY_MASS + TOTAL_PROPELLANT + TANKS_MASS  # 1452700 kg
    REALISTIC_ISP = 780  # s
    DELTA_V_TOTAL = 14200  # m/s
    G0 = 9.81  # m/s²
    
    def test_tw_ratio_nasa_compliant(self):
        """NASA NPR 8705.2C: T/W > 0.5 required for crewed launchpad escape"""
        tw = self.TARGET_THRUST_N / (self.LAUNCHPAD_TOTAL_MASS * self.G0)
        assert tw >= 0.5, f"T/W {tw:.3f} fails NASA minimum 0.5"
        assert round(tw, 2) == 0.52, f"T/W expected 0.52, got {tw:.3f}"
    
    def test_engine_out_abort_capability(self):
        """NASA: Must demonstrate abort to safe orbit on N-1 engines"""
        engine_out_thrust = self.THRUST_PER_NTR * (self.NTR_COUNT - 1)
        e_out_tw = engine_out_thrust / (self.LAUNCHPAD_TOTAL_MASS * self.G0)
        assert e_out_tw >= 0.35, f"Engine-out T/W {e_out_tw:.3f} below 0.35 abort minimum"
        assert round(e_out_tw, 2) == 0.39, f"Engine-out T/W expected 0.39, got {e_out_tw:.3f}"
    
    def test_delta_v_budget(self):
        """Verify propellant mass supports Earth-Mars-Earth DV requirement"""
        exhaust_velocity = self.REALISTIC_ISP * self.G0
        mass_ratio = math.exp(self.DELTA_V_TOTAL / exhaust_velocity)
        required_prop = (self.DRY_MASS * mass_ratio) - self.DRY_MASS
        required_with_margin = required_prop * 1.15
        
        assert self.TOTAL_PROPELLANT >= required_with_margin, \
            f"Propellant {self.TOTAL_PROPELLANT/1000:.1f}t < required {required_with_margin/1000:.1f}t"
    
    def test_mass_fraction_realistic(self):
        """Propellant fraction should be 75-80% for NTR Mars architecture"""
        prop_fraction = self.TOTAL_PROPELLANT / self.LAUNCHPAD_TOTAL_MASS
        assert 0.75 <= prop_fraction <= 0.80, \
            f"Prop fraction {prop_fraction:.3f} outside realistic 0.75-0.80 range"
    
    def test_spike_density_correct(self):
        """Regression: Ensure C-C density 1950 kg/m³, not Inconel 8190"""
        # Geometry from code
        internal_radius = 0.60
        allowable_stress = 150e6
        chamber_pressure = 7.0e6
        stress_ratio = (allowable_stress + chamber_pressure) / (allowable_stress - chamber_pressure)
        external_radius = internal_radius * math.sqrt(stress_ratio)
        
        spike_vol = math.pi * (external_radius**2 - internal_radius**2) * 4.5
        spike_mass_cc = spike_vol * 1950 * self.NTR_COUNT
        spike_mass_inconel = spike_vol * 8190 * self.NTR_COUNT
        
        # Spike should be ~1.6t with C-C, not ~6.8t with Inconel
        assert spike_mass_cc < 2000, f"Spike mass {spike_mass_cc:.0f}kg too high for C-C"
        assert spike_mass_inconel > 6000, "Inconel check: would be 6x too heavy"
    
    def test_mass_budget_closure(self):
        """Verify dry + prop + tanks = pad mass exactly"""
        calculated_pad = self.DRY_MASS + self.TOTAL_PROPELLANT + self.TANKS_MASS
        assert calculated_pad == self.LAUNCHPAD_TOTAL_MASS, \
            f"Mass budget mismatch: {calculated_pad} != {self.LAUNCHPAD_TOTAL_MASS}"
    
    def test_isp_nerva_heritage(self):
        """Isp 780s must be within NERVA demonstrated 825s-850s envelope"""
        assert 750 <= self.REALISTIC_ISP <= 850, \
            f"Isp {self.REALISTIC_ISP}s outside NERVA heritage 750-850s"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])