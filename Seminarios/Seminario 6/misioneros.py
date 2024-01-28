
from dataclasses import dataclass
from copy import deepcopy
import numpy as np

operadores = { "1": "1M_izqbarca", "2": "2M_izqbarca", "3": "3M_izqbarca", 
               "4": "1C_izqbarca", "5": "2C_izqbarca", "6": "3C_izqbarca",
               "7": "1M_barcader", "8": "2M_barcader", "9": "3M_barcader",
                "10": "1C_barcader", "11": "2C_barcader", "12": "3C_barcader",
                "13": "1M_derbarca", "14": "2M_derbarca", "15": "3M_derbarca",
                "16": "1C_derbarca", "17": "2C_derbarca", "18": "3C_derbarca",
                "19": "1M_barcaizq", "20": "2M_barcaizq", "21": "3M_barcaizq",
                "22": "1C_barcaizq", "23": "2C_barcaizq", "24": "3C_barcaizq"
            }
            

@dataclass
class tEstado:
    bote: int
    bote_izq: bool
    cani_izq: int
    cani_der: int
    mis_izq: int
    mis_der: int

    def crearHash(self) -> int:
         return (
            bytes([self.bote]) +
            bytes([int(self.bote_izq)]) +
            bytes([self.cani_izq]) +
            bytes([self.cani_der]) +
            bytes([self.mis_izq]) +
            bytes([self.mis_der])
        )

    def __init__(self, bote, bote_izq, cani_izq, cani_der, mis_izq, mis_der):
        self.bote = bote
        self.bote_izq = bote_izq
        self.cani_izq = cani_izq
        self.cani_der = cani_der
        self.mis_izq = mis_izq
        self.mis_der = mis_der

    def __str__(self):
        s = ""
        s += "Bote: \n" + str(self.bote) + " personas\n"
        if self.bote_izq:
            s += "Barca en la orilla izquierda\n"
        else:
            s += "Barca en la orilla derecha\n"
        s += "Orilla derecha: \n " + str(self.mis_der) + ": Misioneros \n" + str(self.cani_der) + ": Caníbales\n"
        s += "Orilla izquierda: \n " + str(self.mis_izq) + ": Misioneros \n" + str(self.cani_izq) + ": Caníbales\n"
        return s
    
def estadoInicial()-> tEstado:
    bote = 0
    bote_izq = True # True si el bote esta en la orilla izquierda
    cani_der = 0
    mis_der = 0
    cani_izq = 3
    mis_izq = 3
    return tEstado(bote, bote_izq, cani_izq, cani_der, mis_izq, mis_der)

def heuristica(estado) -> int: 
    h1 = max(estado.mis_izq, estado.cani_izq) 
    if estado.bote_izq:
        h2 = 0
    else:
        h2 = 1
    return h1 - h2

def testObjetivo(estado) -> bool:
    # Si todos los misioneros y canibales estan en la orilla derecha
    return estado.mis_der == 3 and estado.cani_der == 3

def esValido(op, estado) -> bool:
    match op:
        case "1" | "2" | "3": # 1 misionero de la izquierda a la barca
            return (
                estado.bote_izq and estado.bote < 2 and # hay espacio en el bote
                ((estado.mis_izq - 1 > 0 and estado.mis_izq - 1 >= estado.cani_izq ) or (estado.mis_izq - 1 == 0))
            )
        case "4"| "5"| "6": # 1 canibal de la izquierda a la barca
            return (
                estado.bote_izq and estado.bote < 2 and # hay espacio en el bote
                estado.cani_izq - 1 >= 0 and 
                (estado.mis_izq >= estado.cani_izq - 1  or estado.mis_izq == 0)
            )
        case "7" |"8"| "9": # 1 misionero de la barca a la derecha
             return (
                estado.bote - 1 >= 0 and
                estado.mis_der + 1 <= 3 and
                estado.mis_der + 1 >= estado.cani_der
            )
        case "10"| "11"| "12": # 1 canibal de la barca a la derecha
            return (
                estado.bote - 1 >= 0 and
                estado.cani_der + 1 <= 3 and
                (estado.mis_der  >= estado.cani_der + 1 or estado.mis_der == 0)
            )
        case "13"| "14"| "15": # 1 misionero de la derecha a la barca
            return (
                not estado.bote_izq and estado.bote < 2 and
                ((estado.mis_der - 1 > 0 and estado.mis_der - 1 >= estado.cani_der) or (estado.mis_der - 1 == 0))
            )
        case "16"| "17"| "18": # 1 canibal de la derecha a la barca
            return (
                not estado.bote_izq and  estado.bote < 2 and
                estado.cani_der - 1 >= 0 and
                (estado.mis_der >= estado.cani_der - 1 or estado.mis_der == 0)
            )
        case "19"| "20"| "21": # 1 misionero de la barca a la izquierda
            return (
                estado.bote - 1 >= 0 and
                estado.mis_izq + 1 <= 3 and
                estado.mis_izq + 1 >= estado.cani_izq
            )
        case "22"| "23"| "24": # 1 canibal de la barca a la izquierda
            return (
                estado.bote - 1 >= 0 and
                estado.cani_izq + 1 <= 3 and
                (estado.mis_izq >= estado.cani_izq + 1 or estado.mis_izq == 0)
            )

def aplicaOperador(op, estado) -> tEstado:
    nuevo = deepcopy(estado)
    if esValido(op, estado):
        match op:
            case "1"| "2"| "3": # 1 misionero de la izquierda a la barca
                nuevo.bote += 1
                nuevo.mis_izq -= 1
            case "4"| "5"| "6": # 1 canibal de la izquierda a la barca
                nuevo.cani_izq -= 1
                nuevo.bote += 1
            case "7"| "8"| "9": # 1 misionero de la barca a la derecha
                nuevo.bote_izq = False # El bote se mueve a la derecha
                nuevo.bote -= 1
                nuevo.mis_der += 1
            case "10"| "11"| "12": # 1 canibal de la barca a la derecha
                nuevo.bote_izq = False # El bote se mueve a la derecha
                nuevo.bote -= 1
                nuevo.cani_der += 1
            case "13"| "14"| "15": # 1 misionero de la derecha a la barca
                nuevo.bote += 1
                nuevo.mis_der -= 1
            case "16"| "17"| "18": # 1 canibal de la derecha a la barca
                nuevo.bote += 1
                nuevo.cani_der -= 1
            case "19"| "20"| "21": # 1 misionero de la barca a la izquierda
                nuevo.bote_izq = True # El bote se mueve a la izquierda
                nuevo.bote -= 1
                nuevo.mis_izq += 1
            case "22"| "23"| "24": # 1 canibal de la barca a la izquierda
                nuevo.bote_izq = True # El bote se mueve a la izquierda
                nuevo.bote -= 1
                nuevo.cani_izq += 1
    return nuevo
