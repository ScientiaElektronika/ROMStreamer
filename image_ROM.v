module image_ROM (
    i_clk,
    i_addr,
    o_data
);

    parameter  DATA_WIDTH = 9;
    parameter  DEPTH = 19090;
    parameter  FILE = "imagex.mem";

    localparam DEPTH_BITS = $clog2(DEPTH);

    input  wire i_clk;
    input  wire [DEPTH_BITS - 1:0] i_addr;
    output reg [DATA_WIDTH-1:0] o_data;

    reg [DATA_WIDTH-1:0] data [0:DEPTH - 1];

    initial begin
        $readmemh(FILE, data);
    end
    always @(posedge i_clk) begin
        o_data <= data[i_addr];
    end
endmodule