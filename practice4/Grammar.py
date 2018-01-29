<<<<<<< HEAD
from DirectedGraph import *
from collections import deque

class Grammar:
    """ G = (N, T, S, P) """
    
    def __init__(self, nonterminals, terminals, start, productions):
        """ nonterminals: set[string]
            terminals: set[string]
            start: string
            productions: dict[string: set[string]] """
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.start = start
        self.productions = productions

        self.lang_prod = lambda a, b: { x  + y for x in a for y in b }
        self.fcg_to_cnf()

    def remove_unit_productions(self):
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
        vector = list(); vector.append(a); vector.append(b)
        return tuple(vector)

    def __reduce(self, collection): 
        def helper(queue, string):
            n = len(string)
            if n > 2:
                queue.append(tuple(string[0]) + index_fun())
                helper(queue, string[1 : n])
            else:
                queue.append(string)

        def index_fun():
            indexed_char = 'D_{%d}' % self.k;
            self.k += 1
            return indexed_char,

        # abcdef => aD1, bD2, cD3, dD4, ef
        # ab => ab
        # a => a
        new_rules = dict()
        original_rules_modified = set()
        for str_enum in collection:
            if len(str_enum) <= 2:
                original_rules_modified.add(str_enum)
            else:
                queue = deque()
                helper(queue, str_enum)
                original_rules_modified.add(queue[0])
                while len(queue) > 1:
                    element = queue.popleft()
                    new_rules[element[1]] = set()
                    new_rules[element[1]].add(queue[0])
        return original_rules_modified, new_rules

    def __print_dict(self, cnf):
        for key in cnf:
            print('{}: '.format(key))
            for value in cnf[key]:
                print(value)
            print()

    def __replace_set_value(self, conjunto, old, new):
        conjunto.remove(old)
        conjunto.add(new)

    def fcg_to_cnf(self):
        self.cnf = self.remove_unit_productions() 
        cnf = self.cnf
        new_rules = dict()
        self.k = 1
        for key in cnf: # enumeramos 
            cnf[key] = set(map(tuple, cnf[key]))
        for key in cnf: # hacemos que cada produccion w sea tal que |w| <= 2
            cnf[key], temp_dict = self.__reduce(cnf[key])
            new_rules = { **new_rules, **temp_dict } # mezclamos diccionarios
        cnf = { **cnf, **new_rules }
        for key in cnf: # creamos nuevas reglas tales que B_x -> x, x en T
            for enum_str in cnf[key]:
                if len(enum_str) == 2:
                    new_tuple = 2 * [None] # lista de longitud 2
                    for i in range(2):
                        char = enum_str[i]
                        if char in self.terminals:
                            new_rules['B_{}'.format(char)] = set()
                            new_rules['B_{}'.format(char)].add(tuple(char)) 
                            new_tuple[i] = 'B_{}'.format(char)
                        else:
                            new_tuple[i] = char
                    self.__replace_set_value(cnf[key], enum_str, tuple(new_tuple))
        cnf = { **cnf, **new_rules }
        self.__print_dict(cnf)
        for key in cnf:
            for value in cnf[key]:
                self.__replace_set_value(cnf[key], value, ''.join(value))
        self.productions = self.cnf

        # 00, 01, 10, 11

    def remove_useless_productions(self):
        pass

    def validate(self, w):
        """ validate(w: string) -> bool
            Determina si una palabra pertenece a la gramatica mediante el algoritmo CYK.
            Funciona ssi la gramatica dada esta en la forma normal de Chomsky. """

        def cyk(i, j):
            ''' Crea una tabla de manera recursiva donde almacena las producciones que 
                generen las subpalabras de la cadena dada, se basa en el principio 
                divide y venceras. '''
            #print('\n',(i, j))
            if j == 1: # Aqui verificamos las variables no terminales que derivan a T
                v[i, j] = set()
                for key in self.productions:
                    if w[i] in self.productions[key]:
                        v[i, j].add(key) 
            else: # Hallamos las variables no terminales que derivan a las subcadenas
                substring = w[i : i + j] 
                sets = set()
                for x in range(1, j): 
                    left, right = divide(substring, x) 
                    l = len(left) 
                    r = len(right) 
                    if not ((i, l) in v): # Si no existen valores en la tabla
                        cyk(i, l)
                    if not ((i + x, r) in v): 
                        cyk(i + x, r)
                    # Obtenemos las variables no terminales validas
                    conjunto = rules(lang_prod(v[i, l], v[i + x, r]))
                    if len(conjunto) > 0: # si es no vacio
                        sets = sets.union(conjunto)
                v[i, j] = sets # Asignamos la union de todas las variables no terminales 
                # validas

        def rules(cartprod):
            ''' rules(cartprod: set[string]) -> set
                Dado un producto de lenguajes, retornamos las reglas que derivan al 
                mismo. '''
            nonterminals = set()
            for value in cartprod:
                for key in self.productions:
                    if value in self.productions[key]:
                        nonterminals.add(key)
            return nonterminals

        def divide(w, i):
            ''' Retorna una bina de la palabra w dividida en dos. 
                La variable i debe estar en range(1, |w|) para efectos del algoritmo.
                >>> divide('pongame diez', 3)
                (pon, game diez) '''
            return w[:i], w[i: len(w)]  

        v = dict() # Variable que guarda los valores de la tabla
        n = len(w)
        cyk(0, n) # Importante obtener v[(0, n)]           
        self.__print_dict(v)
        return self.start in v[0, n]

    def is_rule_cnf(self, values):
        for value in values: # type(value) = string
            n = len(value)
            if n > 2 or n == 0:
                return False
            if n == 1:
                if value not in self.terminals:
                    return False
            if n == 2:
                if all(x in self.nonterminals for x in value) is False:
                    return False
        return True

