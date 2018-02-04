__author__ = 'Angel Lopez Manriquez'

import pdb
from stack import Stack

class DPDA:

    """ Implementacion de un automata de pila. """

    def __init__(self, states, q0, final, sigma, gamma, z0, epsilon = chr(949), 
        empty_stack_as_valid = True):
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
            delta: state x Sigma x Gamma -> Q x Gamma ** *

        Argumentos:
            state {int} -- Estado del automata.
            sigma {str} -- Simbolo de entrada.
            gamma {str} -- Simbolo de la pila.
        """ 
        #pdb.set_trace()
        if self.stack.empty() or gamma != self.stack.top() or (state, sigma, gamma) not in self.table:
            return None, None
        self.stack.pop()
        return self.table[(state, sigma, gamma)]

    def parse(self, word):
        state = self.q0
        stack = self.stack
        for char in word:
            if stack:
                print('\ndomain', state, char, stack.top())
                state, to_push = self.delta(state, char, stack.top())
                print('codomain', state, to_push)
                if state == None:
                    return False
                if to_push == self.epsilon:
                    print('stack', stack)
                    continue
                to_push = list(to_push)
                to_push.reverse()
                while to_push:
                    stack.push(to_push.pop())
                print('stack', stack)
            else:
                return self.empty_stack_as_valid
        return state in self.final

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