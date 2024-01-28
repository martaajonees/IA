

from dataclasses import dataclass
from copy import deepcopy
import numpy as np
from itertools import combinations

MAX = 1
MIN = -1

@dataclass
class tEstado:
    tablero: np.array
    N : int
    ocupadas : int
    turno : int

    def __init__(self, tablero, turno):
        self.tablero = tablero
        self.N = self.tablero.shape[0]
        self.ocupadas = 0
        self.turno = turno

class tJugada:
    celda: int
    def __init__(self, celda):
        self.celda = celda


# vector de posibles jugadas para funcion minimax
def nJugadas(estado: tEstado) -> list:
    jugadas = []
    for i in range(0, estado.N):
        jugadas.append(tJugada(i))
    return jugadas

# devuelve el estado inicial a partir de cualquier N
def estadoInicial(N: int) -> tEstado:
    tablero = np.zeros(N, dtype=int)
    return tEstado(tablero, MAX)

def esValida(estado: tEstado, jugada: tJugada) -> bool:
    return (
            estado.tablero[jugada.celda] == 0 and jugada.celda >= 0 
            and jugada.celda < estado.N
        )

def aplicaJugada(estado: tEstado, jugada: tJugada, jugador:int) -> tEstado:
    nuevo = deepcopy(estado)
    if esValida(estado, jugada):
        nuevo.tablero[jugada.celda] = jugador
        nuevo.ocupadas += 1
        nuevo.turno = -estado.turno
    return nuevo

# 0 si empate, 1 si gana MAX, -1 si gana MIN, None si no es terminal
def esTerminal(estado) -> int:
    terminal = None
    if estado.ocupadas == estado.N:
        terminal = 0
    else:
        # compruebo si hay alguna combinación que sume 15
        jug1 = np.where(estado.tablero == MAX)[0] + 1
        jug2 = np.where(estado.tablero == MIN)[0] + 1
        # todas las combinaciones que sumen 15
        suma15 = []
        for c in combinations(range(1, estado.N), 3):
            if sum(c) == 15:
                suma15.append(c)
        # miramos si en alguna de las combinaciones del jugador 1 suma 15
        for c in combinations(jug1, 3):
            if c in suma15:
                terminal = 1
                break
        if terminal == None:
            # miramos si en alguna de las combinaciones del jugador 2 suma 15
            for b in combinations(jug2, 3):
                if b in suma15:
                    terminal = -1  
                    break
    return terminal

# devuelve puntuacion de los nodos terminales
def utilidad(estado) -> int:
    terminal = esTerminal(estado)
    if terminal == 1:
        return 100
    elif terminal == -1:
        return -100
    else:
        return 0
