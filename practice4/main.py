from Grammar import *

__author__ = "Angel Lopez Manriquez"

def ask_productions():
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
        { 'S', 'A', 'B' }, # V
        { 'a', 'b' }, # T
        'S', # S
        { 'S': { 'AB' }, # P
        'A': { 'BB', 'a' },
        'B': { 'AB', 'b' } } 
    )
    #w = 'aabbb'
    w = 'aab'
    print(g.validate(w))

def test2():
    g = Grammar (
        { 'S', 'A', 'B', 'C' }, # V
        { 'a', 'b' }, # T
        'S', # S
        { 'S': { 'AB', 'BC' }, # P
        'A': { 'BA', 'a' },
        'B': { 'CC', 'b' }, 
        'C': { 'AB', 'a' } } 
    )
    w = 'baaba'
    print(g.validate(w))
    g.fcgtocnf()

def tocnftest():
    g = Grammar (
        { 'S', 'A', 'B' }, # V
        { 'a', 'b', 'c' }, # T
        'S', # S
        { # P
            'S': { 'ABa' }, 
            'A': { 'aab' },
            'B': { 'Ac' }
        } 
    )
    g.fcg_to_cnf()
    #print(g.validate('abc'))

def delunittest():
    g = Grammar (
        { 'S', 'A', 'B' }, # V
        { 'a', 'b', 'c' }, # T
        'S', # S
        { # P
            'S': { 'Aa', 'B' }, 
            'A': { 'a', 'bc', 'B' },
            'B': { 'A', 'bb' }
        } 
    )

def finaltest():
    g = Grammar (
        { 'S', 'P', 'F', 'N' }, # V
        { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '(', ')', '/' }, # T
        'S', # S
        { # P
            'S': { 'S+P', 'S-P', 'P' }, 
            'P': { 'P*F', 'P/F', 'F' },
            'F': { '(S)', 'N' },
            'N': { '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0N', '1N', '2N', '3N', '4N', '5N', '6N', '7N', '8N', '9N' } 
        } 
    )
    print(g.validate('1+(2*3-4)'))
    print(g.validate('(12-7/(4+1))*8-7+(5-21)'))
    print(g.validate('5*(4+8'))
    print(g.validate('10+8-'))

ask_productions()