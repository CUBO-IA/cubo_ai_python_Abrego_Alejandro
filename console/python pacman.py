import os
import sys
import time
import random
import msvcrt

# ============================================================
# PAC-MAN PARA WINDOWS CMD
# Controles:
#   W / Flecha arriba
#   A / Flecha izquierda
#   S / Flecha abajo
#   D / Flecha derecha
#   P = Pausa
#   Q = Salir
# ============================================================

# ---------------- CONFIGURACIÓN ----------------

FPS = 14
FRAME_TIME = 1.0 / FPS

PACMAN = "C"
WALL = "#"
PELLET = "."
POWER = "o"
EMPTY = " "

# Mapa:
# # = pared
# . = punto
# o = power pellet
# C = posición inicial de Pac-Man
#
# El mapa debe ser rectangular.

MAP_TEMPLATE = [
    "###############################",
    "#...........#.................#",
    "#.#####.###.#.###.#####.#####.#",
    "#o#####.###.#.###.#####.#####o#",
    "#.............................#",
    "#.#####.#.###########.#.#####.#",
    "#.......#.....###.....#.......#",
    "#######.#####.###.#####.#######",
    "      #.#.............#.#      ",
    "######.#.#.###   ###.#.#######",
    "     #...#.#       #.#...#    ",
    "######.#.#.#  ###  #.#.#.######",
    "      #.#.#  #   #  #.#.#      ",
    "#######.#.## #   # ##.#.#######",
    "#...........#   #.............#",
    "#.#####.###.#####.###.#####..#",
    "#o....#...................#..o#",
    "#.###.#.#.###########.#.#.###.#",
    "#.....#.#.....###.....#.#.....#",
    "#####.#.#####.###.#####.#.#####",
    "#.............................#",
    "#.#####.###.#.###.#.###.#####.#",
    "#.......#...#.....#...#.......#",
    "#.#####.#.###########.#.#####.#",
    "#.............................#",
    "###############################",
]

# Corrección de filas para que tengan el mismo ancho.
WIDTH = max(len(row) for row in MAP_TEMPLATE)
HEIGHT = len(MAP_TEMPLATE)

MAP_TEMPLATE = [
    row.ljust(WIDTH)
    for row in MAP_TEMPLATE
]


# ---------------- COLORES CMD ----------------

class Colors:
    RESET = "\033[0m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    PINK = "\033[95m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WHITE = "\033[97m"
    MAGENTA = "\033[35m"


# ---------------- UTILIDADES ----------------

def enable_ansi():
    """
    Intenta activar colores ANSI en Windows 10/11.
    Si no funciona, el juego sigue siendo jugable.
    """
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)

        mode = ctypes.c_ulong()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
    except Exception:
        pass


def clear_screen():
    # ANSI es mucho más rápido que os.system("cls")
    sys.stdout.write("\033[2J\033[H")


def hide_cursor():
    sys.stdout.write("\033[?25l")


def show_cursor():
    sys.stdout.write("\033[?25h")


def move_cursor(x, y):
    sys.stdout.write(f"\033[{y};{x}H")


def beep():
    sys.stdout.write("\a")


# ---------------- ENTIDADES ----------------

class Entity:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.direction = (0, 0)

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = (0, 0)


class Ghost(Entity):
    def __init__(self, x, y, color, name):
        super().__init__(x, y)
        self.color = color
        self.name = name
        self.frightened = False
        self.move_timer = 0


# ---------------- JUEGO ----------------

