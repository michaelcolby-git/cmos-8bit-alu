"""Compare measured JSON runs without inventing baseline measurements."""
import json, math, sys
def compare(a,b):
    for key in ('model','vdd','temperature_c','load_f','stimulus','power_window_s'):
        if a[key]!=b[key]: raise ValueError('Unmatched conditions: '+key)
    for d in (a,b):
        for key in ('delay_s','average_supply_power_w'):
            if not math.isfinite(d[key]) or d[key]<=0: raise ValueError('Expected positive finite '+key)
    return {'delay_reduction_percent':100*(a['delay_s']-b['delay_s'])/a['delay_s'],
            'power_change_percent':100*(b['average_supply_power_w']/a['average_supply_power_w']-1)}
if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('Usage: python scripts/compare_runs.py baseline.json candidate.json')
    print(json.dumps(compare(*[json.load(open(p)) for p in sys.argv[1:]]),indent=2))
