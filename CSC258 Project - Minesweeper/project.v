
// world is of size 8 by 8, and each title is of size by 8 by 8 
module project
	(
		CLOCK_50, KEY,				//Clock
		SW,
		//VGA output
		VGA_CLK,   						//	VGA Clock
		VGA_HS,							//	VGA H_SYNC
		VGA_VS,							//	VGA V_SYNC
		VGA_BLANK_N,					//	VGA BLANK
		VGA_SYNC_N,						//	VGA SYNC
		VGA_R,   						//	VGA Red[9:0]
		VGA_G,	 						//	VGA Green[9:0]
		VGA_B,							//	VGA Blue[9:0]
		//Keyboard
		PS2_CLK,
      PS2_DAT
	) ;
	
	//input
	input CLOCK_50;
	input [3:0]	 KEY;
	input [9:0]	SW;
	//keyboard input
	input     		PS2_CLK;
   input   	   	PS2_DAT; 
	
	// VGA outputs
	output			VGA_CLK;   				//	VGA Clock
	output			VGA_HS;					//	VGA H_SYNC
	output			VGA_VS;					//	VGA V_SYNC
	output			VGA_BLANK_N;			//	VGA BLANK
	output			VGA_SYNC_N;				//	VGA SYNC
	output	[9:0]	VGA_R;   				//	VGA Red[9:0]
	output	[9:0]	VGA_G;	 				//	VGA Green[9:0]
	output	[9:0]	VGA_B;   				//	VGA Blue[9:0]
	

	
	wire gameOverSignal;
	
	wire [5:0] title, neighbour;
	wire wren, wren_has_bomb;
	wire create_world;
	wire [6:0] x, y;	
	wire  [2:0] colour; 
	wire [5:0] pixel_offset;	
	wire right, left, up, down, reveal, game_over;
	wire save_centre, need_neigh_for_reveal, reveal_neigh, neigh_reveal_address_ram_revealed;
	wire reset_game_signal;
	wire resetn;
	
	control c0( 
		.gameOverSignal(gameOverSignal),
		.clock(CLOCK_50),
		.resetn(resetn),
		.wren(wren),  
		.wren_has_bomb(wren_has_bomb), .wren_reveal(wren_reveal),
		.right_1(right),
		.left_1(left),
		.up_1(up),
		.down_1(down),
		.reveal_1(reveal),
		.title(title),
		.create_world(create_world),
		.count_bombs(count_bombs),
		.neighbour(neighbour),
		.update_pixel(update_pixel),
		.pixel_offset(pixel_offset),
		.game_over(game_over),    
		.PS2_CLK(PS2_CLK), .PS2_DAT(PS2_DAT),
		
		
		.save_centre(save_centre), 
		.need_neigh_for_reveal(need_neigh_for_reveal),
		.reveal_neigh(reveal_neigh),
		.neigh_reveal_address_ram_revealed(neigh_reveal_address_ram_revealed),
		.reset_game_signal(reset_game_signal)
	);
	
	datapath d0(
		.gameOverSignal(gameOverSignal),
		.clock(CLOCK_50),
		.wren(wren), 
		.wren_has_bomb(wren_has_bomb), .wren_reveal(wren_reveal),
		.title(title),
		.create_world(create_world),
		.count_bombs(count_bombs),
		.neighbour(neighbour),
		.update_pixel(update_pixel),
		.x(x),
		.y(y),
		.right(right),
		.left(left),
		.up(up),
		.down(down), 
		.reveal(reveal),
		.col(colour),
		.pixel_offset(pixel_offset),
		.game_over(game_over),
		
		.save_centre(save_centre), 
		.need_neigh_for_reveal(need_neigh_for_reveal), 
		.reveal_neigh(reveal_neigh), 
		.neigh_reveal_address_ram_revealed(neigh_reveal_address_ram_revealed),
		.reset_game_signal(reset_game_signal)
	);
	
	vga_adapter VGA(
			.resetn(~resetn),
			.clock(CLOCK_50),
			.colour(colour),
			.plot( 1 ),
			.x(x), .y(y),
			.VGA_R(VGA_R),
			.VGA_G(VGA_G),
			.VGA_B(VGA_B),
			.VGA_HS(VGA_HS),
			.VGA_VS(VGA_VS),
			.VGA_BLANK(VGA_BLANK_N),
			.VGA_SYNC(VGA_SYNC_N),
			.VGA_CLK(VGA_CLK));
		
		defparam VGA.RESOLUTION = "160x120";
		defparam VGA.MONOCHROME = "FALSE";
		defparam VGA.BITS_PER_COLOUR_CHANNEL = 1;
		defparam VGA.BACKGROUND_IMAGE = "black.mif";  
		

