module keyboard_PS2(
	clock,
	ps2_clk,
	ps2_dat,
	right,
	left,
	up,
	down,
	reveal,
	resetn);

	input			clock;			//50M_CLK
	input			ps2_clk;		//PS2 port CLK
	input			ps2_dat;		//PS2 port data signal
	output		right;
	output		left;
	output		up;
	output		down;
	output		reveal;
	output		resetn;

	reg			right;
	reg			left;
	reg			up;
	reg			down;
	reg		 	reveal;
	reg			resetn;
	reg			dat_ready=0;
	//------------------------------------------
	reg			ps2_clk_delay1=0;	//ps2k_clk state register
	reg			ps2_clk_delay2=0;
	reg			ps2_clk_delay3=0;	
	wire			ps2_clk_neg;		// ps2k_clk neg edge marker
	
	always @ (posedge clock ) begin			// neg_edge detector					
		ps2_clk_delay1 <= ps2_clk;
		ps2_clk_delay2 <= ps2_clk_delay1;
		ps2_clk_delay3 <= ps2_clk_delay2;
	end

	assign ps2_clk_neg = ~ps2_clk_delay2 & ps2_clk_delay3;	// 1 stands for neg_edge

	//------------------------------------------
	reg	[7:0]	ps2_byte		=0;		// 1 byte data scan code from keyboard
	reg	[7:0]	temp_data		=0;		// current received data
	reg	[3:0] 	num			=0;		// number of received bits
	reg 		ps2_state		=1;		// 1 stands for pressing the button
	reg		ps2_state_delay1=0;								
	reg		ps2_state_delay2=0;
	reg 		key_flag		=0;		// 1 for loose keyboard button

	always@(posedge clock)begin
		ps2_state_delay1<=ps2_state;
		ps2_state_delay2<=ps2_state_delay1;
		dat_ready<=(~ps2_state_delay2) &  ps2_state_delay1;	// prevent reading several same buttons at the same time
	end

	always @ (posedge clock ) begin
		if(ps2_clk_neg) begin	
			case (num)
				4'd0:	num <= num+1'b1;			// jump starting bit
				4'd1:	begin
						num <= num+1'b1;
						temp_data[0] <= ps2_dat;	// bit0
						end
				4'd2:	begin
						num <= num+1'b1;
						temp_data[1] <= ps2_dat;	// bit1
						end
				4'd3:	begin
						num <= num+1'b1;
						temp_data[2] <= ps2_dat;	// bit2
						end
				4'd4:	begin
						num <= num+1'b1;
						temp_data[3] <= ps2_dat;	// bit3
						end
				4'd5:	begin
						num <= num+1'b1;
						temp_data[4] <= ps2_dat;	// bit4
						end
				4'd6:	begin
						num <= num+1'b1;
						temp_data[5] <= ps2_dat;	// bit5
						end
				4'd7:	begin
						num <= num+1'b1;
						temp_data[6] <= ps2_dat;	// bit6
						end
				4'd8:	begin
						num <= num+1'b1;
						temp_data[7] <= ps2_dat;	// bit7
						end
				4'd9:	begin
						num <= num+1'b1;		// checking bit, do nothing
						end
				4'd10:  begin
						num <= 4'd0;		
						end
				default:;
			endcase
		end	
	end 

	always @ (posedge clock)begin	// dealing with the new_received data
		if(num==4'd10) begin	// 1 byte data
			if(temp_data == 8'hf0) 
				key_flag <= 1'b1;
			else begin
				if(!key_flag) begin	// some button has been pressed
					ps2_state <= 1'b1;
					ps2_byte <= temp_data;
				end
				else begin
					ps2_state <= 1'b0;
					key_flag <= 1'b0;
				end
			end
		end
	end

	always @ (posedge clock)begin
		if (ps2_byte==8'hE075 && dat_ready ==1)begin // up
			up = 1'b1;
		end
		else begin
			up = 1'b0;
		end
	end
	
	always @ (posedge clock)begin
		if (ps2_byte==8'hE072 && dat_ready ==1)begin // down
			down = 1'b1;
		end
		else begin
			down = 1'b0;
		end
	end
	
	always @ (posedge clock)begin
		if (ps2_byte==8'hE074 && dat_ready ==1)begin // left
			right = 1'b1;
		end
		else begin
			right = 1'b0;
		end
	end
	
	always @ (posedge clock)begin
		if (ps2_byte==8'hE06B && dat_ready ==1)begin // right
			left = 1'b1;
		end
		else begin
			left = 1'b0;
		end
	end
	
	always @ (posedge clock)begin
		if (ps2_byte==8'h29 && dat_ready==1)begin	//spacebar
			reveal =1'b1;
		end
		else begin
			reveal =1'b0;
		end
	end	
	
	always @ (posedge clock)begin
		if (ps2_byte==8'h21 && dat_ready==1)begin	//c
			resetn =1'b1;
		end
		else begin
			resetn =1'b0;
		end
	end
	
endmodule
