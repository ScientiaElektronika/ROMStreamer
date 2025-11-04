module ROMStreamer(
    i_clk,
    i_rst_n,
    o_DAC_X,
    o_DAC_Y
);

    localparam  DATA_WIDTH = 9;
    localparam  DEPTH = 2387;
    localparam  XFILE = "imagex.mem";
    localparam  YFILE = "imagey.mem";

    input i_clk;
    input i_rst_n;
    output [DATA_WIDTH-1:0] o_DAC_X;
    output [DATA_WIDTH-1:0] o_DAC_Y;

    // -- cnt reg
    reg [$clog2(DEPTH)-1:0] rom_addr;
    // X-Y
    wire [DATA_WIDTH-1:0] data_X;
    wire [DATA_WIDTH-1:0] data_Y;

    image_ROM
    #(
        .DATA_WIDTH(DATA_WIDTH),
        .DEPTH(DEPTH),
        .FILE(XFILE)
    )
    u_ROM_X
    (
        .i_clk(i_clk),
        .i_addr(rom_addr),
        .o_data(data_X)
    );

    image_ROM
    #(
        .DATA_WIDTH(DATA_WIDTH),
        .DEPTH(DEPTH),
        .FILE(YFILE)
    )
    u_ROM_Y
    (
        .i_clk(i_clk),
        .i_addr(rom_addr),
        .o_data(data_Y)
    );
    always @(posedge i_clk or negedge i_rst_n) begin
        if(!i_rst_n) begin
            rom_addr <= 0;
        end
        else if (rom_addr < DEPTH - 1) begin
            rom_addr <= rom_addr + 1;
        end
        else begin
            rom_addr <= 0;
        end
    end

    assign o_DAC_X = data_X;
    assign o_DAC_Y = data_Y;
endmodule
