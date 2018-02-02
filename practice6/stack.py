__author__ = 'Ang3l Lopez Manriquez'

class Stack(list):
    def __init__(self):
        super().__init__()

    def push(self, e):
        self.append(e)

    def pop(self):
        if self:
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