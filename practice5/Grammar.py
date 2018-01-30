from DirectedGraph import *
from collections import deque
import pdb

__author__ = "Angel Lopez Manriquez"

class Grammar:
    """ G = (N, T, S, P) """
    
    def __init__(self, productions, start = 'S'):
        """ El constructor infiere las variables no terminales y no terminales por medio
            del diccionario self.productions. La variable inicial por defecto es el 
            caracter S.
            
            nonterminals: set[string]
            terminals: set[string]
            start: string
            productions: dict[string: set[string]] """
        self.start = start
        self.productions = productions
        self.nonterminals = self.__determine_nonterminals()
        self.terminals = self.__determine_terminals()

        self.lang_prod = lambda a, b: { x  + y for x in a for y in b }
        self.is_cnf = False

    def __str__(self):
        for head in self.productions:
            for body in self.productions[head]:
                print(head, '-->', body)

    def __determine_nonterminals(self):
        """ Es importante ejecutar este metodo antes de __determine_terminals() """
        return set(self.productions.keys())

    def __determine_terminals(self):
        terminals = set()
        for strings in self.productions.values():
            for string in strings:
                for char in string:
                    terminals.add(char)
        return terminals - self.nonterminals

    def __cmp_rule(self, nonterm, rule):
        """ Metodo usado para ordenar las variables no terminales en el metodo
            cnf_to_gnf. """
        values = self.enum # es un diccionario que guarda las enumeraciones de las variables
        # no terminales
        if not rule[0] in values:
            return 1 # si el cuerpo es de la forma aA siendo a un terminal
        i = values[nonterm] 
        j = values[rule[0]]
        if i < j:
            return 1
        elif i == j:
            return 0
        elif i > j:
            return -1

    def __make_ascending_indexes(self):
        """ Despues de ejecutar este metodo se garantiza para A_i -> A_jw que i <= j """
        valid_bodies = set()
        def helper(head, bodies):
            ''' Adjunta los cuerpos validos en la variable valid_bodies. '''
            posible_valid_bodies = set()
            for body in bodies:
                if self.__cmp_rule(head, body) >= 0:
                    valid_bodies.add(body)
                else:
                    posible_valid_bodies = self.substitute(bodies, body, body[0])
            if len(posible_valid_bodies) > 0:
                helper(head, posible_valid_bodies)
        for head in self.productions:
            valid_bodies = set()
            helper(head, self.productions[head])
            self.productions[head] = valid_bodies

    def __remove_equal_indexes(self):
        """ Remueve las reglas que tienen recursividad por la izquierda. 
            Para no tener caracteres raros k deberia estar en [9312, 9471] """
        rules = self.productions
        k = 9312 # Valor UTF-8
        recursive_bodies = list()
        new_rules = dict()
        for head in rules:
            at_least_one = False # variable para saber si al menos un cuerpo de la produccion
            # tiene recursividad por la izquierda
            for body in rules[head]:
                if self.__cmp_rule(head, body) == 0: # tienen recursividad por la izquierda
                    recursive_bodies.append(body)
                    at_least_one = True
            if at_least_one:
                for item in recursive_bodies:
                    rules[head].remove(item)
                to_concat = list(rules[head])
                symbol = chr(k) # nueva variable para eliminar la recursividad por la izquierda
                k += 1
                while to_concat:
                    rules[head].add(to_concat.pop() + symbol)
                new_rules[symbol] = set()
                self.nonterminals.add(symbol) # hay una nueva variable no terminal
                for item in recursive_bodies:
                    new_rules[symbol].add(item[1 : len(item)]) 
                    new_rules[symbol].add(item[1 : len(item)] + symbol) 
        return new_rules # retornamos un diccionario

    def substitute(self, _bodies, body_to_change, nonterminal, count = 1):
        """ Retorna una copia de las producciones modificada con la regla de substitucion. """
        bodies = _bodies.copy()
        new_bodies = set()
        for body in self.productions[nonterminal]:
            new_bodies.add(body_to_change.replace(nonterminal, body, count))
        bodies.remove(body_to_change) # Removemos la variable a cambiar
        return bodies | new_bodies # Regresamos una union de conjuntos

    def __is_rule_gnf(self, rule):
        """ Se asume que para toda w en la regla dada cada caracter de w[1:|w|] 
            pertenece a V. """
        return all(w[0] in self.terminals for w in rule)

    def cnf_to_gnf(self): 
        """ Se asume que nos dan la gramatica en la forma normal de Chumsky """
        gnf = Grammar(self.productions, self.start)
        gnf.productions = gnf.remove_unit_productions()
        # X: An, X en N, n en naturales
        gnf.enum = dict()
        gnf.enum[gnf.start] = 1 # es neces. que S : 1 ?
        gnf.enum = { **gnf.enum, **{ item: num for num, item in enumerate(gnf.nonterminals - set(gnf.start), start = 2) } }
        gnf.__make_ascending_indexes()
        gnf.productions = { **gnf.__remove_equal_indexes(), **gnf.productions }
        while True:
            gnf_rules = list() # guardamos las variables no terminales de una produccion
            # cada cuerpo de la misma esta en la FNG.
            for head in gnf.productions:
                if gnf.__is_rule_gnf(gnf.productions[head]):
                    gnf_rules.append(head)
            if len(gnf.productions) == len(gnf_rules): # condicion que nos saca del bucle
                return gnf # retornamos una gramatica
            for head in gnf.productions:
                replaceable_bodies = list()
                for body in gnf.productions[head]:
                    if body[0] in gnf_rules:
                        replaceable_bodies.append(body)
                while replaceable_bodies: # mientras tengamos elementos
                    body = replaceable_bodies.pop()
                    gnf.productions[head] = gnf.substitute(gnf.productions[head], body, body[0])

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
        self.k = 1 # variable usada en el metodo __reduce
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
        if not self.is_cnf:
            self.fcg_to_cnf()
            self.is_cnf = True
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
    return { a + b for a in x for b in y }
