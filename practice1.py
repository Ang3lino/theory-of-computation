""" 
    Practica 1: Operaciones con cadenas
    autor: Angel Lopez Manriquez
    grupo: 2CV1
    fecha: 23/02/2018
    =================================================================================
        Programa de consola que permite realizar las siguientes operaciones:

        -longitud
        -concatenacion
        -inverso
        -potencia
        -subcadenas
        -prefijos
        -sufijos    
        -palindromo
    
    Caracteristicas ------------------------------------------------------------------
        Se hace uso de los metodos de string de python, tanto de slice (denotada por 
    corchetes [inicio:final:pasos]) como len que retorna la longitud de objeto.

        La mayoria de los metodos piden al usuario una o dos cadenas para trabajar, 
    dependiendo de la situacion.

    Uso ------------------------------------------------------------------------------
    python3 practice1.py
    (usar python practice1.py si no funciona la anterior o bien de doble clic)
"""

def length():
    """ Imprime la longitud de una cadena dada, no retornamos nada. """
    u = input('ingrese la cadena: ')
    print('longitud: ', len(u))

def concat():
    """ Concatena dos cadenas dadas y las muestra, no regresa nada. """
    u = input('ingrese la primer cadena: ')
    v = input('ingrese la segunda cadena: ')
    print('la cadena concatenada es', u + v)

def inverse():
    """ Mostramos una cadena dada al reves. No retorna nada.

        Caracteristicas: 
            Si w es una palabra entonces w[::-1] retornara w ^ {-1}
            aqui hacemos uso de el "extended slice syntax" """
    u = input('ingrese la cadena: ')
    print('La cadena invertida es: ', u[::-1])

def potency():
    """ Mostramos la potencia de una cadena dada, no retorna nada. 
    
        Caracteristicas:
            Sea w una palabra, n un entero, entonces el interprete de 
            python deducira que w * n = w + w + ... + w (n-veces) 
            para un n >= 0"""
    u = input('ingrese la cadena: ')
    n = int(input('ingrese el entero: '))
    if n < 0:   
        u = u[::-1]
        n = -n
    if n == 0:
        print('La cadena es epsilon')
    else:
        print('La cadena potencia es: ', u * n)

def sliding(w, n):
    """ Brinda todas las secuencias de longitud n de una palabra 

        Caracteristicas: 
            Con el metodo append agregamos elementos a una lista, si w es una palabra
            entonces w[a:b] con a <= b, ambos enteros, se retorna una subcadena 
            empezando por a (incluyendo) y terminando hasta b (excluyendo).

        Ejemplos:
            >>> 'hola'[1:3]
            'ol'
            >>> sliding("hola", 1)  
            [ 'h', 'o', 'l', 'a' ]
            >>> sliding("hola", 2)  [ 'ho', 'ol', 'la' ]
    
        parametros: 
            w <- string
            n <- int 

        retorna: 
            una lista de subcadenas de w de longitud n """
    words = list()
    for i, j in enumerate(range(n, len(w) + 1)): 
        words.append(w[i:j])
    return words

def substring():
    """ Muestra todas las subcadenas de una cadena dada, no retorna nada

        Caracteristicas
            Hacemos uso de la funcion sliding """
    w = input('ingrese la cadena: ')
    print('epsilon') # epsilon es subcadena para cualquier cadena
    for i in range(1, len(w) + 1):
        for u in sliding(w, i):
            print(u)

def prefixes():
    """ Muestra todos los prefijos de una cadena dada """
    w = input('ingrese la cadena: ')
    print('epsilon')
    for j in range(len(w) + 1):
        print(w[0:j])

def sufixes():
    """ Muestra todos los sufijos de una cadena dada """
    w = input('ingrese la cadena: ')
    print('epsilon')
    for i in range(len(w) + 1):
        print(w[i:len(w) + 1])

def is_palindrome():
    """ Mostramos si dos cadenas dadas son iguales """
    u = input('ingrese la primer cadena: ')
    if u == u[::-1]:
        print('La cadena es palindroma')
    else:
        print('La cadena no es palindroma')

def main(sel = 'y'):
    """ Funcion en donde preguntamos al usuario alguna accion a realizar sobre una 
        cadena dada. 
        
        Caracteristicas
            Mediante recursion nos mantendremos preguntando al usuario 
            hasta que ya quiera detener el script

        parametros 
            sel: string = Variable bandera, mientras no sea 'n' seguimos corriendo
                el programa. 
        
        Retorna
            None """
    if sel == 'y' or sel == 'Y':
        options = [ 'Longitud', 'concatenacion', 'inverso', \
                    'potencia', 'subcadenas', 'prefijos', \
                    'sufijos', 'palindromo' ]
        print() # se imprime un salto de linea
        # enumerate retorna una tupla enumerada de una coleccion
        for i, option in enumerate(options):
            print(i + 1, option) 
        sel = input("\nSeleccione: ")
        { # emulacion de un switch
            '1' : length,
            '2' : concat,
            '3' : inverse,
            '4' : potency,
            '5' : substring,
            '6' : prefixes,
            '7' : sufixes,
            '8' : is_palindrome 
        # Se mostrara 'caracter invalido' si no se escoge [1-8]
        }.get(sel, lambda: print('caracter invalido'))()
        sel = input('Desea continuar? (Y/n): ')
        main(sel)

main('y') # Arrancamos la funcion principal