endmodule


module control( 
	input clock,				output reg gameOverSignal,
	output resetn,
	output reg wren, wren_has_bomb, wren_reveal,
	output reg right_1, left_1, up_1, down_1, reveal_1,
	output [5:0] title, 
	output [5:0] neighbour,
	output reg count_bombs,
	output reg create_world,
	output [5:0] pixel_offset,
	output reg update_pixel,
	input game_over,    
	input PS2_CLK, input PS2_DAT, 
	output reg save_centre, need_neigh_for_reveal, reveal_neigh, neigh_reveal_address_ram_revealed, 
	output reg reset_game_signal
);
	
	wire right; wire left; wire up; wire down; wire reveal;
	keyboard_PS2 k0(
		.clock(clock),
		.ps2_clk(PS2_CLK),
		.ps2_dat(PS2_DAT),
		.right(right),
		.left(left),
		.up(up),
		.down(down),
		.resetn(resetn),
		.reveal(reveal)
	);
	
	wire [5:0] num_of_titles = 6'd63;  // 64 titles in total
	wire [2:0] max_num_of_neigh = 3'd7 ; // each title can have at most 8 neighbours
	wire [5:0] num_of_pixels= 6'd63;  // 64 pixels for each title
	
	
	wire [2:0] title_offset;  // offset from the current title. Used to select neighbour title 
	
	reg [4:0] current_state, next_state; 
	localparam 	RESET								= 5'd0,	
					CREATE_WORLD					= 5'd1,	// Can initilize bomb count, bomb/no bomb, etc.
					SAVE_TITLE						= 5'd2, 	// need one additional clock cycle inorder to save into register
					
					LOAD_VALUE 						= 5'd3,	// need to load the value first
					COUNT_BOMBS						= 5'd4,	// goes through the neighbouring titles to count the bombs
					SAVE_TITLE_2					= 5'd5,	// loads the count into register
					
					LOAD_COLOR						= 5'd6, // loads the title info
					UPDATE_PIXEL					= 5'd7, // updates the buffer
					
					S_LOAD_KEY						= 5'd8, // waits for user input 
					MOVELEFT_KEY_WAIT				= 5'd9,
					MOVERIGHT_KEY_WAIT			= 5'd10,
					MOVEUP_KEY_WAIT				= 5'd11,
					MOVEDOWN_KEY_WAIT				= 5'd12,
					REVEAL_KEY_WAIT				= 5'd13,
					
					MOVE_LEFT						= 5'd14,	// move LEFT
					MOVE_RIGHT						= 5'd15,	// move RIGHT
					MOVE_UP							= 5'd16,	// move UP
					MOVE_DOWN						= 5'd17,	// move DOWN
					
					LOAD3								= 5'd18,	 // states needed to reveal. load info, update title, save title
					REVEAL							= 5'd19,
					SAVE2								= 5'd20,
					
					// reveals the neighbouring titles
					LOAD_CENTRE_INFO				= 5'd21,	// loads the center piece info. bomb count and reveal status  
					SAVE_CENTRE_INFO				= 5'd22,	// Save info into reg
					LOAD_NEIGHBOUR_INFO			= 5'd23,	// Loads the neighbour info - 
					REVEAL_NEIGHBOUR				= 5'd24,	// update register of reveal status for neighbour
					SAVE_NEIGHBOUR_INFO			= 5'd25, // saves register
					RESET_REVEAL					= 5'd26, // resets some game stuff to 0
					
					WAIT_FOR_RESET					= 5'd27, // reset
					RESET_WAIT						= 5'd28;
	initial current_state = RESET;

	
	always @(*)
	begin: state_table
		case (current_state)
			RESET:						next_state = CREATE_WORLD;
			
			//########################################################################################
			CREATE_WORLD: 				next_state = SAVE_TITLE;
			SAVE_TITLE:					next_state = ( title == num_of_titles ) ? LOAD_VALUE : CREATE_WORLD;	
			
			//########################################################################################
			LOAD_VALUE:					next_state = COUNT_BOMBS;
			COUNT_BOMBS:				next_state = SAVE_TITLE_2;
			SAVE_TITLE_2:				next_state = ( title == num_of_titles  & title_offset == max_num_of_neigh ) ? LOAD_COLOR : LOAD_VALUE; 
			
			//########################################################################################
			LOAD_COLOR:					next_state = UPDATE_PIXEL;
			UPDATE_PIXEL:				begin
												if(  title == num_of_titles & pixel_offset == num_of_pixels )
													next_state = S_LOAD_KEY;
												else 
													next_state = LOAD_COLOR;
											end 
			
			//########################################################################################
			S_LOAD_KEY:					begin			
												if( game_over )
													next_state = WAIT_FOR_RESET; 
												else if (right) 
													next_state = MOVERIGHT_KEY_WAIT ;
												else if (left) 
													next_state = MOVELEFT_KEY_WAIT ;
												else if (up) 
													next_state = MOVEUP_KEY_WAIT ;
												else if (down) 
													next_state = MOVEDOWN_KEY_WAIT ;
												else if(reveal) 
													next_state = REVEAL_KEY_WAIT;
												else if(resetn)
													next_state = RESET_WAIT;
												else
													next_state = S_LOAD_KEY;
											end 
			//########################################################################################
			MOVERIGHT_KEY_WAIT:		next_state = right ? MOVERIGHT_KEY_WAIT : MOVE_RIGHT;
			MOVE_RIGHT:					next_state = LOAD_COLOR;
			
			MOVELEFT_KEY_WAIT:		next_state = left ? MOVELEFT_KEY_WAIT : MOVE_LEFT;
			MOVE_LEFT:					next_state = LOAD_COLOR;
			
			MOVEUP_KEY_WAIT:			next_state = up ? MOVEUP_KEY_WAIT : MOVE_UP;
			MOVE_UP:						next_state = LOAD_COLOR;
			
			MOVEDOWN_KEY_WAIT:		next_state = down ? MOVEDOWN_KEY_WAIT : MOVE_DOWN;
			MOVE_DOWN:  				next_state = LOAD_COLOR;
			
			//########################################################################################
			REVEAL_KEY_WAIT:			next_state = reveal ? REVEAL_KEY_WAIT : LOAD3;  
			LOAD3:						next_state = REVEAL;
			REVEAL:						next_state = SAVE2;
			SAVE2:						next_state = LOAD_CENTRE_INFO;
			
			//########################################################################################
			LOAD_CENTRE_INFO:			next_state = SAVE_CENTRE_INFO;
			SAVE_CENTRE_INFO:			next_state = LOAD_NEIGHBOUR_INFO;
			LOAD_NEIGHBOUR_INFO:		next_state = REVEAL_NEIGHBOUR;
			REVEAL_NEIGHBOUR:			next_state = SAVE_NEIGHBOUR_INFO;
			SAVE_NEIGHBOUR_INFO:		begin
												if( title == num_of_titles  & title_offset == max_num_of_neigh )
													next_state = RESET_REVEAL; 
												else if( title_offset == max_num_of_neigh )
													next_state = RESET_REVEAL;
												else
													next_state = LOAD_NEIGHBOUR_INFO;
											end								
			RESET_REVEAL:				begin
												if( title == 0  & title_offset == 0 )
													next_state = LOAD_COLOR;
												else if( title_offset == 0 )
													next_state = LOAD_CENTRE_INFO;
											end
			//########################################################################################
			WAIT_FOR_RESET: 			next_state = resetn ? RESET_WAIT : WAIT_FOR_RESET;
			RESET_WAIT:				   next_state = resetn ? RESET_WAIT : RESET;
			
			default:						next_state = RESET;
		endcase
	end					
	
	
	reg title_counter_reset, Offset_counter_reset, pixel_counter_reset;
	reg title_counter_enabled, Offset_counter_enabled, pixel_counter_enabled;
	reg need_neigh;
	
	always @(*)
	begin: enable_signals
		title_counter_reset 						= 0;
		Offset_counter_reset 					= 0;
		pixel_counter_reset						= 0;
		
		title_counter_enabled 					= 0;
		Offset_counter_enabled 					= 0;
		pixel_counter_enabled					= 0;
		
		need_neigh 									= 0;
		
		wren 											= 0;
		wren_has_bomb								= 0;
		wren_reveal									= 0;
		
		create_world 								= 0;
		count_bombs 								= 0;
		
		update_pixel								= 0;
		right_1										= 0;
		left_1										= 0;
		up_1											= 0;	
		down_1										= 0;
		reveal_1										= 0;
		
		save_centre									= 0;
		need_neigh_for_reveal					= 0;
		reveal_neigh 								= 0;  
		neigh_reveal_address_ram_revealed 	= 0;
		reset_game_signal									= 0;
		
		gameOverSignal =0;
		
		case (current_state)
			RESET:
				begin
					title_counter_reset = 1;
					Offset_counter_reset = 1;
					pixel_counter_reset = 1;
				end
				
			RESET_WAIT:
				begin
					title_counter_reset = 1;
					Offset_counter_reset = 1;
					pixel_counter_reset = 1;
				end
			
			//#########################################################################	
			CREATE_WORLD: 
				begin
					create_world = 1'b1;
				end 
			SAVE_TITLE:	
				begin
					title_counter_enabled = 1;
					wren_has_bomb = 1'b1;
					wren_reveal = 1;
					wren = 1;
				end 
			
			//#########################################################################	
			LOAD_VALUE:
				begin
					need_neigh = 1'b1;
				end
			COUNT_BOMBS: 
				begin 
					need_neigh = 1'b1;
					count_bombs = 1'b1;
				end
			SAVE_TITLE_2: 
				begin 
					Offset_counter_enabled = 1;
					if ( title_offset == max_num_of_neigh ) 
						title_counter_enabled = 1;
					need_neigh = 1'b1;
					wren = 1'b1;
				end
			
			//#########################################################################	
			UPDATE_PIXEL:
				begin
					update_pixel = 1;
					gameOverSignal = 1;
					pixel_counter_enabled = 1;
					if (pixel_offset == num_of_pixels)
						title_counter_enabled = 1;
				end
			
			//#########################################################################	
			MOVE_RIGHT:
				begin
					right_1 = 1;
					//reveal_1 = 1;
				end
		
			MOVE_LEFT:
				begin
					left_1 = 1;
					//reveal_1 = 1;
				end
			
			MOVE_UP:
				begin
					up_1 = 1;
					//reveal_1 = 1;
				end
			
			MOVE_DOWN:
				begin
					down_1 = 1;
					//reveal_1 = 1;
				end
				
			REVEAL:
				begin
					reveal_1 = 1;
				end
			SAVE2:
				begin
					wren_reveal = 1;
					reveal_1 = 1;
				end
				
						SAVE_CENTRE_INFO:
				begin
					save_centre = 1;
				end
			
			//#########################################################################	
			LOAD_NEIGHBOUR_INFO:
				begin
					need_neigh = 1;
					need_neigh_for_reveal = 1;
				end
				
			REVEAL_NEIGHBOUR:
				begin
					need_neigh = 1;
					need_neigh_for_reveal = 1;
					reveal_neigh = 1;
				end
			SAVE_NEIGHBOUR_INFO:
				begin
					Offset_counter_enabled = 1;
						if ( title_offset == max_num_of_neigh ) 
							title_counter_enabled = 1;
					reveal_neigh = 1;
					need_neigh = 1;
					neigh_reveal_address_ram_revealed = 1;
				end
			RESET_REVEAL:
				begin
					reset_game_signal = 1;
				end
			//#########################################################################	
		endcase
	end
	
