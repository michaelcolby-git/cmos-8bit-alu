import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from compare_runs import compare
class Comparison(unittest.TestCase):
    def setUp(self):
        self.a=dict(model='test fixture',vdd=1.8,temperature_c=25,load_f=1e-14,stimulus='test fixture',power_window_s=[0,1],delay_s=1,average_supply_power_w=1)
    def test_percentage(self):
        b=dict(self.a,delay_s=.83,average_supply_power_w=1.04)
        r=compare(self.a,b)
        self.assertAlmostEqual(r['delay_reduction_percent'],17)
        self.assertAlmostEqual(r['power_change_percent'],4)
    def test_reject_mismatched_conditions(self):
        with self.assertRaises(ValueError): compare(self.a,dict(self.a,vdd=1.62))
    def test_reject_invalid_measurement(self):
        for value in (0,-1,float('nan'),float('inf')):
            with self.assertRaises(ValueError): compare(self.a,dict(self.a,delay_s=value))
if __name__=='__main__': unittest.main()
