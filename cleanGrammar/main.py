from Grammar import *

__author__ = "Angel Lopez Manriquez"

def ask_productions(): 
    """ Obtiene una gramatica por teclado. """
    print("\n Programa que limpia gramaticas .\n")
    nonterminals = set(input("\nIngrese las variables no terminales, separadas por ,: ").
        replace(" ", "").split(','))
    terminals = set(input("\nIngrese las variables terminales, separadas por ,: "). 
        replace(" ", "").split(','))
    start = input("Ingrese la variable inicial: ")
    epsilon = input("Ingrese el caracter que tome el papel de cadena vacia: ")
    productions = dict()
    print("Ingrese las productiones separadas por | : ")
    for value in nonterminals:
        ans = input("{} --> ".format(value)).replace(" ", "").split('|')
        productions[value] = set(ans)
    g = Grammar (nonterminals, terminals, productions, start, epsilon)
    print("La gramatica introducida fue: ")
    print(g)
    print("\nHasta luego. o-o// ")

# G = (V, T, P, S)
def test1():
    g = Grammar (
        { 'A', 'B', 'C', 'E', 'S' }, # N
        { 'a', 'c', 'e' }, # T
        { 
            'S': { 'AC', 'B' }, # P
            'A': { 'a' },
            'C': { 'c', 'BC' },
            'E': { 'aA', 'e' }
        } 
    )
    print(g)
    g.remove_useless_productions()
    g.remove_null_productions()

# G = (V, T, P, S)
def test2():
    g = Grammar (
        { 'A', 'B', 'C', 'S' }, # N
        { 'a', 'b', 'c' }, # T
        { 
            'S': { 'ABAC' }, # P
            'A': { 'aA', chr(949) },
            'B': { 'bB', chr(949) },
            'C': { 'c' }
        } 
    )
    print(g)
    g.remove_null_productions()

test1()
