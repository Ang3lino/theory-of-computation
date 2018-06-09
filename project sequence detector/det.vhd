library ieee;

use ieee.std_logic_1164.all; 
use ieee.numeric_bit.all; -- here we have shift operators 
use ieee.math_real.all; -- log2

-- if name of entity isn't the same of project simulation could fail
entity det is -- turing machine
	generic (
		n : integer := 16);
	port (
		data: in std_logic_vector(n-1 downto 0);
		clk: in std_logic; 
		mclk: inout std_logic;
		control: in std_logic_vector(1 downto 0);
		disp: out std_logic_vector(6 downto 0);
		position_one_hot: out std_logic_vector(n-1 downto 0)
	); 
end entity;

architecture behave of det is

	type state is (d0, d1, d2, d3, d4); 
	constant final_state: state := d4;
	
	signal current_state, next_state: state; 

	signal enable: std_logic;
	signal position: integer range 0 to n - 1;
	signal accepted: std_logic;

	signal tape: std_logic_vector(n-1 downto 0); 

	constant disp_anode_c: std_logic_vector(6 downto 0) := "0110001";
	constant disp_anode_e: std_logic_vector(6 downto 0) := "0110000";
	
	component bin2one_hot 
		generic (bin_vec_len: integer := 8);
		port ( entry: in integer; 
			   result: out std_logic_vector(bin_vec_len-1 downto 0)	);
	end component;
		
	component clk_div 
		generic (   freq: integer := 50e6;
					freq_out: integer := 1 ); 
		port (  clk: in std_logic; 
				o: out std_logic );
	end component;

begin

	u0: bin2one_hot generic map (n) port map(position, position_one_hot);
	--u1: clk_div port map(clk, mclk);
	mclk <= clk;

	disp <= disp_anode_c when accepted = '1' else 
			disp_anode_e;

	management: process(control, mclk) 
	begin 
		if rising_edge(mclk) then 
			if control = "00" then -- save
				tape <= tape; 
			elsif control = "01" then -- load
				tape <= data; 
			elsif control = "10" then -- enable
				position <= position + 1; -- right
			else -- clr
				tape <= (others => '0');
				position <= 0;
			end if;
		end if;
	end process;

	--integer(log2(real(n))) - 1
	turing: process (current_state, tape, position)
	begin
		case current_state is
			when d0 => 	if tape(position) = '1' then
							next_state <= d1;
						else
							next_state <= d0;
						end if;

			when d1 =>	if tape(position) = '0' then
							next_state <= d2;
						else
							next_state <= d0;
						end if;

			when d2 => 	if tape(position) = '1' then
							next_state <= d3;
						else
							next_state <= d0;
						end if;

			when d3 =>	if tape(position) = '0' then
							next_state <= d4;
						else
							next_state <= d0;
						end if;

			when d4 =>	if tape(position) = '1' then
							next_state <= d3;
						else
							next_state <= d0;
						end if;
		end case;

	end process ;
	
	accepted <= '1' when next_state = final_state else 
				'0';

	update_state: process(mclk)
	begin
		if rising_edge(mclk) then
			current_state <= next_state;
		end if;
	end process ;

end architecture;