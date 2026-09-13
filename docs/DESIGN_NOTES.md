# ALU design decisions

## Arithmetic reuse

The adder receives `B XOR SUB` and carry-in `SUB`. ADD therefore computes A+B;
SUB computes A+NOT(B)+1. For subtraction, carry-out equals the unsigned no-borrow
indicator. Signed overflow depends on representability, not unsigned carry: 127+1
overflows signed 8-bit arithmetic, whereas 255+1 produces unsigned carry and zero.

## Gate hierarchy

The generated hierarchy instantiates static CMOS gates rather than behavioral
voltage sources. Each bit contains a full-adder path and parallel logical paths;
a mux tree selects the operation. The generate script keeps bit-level connectivity
consistent and leaves the emitted SPICE text directly inspectable.

## Timing and loading

Ripple carry trades simple structure for a path whose delay grows with width.
Increasing device width changes both drive strength and capacitance, so delay alone
does not characterize a sizing decision. The present revision provides a measured
reference point at fixed loading, with a comparison utility that rejects mismatched
operating conditions.

## Verification boundary

The exhaustive digital test checks the operation contract. The analog vectors
separately check whether the transistor network reaches valid voltage levels.
Transient timing is measured on a deliberately sensitized path, with both edge
directions and explicit thresholds. These checks address different failure modes.
