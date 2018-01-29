""" Segunda practica de Teoria computacional
    ========================================
    Programa que determina si un usuario ingresa una CURP valida 

    Caracteristicas
    ---------------
        Se hace uso de expresiones regulares para determinar si una cadena contiene 
    una  CURP valida.
    
    Uso
    ---
    python3 practice2.py """
    
__author__ = 'Angel Lopez Manriquez'                                                        #
__teacher__ = 'Luz Maria'

import re # se incluye la clase para trabajar expresiones regulares

''' Recordemos la estructura de la CURP: 
        Primera letra del primer apellido.
        Primera vocal del primer apellido.
        Primera letra del segundo apellido.
        Primera letra del primer nombre.
        Fecha de nacimiento sin espacios: año, mes y dı́a, cada uno con dos dı́gitos.
            El mes puede ir de 01 a 12 y el dı́a de 01 a 31.  
        Género (H para hombre, M para mujer).
        Entidad de nacimiento a dos letras. 
        Siguiente consonante del primer apellido.
        Siguiente consonante del segundo apellido.
        Siguiente consonante del primer nombre.
        Homoclave (dos dı́gitos). '''

# Algunas observaciones de expresiones regulares con python
# [abcdef] = [a|b|c|d|f] = [a-f] 
# \d = [012456789]
# [a{n}] = [aa...a] (a n-veces)
# Si se desea hacer union con | se debe de rodear la expresion con ()
def build_expression():
    """ Funcion que retorna la expresion regular para encontrar un patron para la 
        CURP. Para la construccion de la expresion se asume que todo mes tiene 31 dias.
        
        Argumentos:
            Ninguno
        
        Regresa:
                Una concatenacion (String): expresion regular concatenada con otras 
            expresiones para conformar el patron para la CURP.
            """
    first_letter_of_curp = '[A-Z][AEIOU][A-Z]{2}' 
    birthday = '\d{2}((0[1-9])|(1[0-2]))((0[1-9])|([12]\d)|(3[01]))' 
    gender = '[HM]'
    birthday_entity = '(AS|BS|CL|CS|DF|GT|HG|MC|MS|NL|PL|QR|SL|TC|TL|YN|NE|BC|CC|' + \
        'CM|CH|DG|GR|JC|MN|NT|OC|QT|SP|SR|TS|VZ|ZS)'
    following_letters = '[A-Z]{3}'
    homoclave = '\d{2}'
    return first_letter_of_curp + birthday + gender + birthday_entity + \
        following_letters + homoclave

pattern = re.compile(build_expression()) # el metodo compile recibe la expresion
word = input('Ingrese una CURP valida: ') # Obtenemos la cadena dada por teclado
ok = pattern.match(word) # Si no encontramos patron alguno ok es None
if ok is not None and len(word) == 18:
# Nos aseguramos de que la cadena contenga unicamente una CURP con esta sentencia
# toda CURP tiene 18 caracteres
    print('CURP valida')
else:
    print('CURP Invalida')