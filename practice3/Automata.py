class FDA:
    """ A = (Q, \Sigma, \delta, q_0, F)  
        Clase que emula a un automata finito determinista. """

    def __init__(self, states, sigma, transitionTable, initial, final):
        """ Define al automata finito no determinista.

            Argumentos: 
                states: Set[Int]
                sigma: List[Int]
                transitionTable: List[List[Int]]
                initialState: Int
                finalState: Set[Int] """
        self.states = states
        self.sigma = sigma
        self.transitionTable = transitionTable
        self.initialState = initial
        self.finalStates = final

    def delta(self, q, c):
        """ Se espera que, dada la tabla de transicion exista (q, c) para todo q en Q talque 
                delta(q, c) = Q
            delta: (q, c) -> q, None  
            donde: 
                q: int
                c: string, se espera que |c| = 1 """
        if q in self.states and c in self.sigma:
            return self.transitionTable[q][self.sigma.index(c)]
        return None # Esta linea no es necesaria, pues python retorna None en caso de que
        # no lo indiquemos explicitamente

    def belongs_alphabet(self, expr):
        """ Determina si una expresion pertenece al alfabeto dado.
                belongs_alphabet: (expr) -> bool
            donde:  
                expr: string """
        exprSet = set(expr)
        for x in exprSet:
            if x not in self.sigma:
                return False
        return True

    def validate(self, expr): 
        """ Determina si expr pertenece al lenguaje generado por el propio automata.
                validate: (expr) -> bool
            donde: 
                expr: string """
        begin = self.initialState
        if self.belongs_alphabet(expr):
            n = self.delta(begin, expr[0])
            for i in range(1, len(expr)):
                n = self.delta(n, expr[i])
            return n in self.finalStates
        return False

    def transition_delta(self, expr):
        """ Hace lo mismo que el metodo validate, pero de forma recursiva. """
        def helper(w, i, q): # Python soporta funciones internas, esta es una
            if i == len(w):
                return q in self.finalStates
            else:
                j = i + 1
                return helper(w, j, self.delta(q, w[i]))
        return helper(expr, 0, self.initialState)
