

from busqueda_voraz import *
from busqueda_A import *
from puzzle_3piezas import *

def jugar():
    actual = estadoInicial()
    print(actual)

    while not testObjetivo(actual) and actual.N > 1:
        oper = str(input(f"Introduce una operacion {operadores} "))
        if esValido(oper, actual):
            actual = aplicaOperador(oper, actual)
        print(actual)
        
    if testObjetivo(actual):
        print("Objetivo alcanzado") 

def main():
    mensaje = """
    Introduce una opción: 
    1. Búsqueda voraz
    2. Búsqueda A*
    3. Jugar
    """
    opcion = input(mensaje)
    match opcion:
        case "1":
            busqueda_voraz()
        case "2":
            busqueda_A()
        case "3":
            jugar()
        case _:
            print("Opción no válida")
            main()

if __name__ == "__main__":
    main()
