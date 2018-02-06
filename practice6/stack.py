__author__ = 'Ang3l Lopez Manriquez'

class Stack(list):
    """ Tipo abstracto de dato de tipo LIFO. Hereda de list.
    """

    def __init__(self):
        """ Inicializamos el constructor de la superclase.
        """

        super().__init__()

    def push(self, e):
        self.append(e)

    def pop(self):
        if self: # si tenemos elementos 
            return super().pop()
        raise Exception("Pila vacia")

    def top(self):
        if self:
            return self[len(self) - 1]
        raise Exception("Pila vacia")

    def size(self):
        return len(self)

    def empty(self):
        return self.size() == 0