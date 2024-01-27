
from __future__ import annotations
from dataclasses import dataclass # para dataclass
from copy import deepcopy # para deepcopy

operadores = {"1" : "IZQUIERDA", "2" : "DERECHA"} 
# lista de operadores

@dataclass
class tEstado:
    cinta: list # cinta con el dinero 
    ladrones:int # dinero de los ladrones
    banco:int # dinero del banco
    N : int # control del tamaño

    def __init__(self, cinta):
        self.cinta = cinta
        self.ladrones = 0
        self.banco = 0
        self.N = len(cinta)
    
    def __str__(self) -> str:
        return f"{self.cinta} \n Ladrones: {self.ladrones} \t Banca: {self.banco}\n N:{self.N}"

    def crearHash(self) -> str:
        return f"{bytes(self.cinta)}{self.N}"
    
def estadoInicial() :
    inicial = [4, 3, 2, 5, 7, 1, 8, 6]
    return tEstado(inicial)

def esValido(op, estado) -> bool:
    return( estado.N > 1) and (op in operadores.keys())

def aplicaOperador(operador, estado):
    nuevo = deepcopy(estado)
    if esValido(operador, estado):
        match operador:
            case "1":
                nuevo.ladrones += nuevo.cinta.pop(0) #elimina el primero
            case "2":
                nuevo.ladrones += nuevo.cinta.pop(-1) #elimina el ultimo
        nuevo.banco += nuevo.cinta.pop(-1)
        nuevo.N -= 2
    return nuevo
    # Eliminamos el extremo derecho de la cinta

def testObjetivo(estado) -> bool:
    return (estado.N == 0) and (estado.ladrones > estado.banco)
    # Se ha acabado cuando no queda dinero en la cinta
