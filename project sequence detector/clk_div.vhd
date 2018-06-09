library ieee;

use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

-- internal oscilator of fpga cyclone ii EP2C5T144C8N is 50Mhz 

entity clk_div is
	generic (
		freq: integer := 50e6;
		freq_out: integer := 1 ); 
	port (
		clk: in std_logic; 
		o: out std_logic );
end entity;

architecture angel of clk_div is
	signal os: std_logic;
begin

	process (clk)
		variable i: integer range 0 to freq;
	begin 
		if rising_edge(clk) then 
			if i = (freq * freq_out) / 2 then 
				os <= not os;
				i := 0; 	
			else 
				i := i + 1; 
			end if;
		end if;
	end process;

	o <= os;

end architecture ; -- arch