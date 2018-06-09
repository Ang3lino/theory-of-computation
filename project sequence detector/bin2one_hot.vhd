library ieee;

use ieee.std_logic_1164.all;
use ieee.math_real.all; -- log2

entity bin2one_hot is 
	generic (bin_vec_len: integer := 8);
	port ( entry: in integer; 
		   result: out std_logic_vector(bin_vec_len-1 downto 0)	);
end entity;

architecture arch of bin2one_hot is

begin 

	process (entry)
		variable i: integer range 0 to bin_vec_len - 1;
		variable ans: std_logic_vector(bin_vec_len - 1 downto 0);
	begin 
		for i in 0 to bin_vec_len - 1 loop 
			if i = entry then 
				ans(i) := '1';
			else 
				ans(i) := '0';
			end if;
		end loop;
		result <= ans;
	end process;

end architecture;