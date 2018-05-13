from DirectedGraph import *
from collections import deque
import pdb

__author__ = "Angel Lopez Manriquez"

class Grammar:
    """ G = (N, T, S, P) """
    
    def __init__(self, nont, term, productions, start = 'S', epsilon = chr(949)):
        """ El constructor infiere las variables no terminales y no terminales por medio
            del diccionario self.productions. La variable inicial por defecto es el 
            caracter S.
            
            nonterminals: set[string]
            terminals: set[string]
            start: string
            productions: dict[string: set[string]] """
        self.start = start
        self.productions = productions
        self.nonterminals = nont 
        self.terminals = term

        self.lang_prod = lambda a, b: { x  + y for x in a for y in b }

    def __str__(self):
        string = ''
        for head in self.productions:
            string += '{} --> {}\n'.format(head, ' | '.join(self.productions[head]))
        return string

    def remove_useless_productions(self):
        w = list() # it'll be a list of sets
        w.append(set())
        i = 0
        for t in self.terminals: # loop where find which heads derive a terminal
            for h in self.productions:
                for p in self.productions[h]:
                    if t in p:
                        w[0].add(h)
                        break
        print(w[0])
        while True: # emulation of do-while
            w.append(set())
            for currentP in w[i]: # find which heads derive w[i]
                for h in self.productions:
                    if h in w[i]:
                        continue
                    for p in self.productions[h]:
                        if currentP in p:
                            w[i + 1].add(h)
                            break
            print(w[i + 1])
            w[i + 1] = w[i + 1] | w[i]
            print(w[i])
            if w[i] == w[i +1]: # w[i] will be our new nonterminals
                break
            i = i + 1
        useless = self.nonterminals - w[i]
        to_delete = dict() # now we'll remove dead productions
        for u in useless: 
            for h in self.productions:
                for p in self.productions[h]:
                    if u in p:
                        if not h in to_delete:
                            to_delete[h] = set()
                            to_delete[h].add(p)
                        else:
                            to_delete[h].add(p)
        for k in to_delete.keys():
            for v in to_delete[k]:
                self.productions[k] = self.productions[k] - to_delete[k]
        print(self)

    def substitute(self, _bodies, body_to_change, nonterminal, count = 1):
        """ Retorna una copia de las producciones modificada con la regla de substitucion. """
        bodies = _bodies.copy()
        new_bodies = set()
        for body in self.productions[nonterminal]:
            new_bodies.add(body_to_change.replace(nonterminal, body, count))
        bodies.remove(body_to_change) # Removemos la variable a cambiar
        return bodies | new_bodies # Regresamos una union de conjuntos

    def remove_unit_productions(self):
        ''' Removemos producciones unarias mediante un grafo '''
        g = DirectedGraph()
        productions = self.productions.copy()
        for key in productions: # construimos el grafo
            for rule in productions[key]:
                if len(rule) == 1 and rule in self.nonterminals:
                    g.add_edge(key, rule)
        followings = { v: g.vertices_forward(v) for v in g.vertices() }
        not_unit = dict()
        not_unit_fun = lambda s: len(s) != 1 or s in self.terminals
        for vertex in g.vertices():
            not_unit[vertex] = set(filter(not_unit_fun, productions[vertex])) 
        for e0, e1 in g.edges():
            productions[e0].remove(e1)
            for node in followings[e0]:
                productions[e0] = productions[e0] | not_unit[node]
        return productions

    def add_lists(a, b = None): 
        ''' Retorna una lista concatenada, parecida al operador ++ de Scala o Haskell '''
        vector = list(); vector.append(a); vector.append(b)
        return tuple(vector)

    def __print_dict(self, cnf):
        """ Esta funcion no es necesaria para el algoritmo, se uso para depurar el codigo """
        for key in cnf:
            print('{}: '.format(key))
            for value in cnf[key]:
                print(value)
            print()

    def __replace_set_value(self, conjunto, old, new):
        conjunto.remove(old)
        conjunto.add(new)


