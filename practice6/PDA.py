__author__ = 'Ang3l Lopez Manriquez'

from stack import Stack

class PDA:

    """ Implementacion de un automata de pila. """

    def __init__(self, states, q0, final, sigma, gamma, z0, epsilon = chr(949)):
        self.states = states # No. de elementos (q0, q1, ..., qn)
        self.q0 = q0
        self.final = final
        self.sigma = sigma
        self.gamma = gamma
        self.z0 = z0  
        self.epsilon = epsilon

        self.table = dict()
        for u in range(states):
            for v in sigma:
                for w in gamma:
                    self.table[(u, v, w)] = set()

        self.stack = Stack()

    def delta(self, state, sigma, gamma):
        """ La funcion de transicion delta se define como:
            delta: state x sigma x gamma -> un subconjunto de Q x gamma ** *
        
        Argumentos:
            state {int} -- Estado del automata.
            sigma {str} -- Simbolo de entrada.
            gamma {str} -- Simbolo de la pila.
        """ 

        if not self.stack.empty():
            if (state, sigma) in (self.table[0], self.table[1]):
                if gamma == self.stack.top():
                    popped = self.stack.pop()
        else:
            return False
        return self.table[(state, sigma, gamma)]


    def add_transition(self, origin, end):
        state = origin[0]
        sigma = origin[1]
        gamma = origin[2]

        state_out = end[0]
        gamma_out = end[1]

        if state in range(0, self.states) and sigma in self.sigma and gamma in self.gamma:
            self.table[(state, sigma, gamma)].add((state_out, gamma_out))
        else:
            raise Exception("Valores invalidos.")