class PacmanGame:

    def __init__(self):
        self.high_score = self.load_high_score()
        self.reset_game()

    # --------------------------------------------------------
    # HIGH SCORE
    # --------------------------------------------------------

    def load_high_score(self):
        try:
            with open("pacman_highscore.txt", "r") as f:
                return int(f.read().strip())
        except Exception:
            return 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score

        try:
            with open("pacman_highscore.txt", "w") as f:
                f.write(str(self.high_score))
        except Exception:
            pass

    # --------------------------------------------------------
    # RESET
    # --------------------------------------------------------

    def reset_game(self):

        self.board = [
            list(row)
            for row in MAP_TEMPLATE
        ]

        self.score = 0
        self.lives = 3
        self.level = 1

        self.power_timer = 0
        self.paused = False
        self.running = True

        # Buscar zonas razonables para colocar jugadores.
        self.pacman = Entity(14, 14)
        self.pacman.direction = (0, 0)

        # Fantasmas.
        self.ghosts = [
            Ghost(13, 12, Colors.RED, "Blinky"),
            Ghost(15, 12, Colors.PINK, "Pinky"),
            Ghost(13, 13, Colors.CYAN, "Inky"),
            Ghost(15, 13, Colors.MAGENTA, "Clyde"),
        ]

        # Asegurarnos de que las posiciones sean transitables.
        for entity in [self.pacman] + self.ghosts:
            if self.is_wall(entity.x, entity.y):
                self.find_free_position(entity)

        self.total_pellets = self.count_pellets()

    # --------------------------------------------------------
    # MAPA
    # --------------------------------------------------------

    def is_inside(self, x, y):
        return 0 <= y < HEIGHT and 0 <= x < WIDTH

    def is_wall(self, x, y):
        if not self.is_inside(x, y):
            return True

        return self.board[y][x] == WALL

    def is_walkable(self, x, y):
        if not self.is_inside(x, y):
            return False

        # Espacios fuera del mapa se consideran transitables
        # únicamente si forman parte del túnel.
        return self.board[y][x] != WALL

    def find_free_position(self, entity):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                if self.is_walkable(x, y):
                    entity.x = x
                    entity.y = y
                    entity.start_x = x
                    entity.start_y = y
                    return

    def count_pellets(self):
        total = 0

        for row in self.board:
            for cell in row:
                if cell in (PELLET, POWER):
                    total += 1

        return total

    # --------------------------------------------------------
    # ENTRADA
    # --------------------------------------------------------

    def read_input(self):

        if not msvcrt.kbhit():
            return None

        key = msvcrt.getwch()

        # Flechas y teclas especiales.
        if key in ("\x00", "\xe0"):
            key2 = msvcrt.getwch()

            if key2 == "H":
                return (0, -1)

            if key2 == "P":
                return (0, 1)

            if key2 == "K":
                return (-1, 0)

            if key2 == "M":
                return (1, 0)

            return None

        key = key.lower()

        if key == "w":
            return (0, -1)

        if key == "s":
            return (0, 1)

        if key == "a":
            return (-1, 0)

        if key == "d":
            return (1, 0)

        if key == "p":
            self.paused = not self.paused
            return None

        if key == "q":
            self.running = False
            return None

        return None

    # --------------------------------------------------------
    # MOVIMIENTO
    # --------------------------------------------------------

    def can_move(self, entity, direction):

        dx, dy = direction

        nx = entity.x + dx
        ny = entity.y + dy

        # Túneles laterales.
        if nx < 0:
            nx = WIDTH - 1

        if nx >= WIDTH:
            nx = 0

        return self.is_walkable(nx, ny)

    def move_entity(self, entity, direction):

        if not self.can_move(entity, direction):
            return False

        dx, dy = direction

        entity.x += dx
        entity.y += dy

        # Túneles.
        if entity.x < 0:
            entity.x = WIDTH - 1

        elif entity.x >= WIDTH:
            entity.x = 0

        return True

    # --------------------------------------------------------
    # PAC-MAN
    # --------------------------------------------------------

    def update_pacman(self):

        # Mantener dirección actual.
        if self.pacman.direction != (0, 0):
            self.move_entity(
                self.pacman,
                self.pacman.direction
            )

        x = self.pacman.x
        y = self.pacman.y

        cell = self.board[y][x]

        if cell == PELLET:
            self.score += 10
            self.board[y][x] = EMPTY

        elif cell == POWER:
            self.score += 50
            self.board[y][x] = EMPTY
            self.power_timer = FPS * 8

        # Ganar nivel.
        if self.count_pellets() == 0:
            self.level += 1
            self.score += 500
            self.new_level()

    def new_level(self):

        self.board = [
            list(row)
            for row in MAP_TEMPLATE
        ]

        self.pacman.reset()

        for ghost in self.ghosts:
            ghost.reset()

        self.power_timer = 0

        # Aumentar ligeramente la velocidad.
        self.level = min(self.level, 20)

    # --------------------------------------------------------
    # FANTASMAS
    # --------------------------------------------------------

    def get_valid_directions(self, ghost):

        directions = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        valid = []

        for direction in directions:
            if self.can_move(ghost, direction):
                valid.append(direction)

        return valid

    def distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def choose_ghost_direction(self, ghost):

        valid = self.get_valid_directions(ghost)

        if not valid:
            return ghost.direction

        # Evitar dar la vuelta salvo necesidad.
        opposite = (
            -ghost.direction[0],
            -ghost.direction[1]
        )

        if len(valid) > 1 and opposite in valid:
            valid.remove(opposite)

        # Durante power mode los fantasmas se alejan.
        frightened = self.power_timer > 0

        if frightened:
            valid.sort(
                key=lambda d:
                self.distance(
                    ghost.x + d[0],
                    ghost.y + d[1],
                    self.pacman.x,
                    self.pacman.y
                ),
                reverse=True
            )

            # Algo de aleatoriedad.
            if random.random() < 0.35:
                return random.choice(valid)

            return valid[0]

        # IA básica: buscar la posición de Pac-Man.
        valid.sort(
            key=lambda d:
            self.distance(
                ghost.x + d[0],
                ghost.y + d[1],
                self.pacman.x,
                self.pacman.y
            )
        )

        # Clyde tiene comportamiento más aleatorio.
        if ghost.name == "Clyde" and random.random() < 0.35:
            return random.choice(valid)

        # Inky tiene más variación.
        if ghost.name == "Inky" and random.random() < 0.20:
            return random.choice(valid)

        return valid[0]

    def update_ghosts(self):

        # A mayor nivel, fantasmas ligeramente más rápidos.
        chance = min(
            0.45 + self.level * 0.015,
            0.75
        )

        for ghost in self.ghosts:

            # No mover siempre todos los frames.
            if random.random() > chance:
                continue

            direction = self.choose_ghost_direction(ghost)

            ghost.direction = direction

            self.move_entity(
                ghost,
                direction
            )

    # --------------------------------------------------------
    # COLISIONES
    # --------------------------------------------------------

    def check_collisions(self):

        for ghost in self.ghosts:

            if (
                ghost.x == self.pacman.x
                and ghost.y == self.pacman.y
            ):

                if self.power_timer > 0:

                    # Fantasma comido.
                    self.score += 200

                    ghost.x = ghost.start_x
                    ghost.y = ghost.start_y
                    ghost.direction = (0, 0)

                    beep()

                else:

                    self.lives -= 1
                    beep()

                    if self.lives <= 0:
                        self.game_over()
                        return

                    self.reset_positions()
                    return

    def reset_positions(self):

        self.pacman.reset()

        for ghost in self.ghosts:
            ghost.reset()

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(self):

        if self.paused:
            return

        self.update_pacman()

        # El power mode disminuye.
        if self.power_timer > 0:
            self.power_timer -= 1

        self.update_ghosts()

        self.check_collisions()

    # --------------------------------------------------------
    # RENDER
    # --------------------------------------------------------

    def color_cell(self, cell):

        if cell == WALL:
            return Colors.BLUE + WALL + Colors.RESET

        if cell == PELLET:
            return Colors.WHITE + "." + Colors.RESET

        if cell == POWER:
            return Colors.YELLOW + "o" + Colors.RESET

        return " "

    def render(self):

        # Construir todo el frame en memoria.
        output = []

        output.append(
            Colors.YELLOW
            + "          P A C - M A N"
            + Colors.RESET
        )

        output.append(
            f"  Puntos: {self.score:<7}"
            f" Récord: {self.high_score:<7}"
            f" Nivel: {self.level:<3}"
            f" Vidas: {'♥' * self.lives}"
        )

        output.append("")

        # Crear copia visual del mapa.
        visual = [
            row[:]
            for row in self.board
        ]

        # Fantasmas.
        for ghost in self.ghosts:

            if self.power_timer > 0:
                visual[ghost.y][ghost.x] = (
                    Colors.BLUE + "G" + Colors.RESET
                )
            else:
                visual[ghost.y][ghost.x] = (
                    ghost.color + "G" + Colors.RESET
                )

        # Pac-Man encima de todo.
        visual[self.pacman.y][self.pacman.x] = (
            Colors.YELLOW + "C" + Colors.RESET
        )

        for row in visual:

            rendered = ""

            for cell in row:

                # Ya viene coloreado.
                if isinstance(cell, str) and "\033[" in cell:
                    rendered += cell
                else:
                    rendered += self.color_cell(cell)

            output.append(rendered)

        output.append("")

        if self.paused:
            output.append(
                Colors.YELLOW
                + "       *** PAUSA ***"
                + Colors.RESET
            )

        elif self.power_timer > 0:
            seconds = self.power_timer / FPS

            output.append(
                Colors.CYAN
                + f"   POWER MODE: {seconds:.1f}s"
                + Colors.RESET
            )

        else:
            output.append(
                "   WASD / FLECHAS = mover   "
                "P = pausa   Q = salir"
            )

        # Posicionar cursor al principio y dibujar.
        sys.stdout.write("\033[H")
        sys.stdout.write("\n".join(output))
        sys.stdout.write("\033[J")
        sys.stdout.flush()

    # --------------------------------------------------------
    # GAME OVER
    # --------------------------------------------------------

    def game_over(self):

        self.save_high_score()

        clear_screen()

        print()
        print("========================================")
        print("             GAME OVER")
        print("========================================")
        print()
        print(f"        PUNTUACIÓN: {self.score}")
        print(f"        RÉCORD:     {self.high_score}")
        print(f"        NIVEL:      {self.level}")
        print()
        print("        R = volver a jugar")
        print("        Q = salir")
        print()
        print("========================================")

        while True:

            key = msvcrt.getwch().lower()

            if key == "r":
                self.reset_game()
                return

            if key == "q":
                self.running = False
                return

    # --------------------------------------------------------
    # LOOP PRINCIPAL
    # --------------------------------------------------------

    def run(self):

        enable_ansi()
        hide_cursor()
        clear_screen()

        try:

            while self.running:

                frame_start = time.perf_counter()

                direction = self.read_input()

                if direction is not None:
                    self.pacman.direction = direction

                self.update()
                self.render()

                elapsed = time.perf_counter() - frame_start

                delay = FRAME_TIME - elapsed

                if delay > 0:
                    time.sleep(delay)

        finally:

            self.save_high_score()
            show_cursor()
            print()


# ============================================================
# PUNTO DE ENTRADA
# ============================================================

def main():

    game = PacmanGame()

    try:
        game.run()

    except KeyboardInterrupt:
        show_cursor()
        print("\nJuego terminado.")


if __name__ == "__main__":
    main()
