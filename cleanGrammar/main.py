from Grammar import *

__author__ = "Angel Lopez Manriquez"

def ask_productions(): 
    """ Obtiene una gramatica por teclado. """
    print("\n Programa que transforma una gramatica de su FNC a la FNG.\n")
    nonterminals = set(input("\nIngrese las variables no terminales, separadas por ,: ").
        replace(" ", "").split(','))
    start = input("Ingrese la variable inicial: ")
    productions = dict()
    print("Ingrese las productiones separadas por | : ")
    for value in nonterminals:
        ans = input("{} --> ".format(value)).replace(" ", "").split('|')
        productions[value] = set(ans)
    g = Grammar (productions, start)
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

test1()
