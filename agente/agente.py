"""
Agente que compite contra otro
utilizando el algoritmo MiniMax.

Proyecto de la materia de Diseño de Sistemas Inteligentes.

Creadores:

- Luis Fernando Hernández Morales
- POR_CONFIRMAR
"""

import random

class AgenteJugador:
    def __init__(self, ID_WEBSOCKET):
        self.tablero = None
        self.ID = ID_WEBSOCKET
    
    def update_tablero(self, nuevo_tablero):
        self.tablero = nuevo_tablero
    
    # Reglas del agente
    ## Si es el primero en tirar, deberá hacerlo SIEMPRE
    ## en la primera casilla del tablero ( [ 0 ][ 0 ] )
    def primer_tiro(self):
        """
        Primera regla del agente, tirar siempre en la primera casilla
        si el juego acaba de empezar y si es el jugador 1.

        :return: X, Y => Posiciones del arreglo
        """
        return 0,0
    
    # Segunda regla
    ## Debe evaluar dónde es más conveniente efectuar su turno.
    ## Tratando siempre de ocupar la siguiente esquina:
    # [0][0] Esquina superior izquierda
    # [0][2] Esquina superior derecha
    # [2][0] Esquina inferior izquierda
    # [2][2] Esquina inferior derecha
    # Si alguna de esas casillas está ocupada por sí mismo o el oponente:
    # Buscar una casilla aleatoria vacía, dejémos todo a la suerte :v

    def buscar_una_esquina(self):
        if self.tablero[0][0] == None:
            return 0,0
        elif self.tablero[0][2] == None:
            return 0,2
        elif self.tablero[2][0] == None:
            return 2,0
        elif self.tablero[2][2] == None:
            return 2,2
        else:
            return None, None # Buscar hacia los lados del oponente

    def puede_ganar(self, tablero, turno):
        if tablero[0][0] == turno and tablero[0][1] == turno and tablero[0][2] == turno:
            return True
        if tablero[1][1] == turno and tablero[1][1] == turno and tablero[1][2] == turno:
            return True
        if tablero[2][1] == turno and tablero[2][1] == turno and tablero[2][2] == turno:
            return True
        if tablero[0][0] == turno and tablero[1][1] == turno and tablero[2][1] == turno:
            return True
        if tablero[0][1] == turno and tablero[1][1] == turno and tablero[2][1] == turno:
            return True
        if tablero[0][2] == turno and tablero[1][2] == turno and tablero[2][2] == turno:
            return True
        if tablero[0][0] == turno and tablero[1][1] == turno and tablero[2][2] == turno:
            return True
        if tablero[0][2] == turno and tablero[1][1] == turno and tablero[2][1] == turno:
            return True
        return False

    def evaluar_posibilidad(self, x, y):
        copia_tablero = self.tablero
        copia_tablero[x][y] = self.ID
        if self.puede_ganar(copia_tablero, self.ID):
            return 1
        
        if self.ID != 0:#Evaluar la posibilidad de victoria del oponente
            copia_tablero[x][y] = 1 # Turno del oponente
            if self.puede_ganar(copia_tablero, 1):
                return -1
        
        return 0

    def random_cell(self):
        disponibles = []
        for row in range(3):
            for col in range(3):
                if self.tablero[row][col] == None:
                    disponibles.append((row, col))
        if len(disponibles) > 0:
            indice = random.randint(0, len(disponibles)-1)
            # print(disponibles[indice])
            return disponibles[indice]
        else:
            return None, None

    
    def minimax(self):
        """
        Ponderar qué tiro me conviene realizar

        :return: '1' óptimo, '0' empate, '-1' no óptimo
        """
        # print('Evaluando posibilidades')
        default = [[None for _ in range(3)] for _ in range(3)]
        if self.tablero != default:
            # print('No es el tablero inicial')
            # No es el primer tiro, por lo que hay que evaluar el puntaje de cada casilla
            # Intenta buscar una esquina disponible
            x_, y_ = self.buscar_una_esquina()
            if x_ != None and y_ != None:
                # Si se puede efectuar un tiro en una esquina, evaluar las
                # posibilidades:
                posibilidad = self.evaluar_posibilidad(x_, y_)
                return posibilidad, x_, y_
            else:
                # Buscar una posición aletoria porque sí
                x_, y_ = self.random_cell()
                if x_ != None and y_ != None:
                    # print(f"\n\nRandom cell => {x_}, {y_}\n\n")
                    posibilidad = self.evaluar_posibilidad(x_, y_)
                    return posibilidad, x_, y_
                else:
                    return None, None, None
        else:
            # print('Tablero inicial')
            return 1, 0, 0 # Primer tiro
