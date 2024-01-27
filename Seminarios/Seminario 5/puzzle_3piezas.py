
from dataclasses import dataclass
from copy import deepcopy
import numpy as np

operadores = {"1": "ARRIBA_A", "2": "ABAJO_A", "3": "IZQUIERDA_A", "4": "DERECHA_A", 
              "5": "ARRIBA_B", "6": "ABAJO_B", "7": "IZQUIERDA_B", "8": "DERECHA_B", 
              "9": "ARRIBA_C", "10": "ABAJO_C", "11": "IZQUIERDA_C", "12": "DERECHA_C"}

@dataclass
class tEstado:
    M: np.array
    filas: list
    columnas: list
    N: int

    def __init__(self, tablero, filas, columnas):
        self.M = tablero
        self.N = self.M.shape[0]
        self.filas = filas
        self.columnas = columnas
    
    
    def crearHash(self):
        return f"{self.M.tobytes()}{self.N}{self.filas}{self.columnas}"
    
    def __str__(self):
        v = {-1: "⬛️", 0: "⬜️", 1: "🟦", 2: "🟩", 3: "🟥" }
        str = ""
        for i in range(self.N):
            for j in range(self.N):
                str += f"{v[self.M[i, j]]}"
            str += '\n'
        return  str

def heuristica(actual:tEstado) -> int:
    objetivo = estadoObjetivo()
    distancia_A = abs(actual.filas[0] - objetivo.filas[0]) + abs(actual.columnas[0] - objetivo.columnas[0])
    distancia_B = abs(actual.filas[1] - objetivo.filas[1]) + abs(actual.columnas[1] - objetivo.columnas[1])
    distancia_C = abs(actual.filas[2] - objetivo.filas[2]) + abs(actual.columnas[2] - objetivo.columnas[2])
    return distancia_A + distancia_B + distancia_C

def estadoInicial()-> tEstado:
    tablero = np.array(
        [
            [-1, 0, 0, 3, 0, 0],
            [-1, 0, 0, 3, 0, 0],
            [0, 1, 0, 3, 0, 0],
            [1, 1, 1, -1, 2, 0],
            [0, 1, 0, 2, 2, 2],
            [0, 0, 0, 0, 0, 0]
        ]
    )
    return tEstado(tablero, [3, 4, 1], [1, 4, 3])

def estadoObjetivo() -> tEstado:
    tablero = np.array(
        [
            [-1, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, -1, 0, 3],
            [1, 1, 1, 2, 0, 3],
            [0, 1, 2, 2, 2, 3]
        ]
    )
    return tEstado(tablero, [4, 5, 4], [1, 3, 5])

def testObjetivo(actual:tEstado) -> bool:
    objetivo = estadoObjetivo()
    return (actual.M == objetivo.M).all()

