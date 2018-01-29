""" Tercera practica de Teoria computacional
    ========================================
    Programa que valida la expresion regular "[12][0-2]((0[1-9])|(1[0-3]))"

    Caracteristicas:
    ---------------
        Se hace uso de un automata finito determinista.
    Uso:
    ---
        Con los archivos main.py y Automata.py en el mismo directorio, ejecutar el comando:
            python3 main.py """

__author__ = "Angel Lopez Manriquez"
__teacher__ = "Luz Maria Sanchez Garcia"
 
from Automata import FDA # importamos la clase FDA del modulo Automata 

fda = FDA({ x for x in range(6 + 1) }, # Estados
            [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9' ], # Alfabeto
            [[ 6 ,  1 ,  1 ,  6 ,  6 ,  6 ,  6 ,  6 ,  6 ,  6 ], # Tabla de transicion
             [ 2 ,  2 ,  2 ,  6 ,  6 ,  6 ,  6 ,  6 ,  6 ,  6 ],
             [ 3 ,  4 ,  6 ,  6 ,  6 ,  6 ,  6 ,  6 ,  6 ,  6 ],
             [ 6 ,  5 ,  5 ,  5 ,  5 ,  5 ,  5 ,  5 ,  5 ,  5 ],
             [ 5 ,  5 ,  5 ,  5 ,  6 ,  6 ,  6 ,  6 ,  6 ,  6 ],
             [ 6 for i in range(10) ], # listas de longitud 10 donde cada elemento es 6
             [ 6 for i in range(10) ]], # 
            0, # Estado inicial
            { 5 }) # Estado(s) final
#expr = input("Ingrese una expresion regular de la forma [12][0-2]((0[1-9])|(1[0-3])): ") 
expr = "1214"
print(fda.validate(expr)) 
print(fda.transition_delta(expr)) 
