
-- Proyecto: Maquina de Turing
-- Integrantes del equipo
-- Lopez Manriquez Angel
-- Grupo: 2CV1
--    ==============================================================================
	
--	HDL (Hardware Design Language) que determina el lenguaje 
--		L = (0|1)*(1010)+
--	usando el concepto de maquina de Turing, cuando nos encontremos en el estado 
--	final se muestra en un display una C de correcto y una E de error en otro caso.

--	Como efecto secundario, este puede ser usado como un detector de secuencia para 
--	una cadena w = 1010.
    
-- Caracteristicas -----------------------------------------------------------------
--	Hacemos uso de la palabra reservada type que nos provee VHDL para la creacion 
--	de un estado y usamos un vector logico, el cual simula la cinta. Para saber en 
--	que posicion estamos, hacemos uso de un entero.

library ieee; -- biblioteca ieee (Institute of Electrical and Electronics Engineers)

use ieee.std_logic_1164.all; -- para usar std_logic y std_logic_vector
use ieee.numeric_bit.all; -- para usar enteros

entity det is -- detector de secuencia
	generic (
		n : integer := 16); -- numero de bits para la entrada de la cadena
	port (
		data: in std_logic_vector(n-1 downto 0); -- palabra a probar
		clk: in std_logic; -- senial de reloj
		mclk: inout std_logic; -- senial de reloj maestra
		control: in std_logic_vector(1 downto 0); -- entradas de control
		disp: out std_logic_vector(6 downto 0); -- display de anodo comun
		position_one_hot: out std_logic_vector(n-1 downto 0) -- posicion de la cinta
	); 
end entity;

architecture behave of det is

	type state is (d0, d1, d2, d3, d4); -- definicion de edos.
	constant final_state: state := d4; -- edo. final
	
	signal current_state, next_state: state; -- seniales auxiliares

	signal position: integer range 0 to n - 1 := 0;
	signal accepted: std_logic := '0'; -- sera '1' cuando nos encontremos en el estado final

	signal tape: std_logic_vector(n-1 downto 0); 

	constant disp_anode_c: std_logic_vector(6 downto 0) := "0110001";
	constant disp_anode_e: std_logic_vector(6 downto 0) := "0110000";
	
	component bin2one_hot -- retorna la codificacion de un entero en one hot
		generic (bin_vec_len: integer := 8);
		port ( entry: in integer; 
			   result: out std_logic_vector(bin_vec_len-1 downto 0)	);
	end component;
		
	component clk_div -- divisor de frecuencia
		generic (   freq: integer := 50e6;
					freq_out: integer := 1 ); 
		port (  clk: in std_logic; 
				o: out std_logic );
	end component;

begin

	u0: bin2one_hot generic map (n) -- instancia del componente bin2one
		port map(position, position_one_hot);
	--u1: clk_div port map(clk, mclk); -- divisor de frecuencia

	mclk <= clk;

	disp <= (others => '1') when control = "11" else 
				disp_anode_c when accepted = '1' else 
				disp_anode_e;
	
	accepted <= '1' when next_state = final_state else 
					'0';

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
				tape <= (others => '0'); -- limpiamos la cinta
				position <= 0; 
			end if;
		end if;
	end process;

	-- proceso encargado de cambiar de estados
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
							next_state <= d1;
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

	-- actualiza el estado actual por cada flanco de reloj
	update_state: process(mclk)
	begin
		if rising_edge(mclk) then
			current_state <= next_state;
		end if;
	end process ;

end architecture;