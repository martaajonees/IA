from minimax import *

N = int(input("Introduzca el tamaño del tablero: "))
ganador = 0
jugador = int(input("Introduzca el 1er jugador: 1 AI, 2 Tú "))

if jugador != 1:
    jugador = -1

juego = estadoInicial(N)
while juego.ocupadas < N and not ganador:
    if jugador == 1:
        juego = minimax(juego, jugador)
    else:
        juego = jugadaAdversario(juego)
    print(juego)
    if esTerminal(juego):
        ganador = utilidad(juego)
    jugador = -(jugador)

match ganador:
    case 0:
        print("EMPATE")
    case 100:
        print("GANA MAX (IA)")
    case -100:
        print("GANA MIN (JUGADOR)")