//#########################################################################	
	get_neighbour_title gn(
		.need_neigh( need_neigh ),
		.title( title ),
		.offset( title_offset ),
		.neighbour( neighbour )
	);
	
	counter title_counter(
		.clock( clock ),
		.do_count( title_counter_enabled ),
		.reset( title_counter_reset ),
		.max_value( num_of_titles ),
		.count_value( title )
	);
	
	counter titleOffset_counter(
		.clock( clock ),
		.do_count( Offset_counter_enabled ),
		.reset( Offset_counter_reset ),
		.max_value( max_num_of_neigh ),
		.count_value( title_offset )
	);
	
	counter pixel_counter(
		.clock( clock ),
		.do_count( pixel_counter_enabled ),
		.reset( pixel_counter_reset ),
		.max_value( num_of_pixels ),
		.count_value( pixel_offset )
	);
	
//#########################################################################		
	always @( posedge clock)
	begin: state_FFs
		current_state <= next_state;
	end
	
endmodule


		
module datapath(
	input clock,
	input wren, wren_has_bomb, count_bombs, wren_reveal,
	input create_world,
	input [5:0] neighbour,
	input [5:0] title,
	input update_pixel,
	input up, down, left, right, reveal,
	input [5:0] pixel_offset,
	output reg [6:0] x, y,
	output reg [2:0] col,
	output reg game_over,
	input need_neigh_for_reveal, save_centre, reveal_neigh, neigh_reveal_address_ram_revealed, 
	input reset_game_signal,
	
	
	input gameOverSignal
);
	
	reg [5:0] pos; initial pos = 6'd0;  // the current position
	
	// ###############################################################################################################################
	// a register that tells us whether the tile has a bomb or not
	reg has_bomb_in;
	wire has_bomb_out;
	ram64x1 has_bomb
	(
		.address( neighbour ),
		.clock( clock ),
		.data( has_bomb_in ),
		.wren( wren_has_bomb ),
		.q( has_bomb_out )
	);
	
	
	// ###############################################################################################################################
	// a register that tells us whether the tile has been revealed or not
	reg [5:0] rev_title;
	
	// need to have different addresses depending on state
	always @(*)
		begin
		if (reveal)
			rev_title = pos;
		else if( neigh_reveal_address_ram_revealed )
			rev_title = neighbour;
		else
			rev_title = title;
		end
		
	reg is_revealed_in;
	wire is_revealed_out;
	
	// need different wren values depending on state
	reg centre_is_revealed;
	reg is_revealed_wren;
	always @(*)
	begin
		if( centre_is_revealed )
			is_revealed_wren = 1;
		else
			is_revealed_wren = wren_reveal;
	end
	ram64x1 is_revealed
	(
		.address( rev_title ),
		.clock( clock ),
		.data( is_revealed_in ),
		.wren( is_revealed_wren ),
		.q( is_revealed_out )
	);
	

	// ###############################################################################################################################
	// a register that tells us how many neighbouring bombs the tile has
	reg [3:0] bomb_count_in;
	wire [3:0] bomb_count_out;
	ram64x4 bomb_count
	(
		.address( title ),
		.clock( clock ),
		.data( bomb_count_in ),
		.wren(wren),
		.q( bomb_count_out )
	); 
	
	
	// ###############################################################################################################################
	// assign_bomb = 1 with ~20% probability
	wire assign_bomb;
	wire [9:0] total_bombs;
	Fibonacci_LFSR random( 
		.clock(clock),
		.assign_bomb(assign_bomb),
		.total_bombs(total_bombs)
	);
	
	// ###############################################################################################################################
	// selects the image index
	wire color_out;
	reg [3:0] image_index;
	always @(*)
		begin
			if ( ~is_revealed_out )
				image_index = 4'd11;
			else if( has_bomb_out )
				image_index = 4'd10;
			else
				image_index = bomb_count_out;
		end
	// gets the pixel color
	images image( 
		.pixel(pixel_offset) , 
		.image_index( image_index ),
		.selected( pos == title ),
		.col( color_out ) 
	);
	
	
	// ###############################################################################################################################
	// updates game depending on signals
	
	always @( posedge clock )
	begin
		if( create_world )
		// simply creates the grid, initilizes values, assigns bombs
			begin
			 	centre_is_revealed = 0;
				game_over = 0;
				bomb_count_in = 3'd0;
				is_revealed_in = 0;
					
				bomb_count_in = 0	;
				if( assign_bomb == 1 ) 	
					has_bomb_in = 1; 
				else
					has_bomb_in = 0; 
			end
	
		if ( count_bombs  )
		// counts the neighbouring bombs
			begin
				if( has_bomb_out )
					bomb_count_in = bomb_count_out + 1;
				else
					bomb_count_in = bomb_count_out;
			end		
				
		if ( update_pixel )
		// update the pixel to be drawn
			begin
				x = {4'b0000, title[2:0] }* 8 + {4'b0000, pixel_offset[2:0] };
				y = {4'b0000, title[5:3] }* 8 + {4'b0000, pixel_offset[5:3] };
				col = color_out;
			end
	
		if (right)
		// move to the right
			pos = pos + 1;
			
		if (left)
		// move to the left
			pos = pos - 1;
			
		if (up)
		// move the position
			pos = pos - 8;
			
		if (down)
		// move the position
			pos = pos + 8;
			
		if ( reveal )
		// reveals the tile if choosen
			begin
				is_revealed_in = 1;
			end
			
		if( save_centre )
		// saves the center information for purpose of revealing neighbouring tiles
			begin
				if( is_revealed_out & bomb_count_out == 0 )
					centre_is_revealed = 1;
				else
					centre_is_revealed = 0;
			end
			
		if( reveal_neigh )
		// reveal the neighbour if the center has no neighbouring bombs
			begin
				if(  centre_is_revealed  )
					is_revealed_in = 1;
				else
					is_revealed_in = 0;
			end
			
		if( reset_game_signal )
		// resets game
			begin
				centre_is_revealed = 0;
				is_revealed_in = 0;
			end
		if( gameOverSignal)
			begin
			if( is_revealed_out & has_bomb_out )
			begin
			//clicked on a bomb. game is over
				game_over = 1;
			end
		end
	end
		
