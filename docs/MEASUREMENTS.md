# ALU measurement contract

## Functional acceptance

The RTL regression covers all 256 values of A, all 256 values of B, and all eight
operations: 524,288 vectors. Integer arithmetic supplies the expected result and
unsigned flags; signed representability supplies the overflow oracle.

The CMOS regression checks 64 directed/seeded vectors at each of three conditions:
1.8 V / 25 °C, 1.62 V / 85 °C, and 1.98 V / −20 °C. Every result and flag must settle
below 20% VDD for zero or above 80% VDD for one, sampled 9 ns into its 10 ns slot.
Digital exhaustiveness does not imply exhaustive analog coverage.

## Propagation delay

ADD with A=255 and B changing between 0 and 1 sensitizes ripple carry through Y7.
The 0→1 B0 edge produces a falling Y7 edge; the reverse produces a rising Y7 edge.
Each delay is the output 50% VDD crossing minus its corresponding input 50% crossing.
The larger of these two delays is the reported sampled-path delay.

| Parameter | Characterization value |
|---|---|
| Model | Generic MOS Level-1, `spice/gates.cir` |
| Supply / temperature | 1.8 V / 25 °C |
| Output load | 10 fF on each result and flag |
| B0 edge duration | 100 ps |
| Pulse high time / period | 20 ns / 40 ns |
| Maximum transient step | 10 ps |
| Total transient duration | 100 ns |

## Supply power

The script integrates `−V(vdd) × I(VDD)` using time-weighted trapezoids over
10–90 ns. The sign follows the SPICE voltage-source current convention. The result
is total average modeled supply power, including quiescent and transition behavior.
It is not a separate leakage-subtracted switching-power measurement.

## Comparisons and scope

`scripts/compare_runs.py` checks model, voltage, temperature, load, stimulus, and
window equality before calculating relative delay and power changes. Its synthetic
unit-test values test the formula only; they are not reported device measurements.

The voltage/temperature cases use one generic model, so they are not process-corner
sign-off. No baseline-versus-optimized sizing improvement is claimed for this revision.
The exact numerical outputs and source hashes are in [results](../results/VALIDATION.md).