def esValido(op, estado:tEstado) -> bool:
    match op:
        case "1":
            return (
                estado.filas[0] > 1 and
                estado.M[estado.filas[0]-1, estado.columnas[0]-1] == 0 and
                estado.M[estado.filas[0]-1, estado.columnas[0]+1] == 0 and
                estado.M[estado.filas[0]-2, estado.columnas[0]] == 0 
            )
        case "2":
            return (
                estado.filas[0] < 4 and
                estado.M[estado.filas[0]+1, estado.columnas[0]-1] == 0 and
                estado.M[estado.filas[0]+1, estado.columnas[0]+1] == 0 and
                estado.M[estado.filas[0]+2, estado.columnas[0]] == 0
            )
        case "3":
            return (
                estado.columnas[0] > 1 and
                estado.M[estado.filas[0]-1, estado.columnas[0]-1] == 0 and
                estado.M[estado.filas[0]+1, estado.columnas[0]-1] == 0 and
                estado.M[estado.filas[0], estado.columnas[0]-2] == 0
            )
        case "4":
            return (
                estado.columnas[0] < 4 and
                estado.M[estado.filas[0]-1, estado.columnas[0]+1] == 0 and
                estado.M[estado.filas[0]+1, estado.columnas[0]+1] == 0 and
                estado.M[estado.filas[0], estado.columnas[0]+2] == 0
            )
        case "5":
            return (
                estado.filas[1] > 1 and 
                estado.M[estado.filas[1]-1, estado.columnas[1]-1] == 0 and
                estado.M[estado.filas[1]-1, estado.columnas[1]+1] == 0 and
                estado.M[estado.filas[1]-2, estado.columnas[1]] == 0
            )
        case "6":
            return (
                estado.filas[1] < 5 and 
                estado.M[estado.filas[1]+1, estado.columnas[1]-1] == 0 and
                estado.M[estado.filas[1]+1, estado.columnas[1]+1] == 0 and
                estado.M[estado.filas[1]+1, estado.columnas[1]] == 0
            )
        case "7":
            return (
                estado.columnas[1] > 1 and 
                estado.M[estado.filas[1]-1, estado.columnas[1]-1] == 0 and
                estado.M[estado.filas[1], estado.columnas[1]-2] == 0
            )
        case "8":
            return (
                estado.columnas[1] < 4 and 
                estado.M[estado.filas[1]-1, estado.columnas[1]+1] == 0 and
                estado.M[estado.filas[1], estado.columnas[1]+2] == 0
            )
        case "9":
            return (
                estado.filas[2] > 1 and 
                estado.M[estado.filas[2]-2, estado.columnas[2]] == 0
            )
        case "10":
            return (
                estado.filas[2] < 4 and 
                estado.M[estado.filas[2]+2, estado.columnas[2]] == 0
            )
        case "11":
            return (
                estado.columnas[2] > 0 and 
                estado.M[estado.filas[2]-1, estado.columnas[2]-1] == 0 and
                estado.M[estado.filas[2], estado.columnas[2]-1] == 0 and
                estado.M[estado.filas[2]+1, estado.columnas[2]-1] == 0
            )
        case "12":
            return (
                estado.columnas[2] < 5 and 
                estado.M[estado.filas[2]-1, estado.columnas[2]+1] == 0 and
                estado.M[estado.filas[2], estado.columnas[2]+1] == 0 and
                estado.M[estado.filas[2]+1, estado.columnas[2]+1] == 0
            )