endmodule
	
		
module counter(
	// a simple counter
	input clock,
	input do_count,
	input reset,
	input [5:0] max_value,
	output reg [5:0] count_value
	);
	
	always @(posedge clock)
	begin
		if (reset )
			count_value <= 0;
		else if( do_count)
			begin
				count_value <= count_value + 1;
				if ( count_value == max_value)
					count_value <= 0;
			end
	end
endmodule


module get_neighbour_title(  
	// this gets the title index of the neighbouring title based on the offset index
	input need_neigh,
	input [5:0] title,
	input [2:0] offset,
	output reg [5:0] neighbour
	);
	
	always @(*)
	begin
		if( need_neigh == 0)
			neighbour = title;
		else
		begin
			case(offset)
				3'd0: begin  // top-left
							if ( title % 8 == 0 |  title < 8 )
								neighbour = title;
							else
								neighbour = title -9;
						end
				3'd1: begin  //top
							if ( title < 8 )
								neighbour = title;
							else
								neighbour = title -8;
						end
				3'd2: begin  // top right
							if ( ( title  + 1 ) % 8 == 0 |  title < 8  )
								neighbour = title;
							else
								neighbour = title -7;
						end
				3'd3: begin   // left
							if ( title % 8 == 0 )
								neighbour = title;
							else
								neighbour = title - 1;
						end
				3'd4: begin   // right
							if ( ( title  + 1 ) % 8 == 0 )
								neighbour = title;
							else
								neighbour = title + 1;
						end
				3'd5: begin   // bottom left
							if ( title % 8 == 0 |  title > 55 )
								neighbour = title;
							else
								neighbour = title + 7 ;
						end
				3'd6: begin  // bottom
							if ( title > 55  )
								neighbour = title;
							else
								neighbour = title + 8;
						end
				3'd7: begin   //bottom right
							if ( ( title  + 1 ) % 8 == 0 |  title > 55  )
								neighbour = title;
							else
								neighbour = title + 9;
						end
				endcase
			end
		end
