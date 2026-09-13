`timescale 1ns/1ps
module tb_alu8;
  reg [7:0] a,b;
  reg [2:0] op;
  wire [7:0] y;
  wire c,v,z;
  integer ai,bi,oi,sa,sb,sr,checks;
  reg [7:0] ey;
  reg ec,ev;
  alu8 dut(a,b,op,y,c,v,z);
  initial begin
    checks=0;
    for(oi=0;oi<8;oi=oi+1)
      for(ai=0;ai<256;ai=ai+1)
        for(bi=0;bi<256;bi=bi+1) begin
          a=ai; b=bi; op=oi; ec=0; ev=0;
          sa=(ai<128)?ai:ai-256; sb=(bi<128)?bi:bi-256; sr=0;
          case(oi)
            0: begin ey=(ai+bi)%256; ec=(ai+bi)>255; sr=sa+sb; end
            1: begin ey=(ai-bi)&255; ec=ai>=bi; sr=sa-sb; end
            2: ey=ai&bi;
            3: ey=ai|bi;
            4: ey=ai^bi;
            5: ey=255-ai;
            6: begin ey=(ai*2)%256; ec=ai>=128; end
            7: begin ey=ai/2; ec=(ai%2)!=0; end
          endcase
          if(oi<2) ev=(sr < -128)||(sr>127);
          #1;
          if(y!==ey || c!==ec || v!==ev || z!==(ey==0))
            $fatal(1,"ALU mismatch op=%0d a=%0d b=%0d y=%h expected=%h",oi,ai,bi,y,ey);
          checks=checks+1;
        end
    $display("PASS exhaustive ALU: %0d vectors, result/carry/overflow/zero",checks);
    $finish;
  end
endmodule
