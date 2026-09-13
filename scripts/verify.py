"""Run exhaustive RTL verification and optional transistor characterization."""
import argparse, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def run(cmd):
    p=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print(p.stdout)
    if p.returncode: raise SystemExit(p.returncode)
    return p.stdout
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--spice',action='store_true'); args=ap.parse_args()
    (ROOT/'build').mkdir(exist_ok=True)
    run([sys.executable,'scripts/generate_netlist.py'])
    run([os.getenv('IVERILOG','iverilog'),'-g2012','-Wall','-s','tb_alu8','-o','build/alu.vvp','rtl/alu8.v','tests/tb_alu8.v'])
    result=run([os.getenv('VVP','vvp'),'build/alu.vvp'])
    if 'PASS exhaustive' not in result: raise SystemExit('Missing simulation success marker')
    (ROOT/'build/rtl.log').write_text(result)
    if args.spice: run([sys.executable,'scripts/characterize.py'])
