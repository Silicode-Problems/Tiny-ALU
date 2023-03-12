module tinyalu(
    reset,
    op_code,
    A,
    B,
    out
);
    input wire reset;
    input wire [2:0]op_code;
    input wire [7:0]A;
    input wire [7:0]B;
    output reg[15:0] out;
    parameter no_op =  3'b000,
    add = 3'b001,
    sub = 3'b010,
    mul = 3'b011,
    and_ = 3'b100,
    or_ = 3'b101,
    xor_ = 3'b110,
    comp_ = 3'b111;

    always @(A or B or reset or op_code) begin
        if(reset)
            out = 16'd0;
        else begin
            case(op_code)
                no_op: out = A;
                add: out = A+B;
                sub: out = A-B;
                mul: out = A*B;
                and_: out = A&B;
                or_: out = A|B;
                xor_: out = A^B;
                comp_: out = ~A;
                default: out = 16'd0;
            endcase
        end 
    end
endmodule 