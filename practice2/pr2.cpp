/*  Practica 2: expresiones regulares
    Autor: Angel Lopez Manriquez
    Grupo: 2CV1
    =================================================================================
        Programa de consola que determina si la cabecera para incluir bibliotecas en 
		C es correcta. Se asume que la cabecera esta en la carpeta donde se instala 
		el lenguaje.
    
    Caracteristicas ------------------------------------------------------------------
		Hacemos uso de la clase regex en conjunto con sus funciones amigas. Al crear
		la variable de instancia le pasamos al constructor la expresion regular.

	Compilacion ------------------------------------------------------------------------------
		g++ pr2.cpp -std=c++11 
		es importante que la version del compilador g++ sea 11 o superior, puesto 
		que desde esta version se incluyo la biblioteca regex. */

#include <iostream>
#include <regex>
#include <string>

using namespace std;

int main(void) {
	// expresion regular que acepta cualquier caracter del alfabeto ingles o digito
	string valid_char = "([A-Z]|[a-z]|\\d)", 
		   include = "#include\\s?((<((" + valid_char + ")+).h>))\\s*",
		   input; // cadena que guardara la expresion a validar
	regex pattern(include); // creamos una variable de instancia tipo regex
	getline(cin, input); // leemos todo el texto de una linea ingresado por teclado
	bool accepted = regex_match(input, pattern);
	cout << (accepted ? "Cadena valida" : "cadena invalida") << endl;
	return 0;
}