def aplicaOperador(op, estado) -> tEstado:
    nuevo = deepcopy(estado)
    if esValido(op, estado):
        match op:
            case "1":
                # Mover A hacia arriba
                nuevo.M[estado.filas[0]-1, estado.columnas[0]-1] = 1 
                nuevo.M[estado.filas[0]-1, estado.columnas[0]+1] = 1 
                nuevo.M[estado.filas[0]-2, estado.columnas[0]] = 1 
                # Quita A de su posición original
                nuevo.M[estado.filas[0], estado.columnas[0]-1] = 0
                nuevo.M[estado.filas[0], estado.columnas[0]+1] = 0
                nuevo.M[estado.filas[0]+1, estado.columnas[0]] = 0
                # Actualiza posición de A
                nuevo.filas[0] -= 1
            case "2":
                # Mover A hacia abajo
                nuevo.M[estado.filas[0]+1, estado.columnas[0]-1] = 1 
                nuevo.M[estado.filas[0]+1, estado.columnas[0]+1] = 1 
                nuevo.M[estado.filas[0]+2, estado.columnas[0]] = 1
                # Quita A de su posición original
                nuevo.M[estado.filas[0], estado.columnas[0]-1] = 0
                nuevo.M[estado.filas[0], estado.columnas[0]+1] = 0
                nuevo.M[estado.filas[0]-1, estado.columnas[0]] = 0
                # Actualiza posición de A
                nuevo.filas[0] += 1
            case "3":
                # Mover A hacia la izquierda
                nuevo.M[estado.filas[0]-1, estado.columnas[0]-1] = 1 
                nuevo.M[estado.filas[0]+1, estado.columnas[0]-1] = 1 
                nuevo.M[estado.filas[0], estado.columnas[0]-2] = 1
                # Quita A de su posición original
                nuevo.M[estado.filas[0]-1, estado.columnas[0]] = 0
                nuevo.M[estado.filas[0]+1, estado.columnas[0]] = 0
                nuevo.M[estado.filas[0], estado.columnas[0]+1] = 0
                # Actualiza posición de A
                nuevo.columnas[0] -= 1
            case "4":
                # Mover A hacia la derecha
                nuevo.M[estado.filas[0]-1, estado.columnas[0]+1] = 1
                nuevo.M[estado.filas[0]+1, estado.columnas[0]+1] = 1 
                nuevo.M[estado.filas[0], estado.columnas[0]+2] = 1
                # Quita A de su posición original
                nuevo.M[estado.filas[0]-1, estado.columnas[0]] = 0
                nuevo.M[estado.filas[0]+1, estado.columnas[0]] = 0
                nuevo.M[estado.filas[0], estado.columnas[0]-1] = 0
                # Actualiza posición de A
                nuevo.columnas[0] += 1
            case "5":
                # Mover B hacia arriba
                nuevo.M[estado.filas[1]-1, estado.columnas[1]-1] = 2
                nuevo.M[estado.filas[1]-1, estado.columnas[1]+1] = 2
                nuevo.M[estado.filas[1]-2, estado.columnas[1]] = 2
                # Quita B de su posición original
                nuevo.M[estado.filas[1], estado.columnas[1]-1] = 0
                nuevo.M[estado.filas[1], estado.columnas[1]+1] = 0
                nuevo.M[estado.filas[1], estado.columnas[1]] = 0
                # Actualiza posición de B
                nuevo.filas[1] -= 1
            case "6":
                # Mover B hacia abajo
                nuevo.M[estado.filas[1]+1, estado.columnas[1]-1] = 2 
                nuevo.M[estado.filas[1]+1, estado.columnas[1]+1] = 2 
                nuevo.M[estado.filas[1]+1, estado.columnas[1]] = 2
                # Quita B de su posición original
                nuevo.M[estado.filas[1], estado.columnas[1]-1] = 0
                nuevo.M[estado.filas[1], estado.columnas[1]+1] = 0
                nuevo.M[estado.filas[1]-1, estado.columnas[1]] = 0
                # Actualiza posición de B
                nuevo.filas[1] += 1
            case "7":
                # Mover B hacia la izquierda
                nuevo.M[estado.filas[1]-1, estado.columnas[1]-1] = 2
                nuevo.M[estado.filas[1], estado.columnas[1]-2] = 2
                # Quita B de su posición original
                nuevo.M[estado.filas[1]-1, estado.columnas[1]] = 0
                nuevo.M[estado.filas[1], estado.columnas[1]+1] = 0
                # Actualiza posición de B
                nuevo.columnas[1] -= 1
            case "8":
                # Mover B hacia la derecha
                nuevo.M[estado.filas[1]-1, estado.columnas[1]+1] = 2
                nuevo.M[estado.filas[1], estado.columnas[1]+2] = 2
                # Quita B de su posición original
                nuevo.M[estado.filas[1]-1, estado.columnas[1]] = 0
                nuevo.M[estado.filas[1], estado.columnas[1]-1] = 0
                # Actualiza posición de B
                nuevo.columnas[1] += 1
            case "9":
                # Mover C hacia arriba
                nuevo.M[estado.filas[2]-2, estado.columnas[2]] = 3
                # Quita C de su posición original
                nuevo.M[estado.filas[2]+1, estado.columnas[2]] = 0
                # Actualiza posición de C
                nuevo.filas[2] -= 1
            case "10":
                # Mover C hacia abajo
                nuevo.M[estado.filas[2]+2, estado.columnas[2]] = 3
                # Quita C de su posición original
                nuevo.M[estado.filas[2]-1, estado.columnas[2]] = 0
                # Actualiza posición de C
                nuevo.filas[2] += 1
            case "11":
                # Mover C hacia la izquierda
                nuevo.M[estado.filas[2]-1, estado.columnas[2]-1] = 3
                nuevo.M[estado.filas[2], estado.columnas[2]-1] = 3
                nuevo.M[estado.filas[2]+1, estado.columnas[2]-1] = 3
                # Quita C de su posición original
                nuevo.M[estado.filas[2]-1, estado.columnas[2]] = 0
                nuevo.M[estado.filas[2], estado.columnas[2]] = 0
                nuevo.M[estado.filas[2]+1, estado.columnas[2]] = 0
                # Actualiza posición de C
                nuevo.columnas[2] -= 1
            case "12":
                # Mover C hacia la derecha
                nuevo.M[estado.filas[2]-1, estado.columnas[2]+1] = 3
                nuevo.M[estado.filas[2], estado.columnas[2]+1] = 3
                nuevo.M[estado.filas[2]+1, estado.columnas[2]+1] = 3
                # Quita C de su posición original
                nuevo.M[estado.filas[2]-1, estado.columnas[2]] = 0
                nuevo.M[estado.filas[2], estado.columnas[2]] = 0
                nuevo.M[estado.filas[2]+1, estado.columnas[2]] = 0
                # Actualiza posición de C
                nuevo.columnas[2] += 1
        return nuevo

