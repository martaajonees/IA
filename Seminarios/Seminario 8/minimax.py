

from juego_suma15 import *
import math

def jugadaAdversario(nodo):
    valida = False
    jugada = None
    while not valida:
        celda = int(input("Introduce la celda: "))
        jugada = tJugada(celda)
        valida = esValida(nodo, jugada)
        if not valida:
            print("\n Intenta otra posicion del tablero \n")
    nodo = aplicaJugada(nodo, jugada, -1)
    return nodo

def minimax(nodo: tEstado, jugador: int):
    jugadas = nJugadas(nodo)
    maximo = -math.inf
    mejorJugada = jugadas[0]
    for jugada in jugadas:
        if esValida(nodo, jugada):
            intento = aplicaJugada(nodo, jugada, jugador)
            max_actual = valorMin(intento, -(jugador))
            if max_actual > maximo:
                maximo = max_actual
                mejorJugada = jugada
    nodo = aplicaJugada(nodo, mejorJugada, jugador)
    return nodo

def valorMax(nodo, jugador: int):
    jugadas = nJugadas(nodo)
    if esTerminal(nodo):
        return utilidad(nodo)
    valor_max = -math.inf
    for jugada in jugadas:
        if esValida(nodo, jugada):
            valor_max = max(valor_max, valorMin(aplicaJugada(nodo, jugada, jugador), jugador))
    return valor_max


def valorMin(nodo, jugador: int):
    jugadas = nJugadas(nodo)
    if esTerminal(nodo):
        return utilidad(nodo)
    valor_min = math.inf
    for jugada in jugadas:
        if esValida(nodo, jugada):
            valor_min = min(valor_min, valorMax(aplicaJugada(nodo, jugada, jugador), jugador))
    return valor_min