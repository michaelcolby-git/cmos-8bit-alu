# Measurement contract

Digital results are checked against integer arithmetic, including signed range checks.
The transistor script separately checks settled output and flags for directed cases.
Rail checks require logic low < 20% VDD and logic high > 80% VDD, not merely a 50% threshold.

Timing sensitizes ADD carry propagation: A=255, B switches 0 to 1, so Y7 falls.
Delay is the Y7 falling 50% crossing minus the B0 rising 50% crossing after 20 ns.
The reverse transition also measures the rising output delay. The maximum of these
two measurements is the sampled path delay, NOT a universal worst case.

Power is the average of `-V(vdd)*I(VDD)` over 10-90 ns, including quiescent and
transition behavior. Supply-current sign follows SPICE voltage-source convention.
It is total average modeled supply power, not leakage-subtracted switching power.
Do not compare it directly with the resume's 45 uW without reconciling the definitions.

The sweep runs nominal supply/temperature and selected voltage/temperature cases.
These are voltage/temperature samples, not foundry process corners. Global width
scaling is an experiment, not a claimed optimization. Use identical stimuli, output
loads, input slopes, model, voltage, temperature, and measurement windows when comparing.
`scripts/compare_runs.py` rejects mismatched conditions and prints percent changes.

For the original Cadence work, attach schematic/hierarchy exports, permitted model
identifiers, sizing table, baseline and optimized logs, labeled edge crossings, and
the vectors used to establish the actual worst path.
