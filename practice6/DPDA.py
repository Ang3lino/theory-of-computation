__author__ = 'Angel Lopez Manriquez'

import pdb
from stack import Stack

class DPDA:

    """ Implementacion de un automata de pila. """

    def __init__(self, states, q0, final, sigma, gamma, z0, epsilon = chr(949), 
        empty_stack_as_valid = True, from_left = True):
        """ Para inicializar el automata de pila determinista se requiere de: 

                states[int]: el numero de estados (q0, q1, ..., qn)
                q0[int]: el id del estado inicial
                final[set]: conjunto de estados finales del automata
                sigma[set]: conjunto de variables de entrada
                gamma[set]: conjunto de variables de la pila
                z0[str]: caracter que se apilara al inicializar el automata
                epsilon[str]: caracter que representa a la cadena vacia epsilon, por 
                    defecto se pone la letra minuscula epsilon (el 949 es el valor es ASCII 
                    de este)
                empty_stack_as_valid[bool]: si este valor es True definiremos al automata tal 
                    que si en algun punto la pila es vacia la cadena es aceptada por el 
                    lenguaje generado por este
                from_left[bool]: si es True, la cadena retornada por delta sera apilada 
                    empezando por el caracter de la izquierda
        """

        self.states = states 
        self.q0 = q0
        self.final = final
        self.sigma = sigma
        self.gamma = gamma
        self.z0 = z0
        self.epsilon = epsilon

        self.table = dict() # variable en la cual se guardan los valores al ejecutar add_transition

        self.stack = Stack() # pila del programa
        self.stack.push(z0) # apilamos el caracter z0

    def delta(self, state, sigma, gamma):
        """ La funcion de transicion delta se define como:
            delta: state x Sigma x Gamma -> Q x Gamma ** *

        Argumentos:
            state {int} -- Estado del automata.
            sigma {str} -- Simbolo de entrada.
            gamma {str} -- Simbolo de la pila.
        """ 
        # si obtenemos un caracter invalido, retornamos una bina 
        if self.stack.empty() or gamma != self.stack.top() or (state, sigma, gamma) not in self.table:
            return None, None
        self.stack.pop()
        return self.table[(state, sigma, gamma)] # retornamos una cadena

    def parse(self, word):
        """ Metodo que determina si una cadena es valida por el automata de pila.
        
        Arguments:
            word {str} -- Posible palabra aceptada.
        
        Returns:
            bool -- True si pertenece, False en caso contrario.
        """

        state = self.q0
        stack = self.stack
        for char in word:
            if stack: # si la pila no esta vacia
                print('\ndomain', state, char, stack.top())
                state, to_push = self.delta(state, char, stack.top()) 
                print('codomain', state, to_push)
                if state == None: # No hay valor correspondiente para la letra actual
                    return False
                if to_push == self.epsilon: # no apilaremos nada en este paso
                    print('stack', stack)
                    continue
                to_push = list(to_push) 
                if from_left:
                    to_push.reverse()
                while to_push: # mientras la pila tenga elementos
                    stack.push(to_push.pop())
                print('stack', stack)
            else:
                return self.empty_stack_as_valid
        return state in self.final # el estado pertenece a self.final ?

    def add_transition(self, origin, end):
        """ Agregamos una transision.
        
        Arguments:
            origin {int} -- Estado de origen
            end {int} -- Estado de destino
        
        Raises:
            Exception -- Se lanzara una excepcion en caso de se quiera agregar una 
            transicion invalida.
        """

        state = origin[0]
        sigma = origin[1]
        gamma = origin[2]

        state_out = end[0]
        gamma_out = end[1]

        if state in range(0, self.states) and sigma in self.sigma and gamma in self.gamma:
            self.table[(state, sigma, gamma)] = (state_out, gamma_out)
        else:
            raise Exception("Valores invalidos.")
