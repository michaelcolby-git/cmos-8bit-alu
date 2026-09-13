`timescale 1ns/1ps
// Reference behavior for the reconstructed transistor-level ALU.
// op: 0 ADD, 1 SUB, 2 AND, 3 OR, 4 XOR, 5 NOT A, 6 SHL A, 7 SHR A.
module alu8(a, b, op, y, carry, overflow, zero);
  input [7:0] a, b;
  input [2:0] op;
  output [7:0] y;
  output [0:0] carry, overflow;
  output zero;
  reg [7:0] y;
  reg [0:0] carry, overflow;
  reg [8:0] wide;
  assign zero = (y == 0);
  always @* begin
    y=0; carry=0; overflow=0; wide=0;
    case(op)
      0: begin
        wide={1'b0,a}+{1'b0,b}; y=wide[7:0]; carry=wide[8];
        overflow=(a[7]==b[7]) && (y[7]!=a[7]);
      end
      1: begin
        wide={1'b0,a}+{1'b0,~b}+9'd1; y=wide[7:0]; carry=wide[8];
        overflow=(a[7]!=b[7]) && (y[7]!=a[7]);
      end
      2: y=a&b;
      3: y=a|b;
      4: y=a^b;
      5: y=~a;
      6: begin y={a[6:0],1'b0}; carry=a[7]; end
      7: begin y={1'b0,a[7:1]}; carry=a[0]; end
    endcase
  end
endmodule
