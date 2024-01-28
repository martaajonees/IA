
from __future__ import annotations #referenciar una clase dentro de la misma clase
from dibot2 import *
from dataclasses import dataclass

nodos_visitados = 0 # variable global que cuenta los nodos visitados
nodos_generados = 0 # variable global que cuenta los nodos generados
profundidad = 0 # variable global que cuenta la profundidad

@dataclass
class Nodo:
    estado: tEstado
    operador: str
    profundidad: int
    coste: int
    padre: Nodo

    def hash(self) -> str:
        return self.estado.crearHash()

def nodoInicial() -> Nodo:
    return Nodo(estadoInicial(), "0", 0 , 0, None)

def expandir(nodo:Nodo) -> list:
    global nodos_generados
    global profundidad
    sucesores = []
    for op in operadores.keys():
        if esValido(op, nodo.estado):
            nuevo = aplicaOperador(op, nodo.estado) # aplicamos el operador al estado del nodo
            n = Nodo(nuevo, op, nodo.profundidad + 1, nodo.coste + 1, nodo)
            if profundidad < n.profundidad:
                profundidad = n.profundidad
            nodos_generados += 1
            sucesores.append(n)
    return sucesores

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
    print("Profundidad: ", profundidad)
    
    
# 13 nodos visitados
# 14 nodos generados
def busqueda_profundidad()-> bool:
    global nodos_visitados
    objetivo = False # variable que indica si se ha encontrado el objetivo
    abiertos = []
    abiertos.append(nodoInicial()) # lista de nodos abiertos
    cerrados = {} # diccionario de nodos cerrados
    while not objetivo and len(abiertos) > 0:
        actual = abiertos.pop(0) # abrimos el primer nodo de la lista de abiertos
        nodos_visitados += 1
        if not testObjetivo(actual.estado): # comprobamos que el esado actual no sea el objetivo
            if actual.hash() not in cerrados:
                sucesores = expandir(actual) 
                abiertos = sucesores + abiertos
                cerrados[actual.hash()] = None # añadimos el nodo actual a la lista de cerrados
        else:
            objetivo = True
    if objetivo:
        dispSolucion(actual)
    else:
        print("No se ha encontrado solución")
    return objetivo

# 18 nodos visitados
# 20 nodos generados
def busqueda_anchura()->bool:
    global nodos_visitados
    objetivo = False
    abiertos = []
    cerrados = {}
    abiertos.append(nodoInicial())
    while not objetivo and len(abiertos) > 0:
        actual = abiertos.pop(0)
        nodos_visitados += 1
        if not testObjetivo(actual.estado):
            if actual.hash() not in cerrados:
                sucesores = expandir(actual)
                abiertos = abiertos + sucesores
                cerrados[actual.hash()] = None
        else:
            objetivo = True
    if objetivo:
        dispSolucion(actual)
    else:
        print("No se ha encontrado solución")
    return objetivo

def retroceso(nodo:Nodo) -> bool:
    global nodos_visitados
    global nodos_generados
    objetivo = False
    nodos_visitados += 1
    if testObjetivo(nodo.estado):
        objetivo = True
        dispSolucion(nodo)
    else:
        for sucesor in expandir(nodo):
            nodos_generados += 1
            if not objetivo:
                objetivo = retroceso(sucesor)
    return objetivo

# Nodos Visitados:  13
# Nodos Generados:  26
def busqueda_retroceso() -> bool:
    return retroceso(nodoInicial())

# Nodos Visitados:  13
# Nodos Generados:  14
def profundidad_limitada(limite:int) -> bool:
    global nodos_visitados
    objetivo = False # variable que indica si se ha encontrado el objetivo
    abiertos = []
    abiertos.append(nodoInicial()) # lista de nodos abiertos
    cerrados = {} # diccionario de nodos cerrados
    while not objetivo and len(abiertos) > 0:
        actual = abiertos.pop(0) # abrimos el primer nodo de la lista de abiertos
        nodos_visitados += 1
        if not testObjetivo(actual.estado): # comprobamos que el esado actual no sea el objetivo
            if actual.hash() not in cerrados and actual.profundidad < limite:
                sucesores = expandir(actual) 
                abiertos = sucesores + abiertos
                cerrados[actual.hash()] = None # añadimos el nodo actual a la lista de cerrados
        else:
            objetivo = True
    if objetivo:
        dispSolucion(actual)
    else:
        print("No se ha encontrado solución")
    return objetivo

# Nodos Visitados:  37
# Nodos Generados:  34
def profundidad_iterativa(limite:int) -> bool:
    objetivo = False
    cont = 0
    while not objetivo and cont < limite:
        objetivo = profundidad_limitada(limite)
        cont += 1
    return objetivo
