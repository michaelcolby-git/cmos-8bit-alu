"""Check CMOS outputs and measure a sensitized carry path using actual ngspice data."""
import json,random
from pathlib import Path
from generate_netlist import generate
from spice_utils import simulate,at,crossing,average,logic,svg
ROOT=Path(__file__).resolve().parents[1]
def expected(a,b,op):
    y=[(a+b)&255,(a-b)&255,a&b,a|b,a^b,255-a,(a<<1)&255,a>>1][op]
    carry=[int(a+b>255),int(a>=b),0,0,0,0,a>>7,a&1][op]
    signed=lambda x:x if x<128 else x-256
    result=signed(a)+(signed(b) if op==0 else -signed(b))
    ov=int(not -128<=result<=127) if op<2 else 0
    return [(y>>i)&1 for i in range(8)]+[carry,ov,int(y==0)]
def base(vdd,temp):
    pins=[f'a{i}' for i in range(8)]+[f'b{i}' for i in range(8)]+['op0','op1','op2']+[f'y{i}' for i in range(8)]+['carry','overflow','zero','vdd','0']
    return ['ALU reference characterization','.include spice/gates.cir','.include spice/alu8.cir',f'.temp {temp}',f'VDD vdd 0 {vdd}','Xalu '+' '.join(pins)+' alu8']+[f'C{i} {n} 0 10f' for i,n in enumerate([f'y{i}' for i in range(8)]+['carry','overflow','zero'])]
def control(name,stop,signals):
    return ['.control','set noaskquit','set wr_singlescale','set wr_vecnames',f'tran 0.02n {stop} 0 0.02n',f'wrdata build/{name}.dat '+' '.join(signals),'quit','.endc','.end']
def main():
    (ROOT/'spice/alu8.cir').write_text(generate())
    vectors=[(a,b,op) for op in range(8) for a,b in [(0,0),(255,1),(127,1),(128,1),(85,170),(1,255)]]
    rng=random.Random(118)
    vectors += [(rng.randrange(256),rng.randrange(256),rng.randrange(8)) for _ in range(16)]
    signals=[f'v(y{i})' for i in range(8)]+['v(carry)','v(overflow)','v(zero)']
    reports=[]
    for vdd,temp in [(1.8,25),(1.62,85),(1.98,-20)]:
        name=f'functional_{vdd}_{temp}'.replace('.','p').replace('-','m')
        lines=base(vdd,temp)
        for bit,node in enumerate([f'a{i}' for i in range(8)]+[f'b{i}' for i in range(8)]+['op0','op1','op2']):
            values=[]
            for a,b,op in vectors:
                word=a|(b<<8)|(op<<16); values.append(vdd*((word>>bit)&1))
            points=['0',str(values[0])]
            for k in range(1,len(values)):
                points += [f'{k*10}n',str(values[k-1]),f'{k*10+.1}n',str(values[k])]
            lines.append('V'+node+' '+node+' 0 PWL('+' '.join(points)+')')
        rows=simulate(ROOT,name,'\n'.join(lines+control(name,f'{len(vectors)*10}n',signals)))
        for k,vector in enumerate(vectors):
            got=[logic(at(rows,(k*10+9)*1e-9,i+1),vdd) for i in range(11)]
            if got!=expected(*vector): raise AssertionError((name,k,vector,got,expected(*vector)))
        reports.append({'name':name,'vdd':vdd,'temperature_c':temp,'vectors_passed':len(vectors)})
    vdd=1.8; name='carry_path'; lines=base(vdd,25)
    for i in range(8):
        lines.append(f'Va{i} a{i} 0 {vdd}')
        lines.append(f'Vb{i} b{i} 0 '+(f'PULSE(0 {vdd} 20n 100p 100p 20n 40n)' if i==0 else '0'))
    lines += [f'Vo{i} op{i} 0 0' for i in range(3)]
    lines += ['.control','set noaskquit','set wr_singlescale','set wr_vecnames','tran 0.01n 100n 0 0.01n','let power = -v(vdd)*i(VDD)',f'wrdata build/{name}.dat v(b0) v(y7) power','quit','.endc','.end']
    rows=simulate(ROOT,name,'\n'.join(lines))
    fall=crossing(rows,2,vdd/2,20e-9,35e-9,False)-crossing(rows,1,vdd/2,20e-9,21e-9,True)
    rise=crossing(rows,2,vdd/2,40e-9,55e-9,True)-crossing(rows,1,vdd/2,40e-9,42e-9,False)
    if min(rise,fall)<=0: raise AssertionError('Nonpositive propagation delay')
    report={'model':'generic Level-1, spice/gates.cir','vdd':vdd,'temperature_c':25,'load_f':1e-14,
            'stimulus':'A=255; ADD; B0 20ns-high/40ns-period; slew=100ps','power_window_s':[1e-8,9e-8],
            'delay_s':max(rise,fall),'rise_delay_s':rise,'fall_delay_s':fall,
            'average_supply_power_w':average(rows,3,10e-9,90e-9),'functional_checks':reports}
    (ROOT/'build/results.json').write_text(json.dumps(report,indent=2)+'\n')
    svg(rows,[('B0',1,'#58a6ff'),('Y7',2,'#3fb950')],ROOT/'build/carry-path.svg','Measured CMOS ALU carry path | generic model',vdd)
    print(f'PASS {len(vectors)*3} CMOS vectors; sampled path delay={report["delay_s"]*1e9:.6f} ns; total average supply power={report["average_supply_power_w"]*1e6:.6f} uW')
if __name__=='__main__': main()
