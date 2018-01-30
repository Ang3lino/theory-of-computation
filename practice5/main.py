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
    print("La gramatica en la FNG equivalente es: ")
    gnf = g.cnf_to_gnf()
    print(gnf)
    print("\nHasta luego. o-o// ")

# G = (V, T, S, P)
def test1():
    g = Grammar (
        { 
            'S': { 'AB' }, # P
            'A': { 'BB', 'a' },
            'B': { 'AB', 'b' } 
        } 
    )
    gnf = g.cnf_to_gnf()
    print(gnf)

def test2():
    g = Grammar (
        { 'S': { 'AB', 'BC' }, # P
        'A': { 'BA', 'a' },
        'B': { 'CC', 'b' }, 
        'C': { 'AB', 'a' } } 
    )
    gnf = g.cnf_to_gnf()
    print(gnf)

def test3():
    g = Grammar (
        { 
            'S': { 'CA', 'BB' }, # P
            'C': { 'b' }, 
            'A': { 'a' },
            'B': { 'SB', 'b' }
        } 
    )
    gnf = g.cnf_to_gnf()
    print(gnf)

ask_productions()