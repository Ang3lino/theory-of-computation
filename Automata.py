class Automata:
    """ $ A = (Q, \sigma, \delta, q_0, F) $ """

    def __init__(self, states, sigma, transitionTable, initial, final):
        self.states = states
        self.sigma = sigma
        self.transitionTable = transitionTable
        self.initialStates = initial
        self.finalStates = final

    def delta(self, q, c):
        if q in self.states and c in self.sigma:
            return self.transitionTable[q][self.sigma.index(c)]
        return None

    def belongsAlphabet(self, expr):
        exprSet = set(expr)
        for x in exprSet:
            if x not in self.sigma:
                return False
        return True

    def isValid(self, expr, begin = 0): # aqui mero 
        if self.belongsAlphabet(expr):
            n = self.delta(begin, expr[0])
            for i in range(1, len(expr)):
                n = self.delta(n, expr[i])
            return n in self.finalStates
        return False