def lang_prod(x, y):
    """ lang_prod(x: set[string], y: set[string]) -> set[string]
        Retorna el producto de dos lenguajes.  """
=======
from DirectedGraph import *
from collections import deque
import pdb

class Grammar:
    """ G = (N, T, S, P) """
    
    def __init__(self, nonterminals, terminals, start, productions):
        """ nonterminals: set[string]
            terminals: set[string]
            start: string
            productions: dict[string: set[string]] """
        self.nonterminals = nonterminals
        self.terminals = terminals
        self.start = start
        self.productions = productions

        self.lang_prod = lambda a, b: { x  + y for x in a for y in b }
        self.fcg_to_cnf()

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

    def __reduce(self, collection): 
        ''' Funcion de ayuda para fcg_to_cnf. Aqui, nos aseguramos de que las tuplas 
            tengan una longitud menor o igual a 2. '''
        def helper(queue, string):
            n = len(string)
            if n > 2:
                queue.append(tuple(string[0]) + index_fun())
                helper(queue, string[1 : n])
            else:
                queue.append(string)

        def index_fun():
            ''' Simula un subindice a la letra B:  B_x -> x '''
            indexed_char = 'D_{%d}' % self.k;
            self.k += 1
            return indexed_char,

        # abcdef => aD1, bD2, cD3, dD4, ef
        # ab => ab
        # a => a
        new_rules = dict() # aqui se guardaran las reglas D_{n} -> R
        original_rules_modified = set() # modificaremos las reglas originales
        for str_enum in collection:
            if len(str_enum) <= 2: # ya cumple con la condicion
                original_rules_modified.add(str_enum)
            else:
                queue = deque()
                helper(queue, str_enum)
                original_rules_modified.add(queue[0])
                while len(queue) > 1: # para no ir mas alla de la etiquetacion
                    element = queue.popleft()
                    new_rules[element[1]] = set()
                    new_rules[element[1]].add(queue[0])
        return original_rules_modified, new_rules

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

    def fcg_to_cnf(self):
        self.cnf = self.remove_unit_productions() 
        cnf = self.cnf # para no escribir self demasiado
        new_rules = dict() # diccionario de apoyo para guardar nuevas reglas
        self.k = 1 # variable usada en __reduce
        for key in cnf: # "enumeramos"
            cnf[key] = set(map(tuple, cnf[key]))
        for key in cnf: # hacemos que cada produccion w sea tal que |w| <= 2
            cnf[key], temp_dict = self.__reduce(cnf[key])
            new_rules = { **new_rules, **temp_dict } # mezclamos diccionarios (py >= 3.5)
        cnf = { **cnf, **new_rules }
        for key in cnf: # creamos nuevas reglas tales que B_x -> x, x en T
            for enum_str in cnf[key]:
                if len(enum_str) == 2:
                    new_tuple = 2 * [None] # lista de longitud 2
                    for i in range(2):
                        char = enum_str[i]
                        if char in self.terminals:
                            new_rules['B_{}'.format(char)] = set()
                            new_rules['B_{}'.format(char)].add(tuple(char)) 
                            new_tuple[i] = 'B_{}'.format(char)
                        else:
                            new_tuple[i] = char
                    self.__replace_set_value(cnf[key], enum_str, tuple(new_tuple))
        self.cnf = { **cnf, **new_rules }
        #self.__print_dict(cnf)
        for key in self.cnf: # Removemos la enumeracion
            for value in self.cnf[key]:
                self.__replace_set_value(self.cnf[key], value, ''.join(value))

    def remove_useless_productions(self):
        pass

    def validate(self, w):
        """ validate(w: string) -> bool
            Determina si una palabra pertenece a la gramatica mediante el algoritmo CYK.
            Funciona ssi la gramatica dada esta en la forma normal de Chomsky. """

        def cyk(i, j):
            ''' Crea una tabla de manera recursiva donde almacena las producciones que 
                generen las subpalabras de la cadena dada, se basa en el principio 
                divide y venceras. '''
            if j == 1: # Aqui verificamos las variables no terminales que derivan a T
                v[i, j] = set()
                for key in self.cnf:
                    if w[i] in self.cnf[key]:
                        v[i, j].add(key) 
            else: # Hallamos las variables no terminales que derivan a las subcadenas
                substring = w[i : i + j] 
                sets = set()
                for x in range(1, j): 
                    left, right = divide(substring, x) 
                    l = len(left) 
                    r = len(right) 
                    if not ((i, l) in v): # Si no existen valores en la tabla
                        cyk(i, l)
                    if not ((i + x, r) in v): 
                        cyk(i + x, r)
                    # Obtenemos las variables no terminales validas
                    conjunto = rules(lang_prod(v[i, l], v[i + x, r]))
                    if len(conjunto) > 0: # si es no vacio
                        sets = sets.union(conjunto)
                v[i, j] = sets # Asignamos la union de todas las variables no terminales 
                # validas

        def rules(cartprod):
            ''' rules(cartprod: set[string]) -> set
                Dado un producto de lenguajes, retornamos las reglas que derivan al 
                mismo. '''
            nonterminals = set()
            for value in cartprod:
                for key in self.cnf:
                    if value in self.cnf[key]:
                        nonterminals.add(key)
            return nonterminals

        def divide(w, i):
            ''' Retorna una bina de la palabra w dividida en dos. 
                La variable i debe estar en range(1, |w|) para efectos del algoritmo.
                >>> divide('pongame diez', 3)
                (pon, game diez) '''
            return w[:i], w[i: len(w)]  

        v = dict() # Variable que guarda los valores de la tabla
        n = len(w)
        #pdb.set_trace() # breakpoint para el depurador de pdb
        cyk(0, n) # Importante obtener v[(0, n)]           
        #self.__print_dict(v)
        return self.start in v[0, n]

    def is_rule_cnf(self, values):
        for value in values: # type(value) = string
            n = len(value)
            if n > 2 or n == 0:
                return False
            if n == 1:
                if value not in self.terminals:
                    return False
            if n == 2:
                if all(x in self.nonterminals for x in value) is False:
                    return False
        return True

def lang_prod(x, y):
    """ lang_prod(x: set[string], y: set[string]) -> set[string]
        Retorna el producto de dos lenguajes.  """
>>>>>>> 6019c4cc545b83b03522a73e39271ce1c35733d0
    return { a + b for a in x for b in y }