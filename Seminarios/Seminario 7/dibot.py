
from dataclasses import dataclass
from copy import deepcopy
import numpy as np

operadores = {  "1": "SupIzq",
                "2": "SupDrch",
                "3": "InfIzq",
                "4": "InfDrch",
            }

@dataclass
class tEstado:
    tablero: np.array
    N: int
    M: int
    dibot: list

    def __str__(self):
        v = {"0": "⬜️", "1": "⬛️" , "2": "🏁", "3": "🤖"}
        s = ""
        for i in range(self.N):
            for j in range(self.M):
                s += v[str(self.tablero[i][j])]
            s += "\n"
        return s
    
    def __init__(self, tablero, dibot):
        self.tablero = tablero
        self.N = self.tablero.shape[0]
        self.M = self.tablero.shape[1]
        self.dibot = dibot
    
    def crearHash(self):
        return f"{self.tablero.tobytes()}{self.dibot[0]}{self.dibot[1]}"

def coste(op, estado: tEstado) -> int:
    return 1

def heuristica(estado: tEstado) -> int:
    return abs(estado.dibot[0] - 2) + abs(estado.dibot[1] - 6)

def estadoInicial() -> tEstado:
    tablero = np.array([[3, 0, 0, 0, 1, 0, 0],
                       [0, 0, 1, 0, 0, 0, 1],
                       [0, 0, 1, 1, 0, 1, 2],
                       [0, 0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 1, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0],]
                    )
    dibot = [0, 0]
    return tEstado(tablero, dibot)


def testObjetivo(estado: tEstado) -> bool:
    return estado.dibot == [2, 6]

def esValido(op, estado: tEstado) -> bool:
    match op:
        case "1":
            return (
                estado.dibot[0] > 0 and estado.dibot[1] > 0 and
                estado.tablero[estado.dibot[0]-1, estado.dibot[1]-1] != 1 
            )
        case "2":
            return (
                estado.dibot[0] > 0 and estado.dibot[1] < estado.M -1 and
                estado.tablero[estado.dibot[0]-1, estado.dibot[1]+1] != 1
            ) 
        case "3":
            return (
                estado.dibot[0] < estado.N -1 and estado.dibot[1] > 0 and
                estado.tablero[estado.dibot[0]+1, estado.dibot[1]-1] != 1
            )
        case "4":
            return (
                estado.dibot[0] < estado.N -1 and estado.dibot[1] < estado.M -1 and
                estado.tablero[estado.dibot[0]+1, estado.dibot[1]+1] != 1
            )

def aplicaOperador(op, estado: tEstado) -> tEstado:
    nuevo = deepcopy(estado)
    if esValido(op, estado):
        match op:
            case "1":
                nuevo.tablero[estado.dibot[0], estado.dibot[1]] = 0
                nuevo.dibot[0] -= 1
                nuevo.dibot[1] -= 1
                nuevo.tablero[nuevo.dibot[0], nuevo.dibot[1]] = 3
            case "2":
                nuevo.tablero[estado.dibot[0], estado.dibot[1]] = 0
                nuevo.dibot[0] -= 1
                nuevo.dibot[1] += 1
                nuevo.tablero[nuevo.dibot[0], nuevo.dibot[1]] = 3
            case "3":
                nuevo.tablero[estado.dibot[0], estado.dibot[1]] = 0
                nuevo.dibot[0] += 1
                nuevo.dibot[1] -= 1
                nuevo.tablero[nuevo.dibot[0], nuevo.dibot[1]] = 3
            case "4":
                nuevo.tablero[estado.dibot[0], estado.dibot[1]] = 0
                nuevo.dibot[0] += 1
                nuevo.dibot[1] += 1
                nuevo.tablero[nuevo.dibot[0], nuevo.dibot[1]] = 3
    return nuevo
