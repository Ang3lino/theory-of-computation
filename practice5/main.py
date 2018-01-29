from Grammar import *

__author__ = "Angel Lopez Manriquez"

def ask_productions(): # Cuidado con el constructor
    """ Obtiene una gramatica por teclado. """
    print("\n Programa que determina si una palabra pertenece o no a una GLC.\n")
    nonterminals = set(input("\nIngrese las variables no terminales, separadas por ,: ").
        replace(" ", "").split(','))
    terminals = set(input("Ingrese las variables terminales, separadas por ,: ").
        replace(" ", "").split(','))
    start = input("Ingrese la variable inicial: ")
    productions = dict()
    print("Ingrese las productiones separadas por | : ")
    for value in nonterminals:
        productions[value] = set(input("{} --> ".format(value)).replace(" ", "").split('|'))
    g = Grammar (nonterminals, terminals, start, productions)
    want_to_continue = 'y'
    while want_to_continue == 'y':
        print()
        word = input("Ingrese una palabra ")
        if g.validate(word):
            print("La palabra %s pertenece a L(G) :D " % word)
        else:
            print("La palabra %s no pertenece a L(G) D: " % word)
        want_to_continue = input("Desea continuar? (y/n): ")
    print("\nHasta luego. o-o// ")

# G = (V, T, S, P)
def test1():
    g = Grammar (
        { 'S': { 'AB' }, # P
        'A': { 'BB', 'a' },
        'B': { 'AB', 'b' } } 
    )
    #w = 'aabbb'
    #w = 'aab'
    #print(g.validate(w))

def test2():
    g = Grammar (
        { 'S': { 'AB', 'BC' }, # P
        'A': { 'BA', 'a' },
        'B': { 'CC', 'b' }, 
        'C': { 'AB', 'a' } } 
    )
    #w = 'baaba'
    #print(g.validate(w))
    #g.fcgtocnf()

def test3():
    g = Grammar (
        { 
            'S': { 'CA', 'BB' }, # P
            'C': { 'b' }, 
            'A': { 'a' },
            'B': { 'SB', 'b' }
        } 
    )
    #print(g.substitute({ 'SB', 'b' }, 'SB', 'S'))
    g.cnf_to_gnf()

test3()