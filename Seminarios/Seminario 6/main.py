
from misioneros import *
from busqueda_A import *
from busqueda_voraz import *
from busqueda_no_informada import *

def jugar():
    actual = estadoInicial()
    print(actual)

    while not testObjetivo(actual):
        oper = input(f"Introduce una operacion {operadores} ")
        if esValido(oper, actual):
            actual = aplicaOperador(oper, actual)
        print(actual)
        
    if testObjetivo(actual):
        print("Objetivo alcanzado") 


def main():
    mensaje = """
        Introduce una opción: 
        1. Búsqueda en profundidad
        2. Búsqueda en anchura
        3. Búsqueda con retroceso
        4. Búsqueda Profundidad limitada
        5. Búsqueda Profundidad Iterativa
        6. Búsqueda Voraz
        7. Búsqueda A*
        8. Jugar
        """
    opcion = input(mensaje)

    match opcion:
        case "1":
            resultado = busqueda_profundidad()
            if resultado:
                print("La búsqueda en profundidad fue exitosa.")
            else:
                print("La búsqueda en profundidad no fue exitosa.")
        case "2":
            resultado = busqueda_anchura()
            if resultado:
                print("La búsqueda en anchura fue exitosa.")
            else:
                print("La búsqueda en anchura no fue exitosa.")
        case "3":
            resultado = busqueda_retroceso()
            if resultado:
                print("La búsqueda con retroceso fue exitosa.")
            else:
                print("La búsqueda con retroceso no fue exitosa.")
        case "4":
            limite = int(input("Introduce el límite de profundidad: "))
            resultado = profundidad_limitada(limite)
            if resultado:
                print("La búsqueda con profundidad limitada fue exitosa.")
            else:
                print("La búsqueda con profundidad limitada no fue exitosa.")

        case "5":
            limite = int(input("Introduce el límite de profundidad: "))
            resultado = profundidad_iterativa(limite)
            if resultado:
                print("La búsqueda con profundidad iterativa fue exitosa.")
            else:
                print("La búsqueda con profundidad iterativa no fue exitosa.")
        case "6":
            resultado = busqueda_voraz()
            if resultado:
                print("La búsqueda voraz fue exitosa.")
            else:
                print("La búsqueda voraz no fue exitosa.")
        case "7":
            resultado = busqueda_A()
            if resultado:
                print("La búsqueda A* fue exitosa.")
            else:
                print("La búsqueda A* no fue exitosa.")
        case "8":
            jugar()

# Asegura que main() se ejecuta solo cuando este script se ejecuta directamente (no cuando se importa)
if __name__ == "__main__":
    main()