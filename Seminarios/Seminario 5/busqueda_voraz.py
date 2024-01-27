from __future__ import annotations
from dataclasses import dataclass
from puzzle_3piezas import *

nodos_visitados = 0
nodos_generados = 0

@dataclass
class Nodo:
    estado: tEstado
    operador: str
    profundidad: int
    coste: int
    heuristica: int
    padre: Nodo

    def crearHash(self):
        return self.estado.crearHash()

    def __lt__(self, estado) -> bool:
        return self.heuristica < estado.heuristica

def nodoInicial() -> Nodo:
    return Nodo (estadoInicial(), "0", 0, 0, 0, None)

def dispCamino(nodo):
    lista = []
    aux = nodo
    while aux.padre != None:
        lista.append((aux.estado, aux.operador))
        aux = aux.padre
    print("Estado inicial: ")
    print(nodoInicial().estado)
    for i in lista[::-1]:
        print("Movimiento hacia: ", operadores[i[1]], "\n")
        print(i[0])
        print()


def dispSolucion(nodo):
    dispCamino(nodo)
    print("Profundidad: ", nodo.profundidad)
    print("Coste: ", nodo.coste)
    print("Nodos Visitados: ", nodos_visitados)
    print("Nodos Generados: ", nodos_generados)

def expandir(nodo:Nodo) -> list:
    global nodos_generados
    sucesores = []
    for op in operadores.keys():
        if esValido(op, nodo.estado):
            nuevo = aplicaOperador(op, nodo.estado)
            heur = heuristica(nuevo)
            n = Nodo(nuevo, op, nodo.profundidad + 1, nodo.coste + 1, heur, nodo)
            sucesores.append(n)
            nodos_generados += 1
    return sucesores

def busqueda_voraz() -> bool:
    global nodos_visitados
    objetivo = False
    abiertos = []
    abiertos.append(nodoInicial())
    cerrados = {}
    while len(abiertos) != 0 and not objetivo:
        actual = abiertos.pop(0)
        nodos_visitados += 1
        if not testObjetivo(actual.estado):
            if actual.crearHash() not in cerrados:
                sucesores = expandir(actual)
                abiertos = abiertos + sucesores
                abiertos.sort()
                cerrados[actual.crearHash()] = None
        else:
            objetivo = True
    if objetivo:
        dispSolucion(actual)
    else:
        print("No se ha encontrado solución")
    return objetivo