endmodule



module Fibonacci_LFSR( 
	// uniform number generator 
	input clock,
	output reg assign_bomb,
	output reg [9:0] total_bombs
);

	reg [9:0] x; initial x = 10'd5; 
	initial total_bombs = 10'd0;
	reg bit; 
	
	always @( posedge clock )
	begin
		bit = (x[0] ^ x[3] ) & 1;
		x = x >> 1;
		x[9] = bit;
		if (x < 10'd200 )  // assign bomb with roughly 20 percent probability
			assign_bomb = 1;
		else
			assign_bomb = 0;
		total_bombs = total_bombs + assign_bomb;
	end

endmodule
					

module images( 
	// the images to be drawn
	input [5:0] pixel, 
	input [3:0] image_index, 
	input selected,
	output reg [ 2:0] col 
);
	
	always @(*)
	begin
		case (image_index)
			4'd0: // 0 
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
				
					// image
					6'd10: 	col = 3'b010;
					6'd11: 	col = 3'b010;
					6'd12: 	col = 3'b010;
					6'd18: 	col = 3'b010;
					6'd20: 	col = 3'b010;
					6'd26: 	col = 3'b010;
					6'd28: 	col = 3'b010;
					6'd34: 	col = 3'b010;
					6'd36: 	col = 3'b010;
					6'd42: 	col = 3'b010;
					6'd43: 	col = 3'b010;
					6'd44: 	col = 3'b010;
					default: col = 3'b111;
				endcase
			4'd1: // 1
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
				
					// image
					6'd12: 	col = 3'b010;
					6'd20: 	col = 3'b010;
					6'd28: 	col = 3'b010;
					6'd36: 	col = 3'b010;
					6'd44: 	col = 3'b010;
					default: col = 3'b111;
				endcase
			4'd2: // 2
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
				
					// image
					6'd10: 	col = 3'b010;
					6'd11: 	col = 3'b010;
					6'd12: 	col = 3'b010;
					6'd20: 	col = 3'b010;
					6'd26: 	col = 3'b010;
					6'd27: 	col = 3'b010;
					6'd28: 	col = 3'b010;
					6'd34: 	col = 3'b010;
					6'd42: 	col = 3'b010;
					6'd43: 	col = 3'b010;
					6'd44: 	col = 3'b010;
					default: col = 3'b111;
				endcase
			4'd3: // 3
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
				
					// image
					6'd10: 	col = 3'b010;
					6'd11: 	col = 3'b010;
					6'd12: 	col = 3'b010;
					6'd20: 	col = 3'b010;
					6'd26: 	col = 3'b010;
					6'd27: 	col = 3'b010;
					6'd28: 	col = 3'b010;
					6'd36: 	col = 3'b010;
					6'd42: 	col = 3'b010;
					6'd43: 	col = 3'b010;
					6'd44: 	col = 3'b010;
					default: col = 3'b111;
				endcase
			4'd4: // 4
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
				
					// image
					6'd10: 	col = 3'b010;
					6'd12: 	col = 3'b010;
					6'd18: 	col = 3'b010;
					6'd20: 	col = 3'b010;
					6'd26: 	col = 3'b010;
					6'd27: 	col = 3'b010;
					6'd28: 	col = 3'b010;
					6'd36: 	col = 3'b010;
					6'd44: 	col = 3'b010;
					default: col = 3'b111;
				endcase
			4'd5: // 5
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
				
					// image
					6'd10: 	col = 3'b010;
					6'd11: 	col = 3'b010;
					6'd12: 	col = 3'b010;
					6'd18: 	col = 3'b010;
					6'd26: 	col = 3'b010;
					6'd27: 	col = 3'b010;
					6'd28: 	col = 3'b010;
					6'd36: 	col = 3'b010;
					6'd42: 	col = 3'b010;
					6'd43: 	col = 3'b010;
					6'd44: 	col = 3'b010;
					default: col = 3'b111;
				endcase
			4'd6: // 6
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
				
					// image
					6'd10: 	col = 3'b010;
					6'd11: 	col = 3'b010;
					6'd12: 	col = 3'b010;
					6'd18: 	col = 3'b010;
					6'd26: 	col = 3'b010;
					6'd27: 	col = 3'b010;
					6'd28: 	col = 3'b010;
					6'd34: 	col = 3'b010;
					6'd36: 	col = 3'b010;
					6'd42: 	col = 3'b010;
					6'd43: 	col = 3'b010;
					6'd44: 	col = 3'b010;
					default: col = 3'b111;
				endcase
			4'd7: // 7
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
				
					// image
					6'd10: 	col = 3'b010;
					6'd11: 	col = 3'b010;
					6'd12: 	col = 3'b010;
					6'd20: 	col = 3'b010;
					6'd28: 	col = 3'b010;
					6'd36: 	col = 3'b010;
					6'd44: 	col = 3'b010;
					default: col = 3'b111;
				endcase
			4'd8: // 8
				case (pixel)
					/// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
				
					// image
					6'd10: 	col = 3'b010;
					6'd11: 	col = 3'b010;
					6'd12: 	col = 3'b010;
					6'd18: 	col = 3'b010;
					6'd20: 	col = 3'b010;
					6'd26: 	col = 3'b010;
					6'd27: 	col = 3'b010;
					6'd28: 	col = 3'b010;
					6'd34: 	col = 3'b010;
					6'd36: 	col = 3'b010;
					6'd42: 	col = 3'b010;
					6'd43: 	col = 3'b010;
					6'd44: 	col = 3'b010;
					default: col = 3'b111;
				endcase
			4'd10: // bomb
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
					default: col = 3'b100;
				endcase
			4'd11: // hidden
				case (pixel)
					// title border
					6'd0:		col = selected ? 3'b001 : 3'b111;
					6'd1:		col = selected ? 3'b001 : 3'b111;
					6'd2:		col = selected ? 3'b001 : 3'b111;
					6'd3:		col = selected ? 3'b001 : 3'b111;
					6'd4:		col = selected ? 3'b001 : 3'b111;
					6'd5:		col = selected ? 3'b001 : 3'b111;
					6'd6:		col = selected ? 3'b001 : 3'b111;
					6'd7:		col = selected ? 3'b001 : 3'b000;
					6'd8:		col = selected ? 3'b001 : 3'b111;
					6'd15:	col = selected ? 3'b001 : 3'b000;
					6'd16:	col = selected ? 3'b001 : 3'b111;
					6'd23:	col = selected ? 3'b001 : 3'b000;
					6'd24:	col = selected ? 3'b001 : 3'b111;
					6'd31:	col = selected ? 3'b001 : 3'b000;
					6'd32:	col = selected ? 3'b001 : 3'b111;
					6'd39:	col = selected ? 3'b001 : 3'b000;
					6'd40:	col = selected ? 3'b001 : 3'b111;
					6'd47:	col = selected ? 3'b001 : 3'b000;
					6'd48:	col = selected ? 3'b001 : 3'b111;
					6'd55:	col = selected ? 3'b001 : 3'b000;
					6'd56:	col = selected ? 3'b001 : 3'b000;
					6'd57:	col = selected ? 3'b001 : 3'b000;
					6'd58:	col = selected ? 3'b001 : 3'b000;
					6'd59:	col = selected ? 3'b001 : 3'b000;
					6'd60:	col = selected ? 3'b001 : 3'b000;
					6'd61:	col = selected ? 3'b001 : 3'b000;
					6'd62:	col = selected ? 3'b001 : 3'b000;
					6'd63:	col = selected ? 3'b001 : 3'b000;
					default: col = 3'b111;
				endcase
			default: col = 3'b100;
		endcase
	end
endmodule 
