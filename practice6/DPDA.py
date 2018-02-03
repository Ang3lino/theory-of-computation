__author__ = 'Ang3l Lopez Manriquez'

import pdb
from stack import Stack

class DPDA:

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

        self.stack = Stack()
        self.stack.push(z0)

    def delta(self, state, sigma, gamma):
        """ La funcion de transicion delta se define como:
            delta: state x sigma x gamma -> Q x gamma ** *

        Argumentos:
            state {int} -- Estado del automata.
            sigma {str} -- Simbolo de entrada.
            gamma {str} -- Simbolo de la pila.
        """ 

        #pdb.set_trace()
        if not self.stack.empty():
            # if any((state, sigma) in x[0:2] for x in self.table): no funciona
            if any((state, sigma) == x[0:2] for x in self.table):
                if gamma == self.stack.top():
                    self.stack.pop()
                    return self.table[(state, sigma, gamma)]
        return None, None

    def parse(self, word):
        state = self.q0
        stack = self.stack
        for char in word:
            if stack:
                print('stack', stack)
                print('domain', state, char, stack.top())
                state, to_push = self.delta(state, char, stack.top())
                print('codomain', state, to_push)
                if state == None:
                    return False
                print(to_push)
                to_push = list(to_push)
                print(to_push)
                if to_push == self.epsilon:
                    continue
                while to_push:
                    stack.push(to_push.pop())
            else:
                return False
        return True

    def add_transition(self, origin, end):
        # delta: state x sigma x gamma -> un subconjunto de Q x gamma ** *
        state = origin[0]
        sigma = origin[1]
        gamma = origin[2]

        state_out = end[0]
        gamma_out = end[1]

        if state in range(0, self.states) and sigma in self.sigma and gamma in self.gamma:
            self.table[(state, sigma, gamma)] = (state_out, gamma_out)
        else:
            raise Exception("Valores invalidos.")
