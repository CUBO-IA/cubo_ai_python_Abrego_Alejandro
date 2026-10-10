import os
import random
import time
import msvcrt

# ============================================================
# PAC-MAN CONSOLE
# ============================================================

RESET = "\033[0m"
BLUE = "\033[94m"
YELLOW = "\033[93m"
WHITE = "\033[97m"
RED = "\033[91m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
GREEN = "\033[92m"

# Mapa compacto y perfectamente rectangular.
# # = pared
# . = punto
# o = superpunto
# espacio = camino
MAP_TEXT = [
    "#############################",
    "#............#..............#",
    "#.####.#####.#.#####.####.#.#",
    "#o####.#####.#.#####.####.o#",
    "#...........................#",
    "#.####.##.#########.##.####.#",
    "#......##.....#.....##......#",
    "######.#####.#.#.#####.######",
    "######.#####.#.#.#####.######",
    "#.........         .........#",
    "#.####.###         ###.####.#",
    "#o...#.               .#...o#",
    "###.#.#################.####",
    "#...#...................#...#",
    "#.###.#####.#####.#####.###.#",
    "#...........................#",
    "#############################",
]

# Normalizamos todas las filas para que tengan exactamente el mismo ancho.
WIDTH = max(len(row) for row in MAP_TEXT)

MAZE = []

for row in MAP_TEXT:
    row = row.ljust(WIDTH, "#")
    MAZE.append(list(row))

HEIGHT = len(MAZE)

# ------------------------------------------------------------
# Posiciones
# ------------------------------------------------------------

pacman_x = WIDTH // 2
pacman_y = HEIGHT - 2

# Buscar una posición libre cercana
while MAZE[pacman_y][pacman_x] == "#":
    pacman_y -= 1

ghosts = [
    {
        "x": WIDTH // 2 - 2,
        "y": 9,
        "color": RED,
    },
    {
        "x": WIDTH // 2,
        "y": 9,
        "color": MAGENTA,
    },
    {
        "x": WIDTH // 2 + 2,
        "y": 9,
        "color": CYAN,
    },
    {
        "x": WIDTH // 2 - 1,
        "y": 10,
        "color": YELLOW,
    },
]

score = 0
lives = 3
level = 1

direction = (0, -1)

mouth_open = True
paused = False
game_over = False

# ------------------------------------------------------------
# Utilidades
# ------------------------------------------------------------

def clear_screen():
    os.system("cls")


def valid_position(x, y):
    if y < 0 or y >= HEIGHT:
        return False

    if x < 0 or x >= WIDTH:
        return False

    return MAZE[y][x] != "#"


def count_dots():
    total = 0

    for row in MAZE:
        for tile in row:
            if tile in (".", "o"):
                total += 1

    return total


def reset_positions():
    global pacman_x, pacman_y

    pacman_x = WIDTH // 2
    pacman_y = HEIGHT - 2

    while not valid_position(pacman_x, pacman_y):
        pacman_y -= 1

    positions = [
        (WIDTH // 2 - 2, 9),
        (WIDTH // 2, 9),
        (WIDTH // 2 + 2, 9),
        (WIDTH // 2 - 1, 10),
    ]

    for ghost, position in zip(ghosts, positions):
        ghost["x"], ghost["y"] = position


# ------------------------------------------------------------
# Dibujado
# ------------------------------------------------------------

def draw():

    clear_screen()

    print(
        BLUE
        + "╔════════════════════════════════════════════╗"
        + RESET
    )

    print(
        BLUE
        + "║"
        + YELLOW
        + "          PAC-MAN CONSOLE EDITION          "
        + BLUE
        + "║"
        + RESET
    )

    print(
        BLUE
        + "╠════════════════════════════════════════════╣"
        + RESET
    )

    status = (
        f"SCORE {score:06d}   "
        f"LEVEL {level:02d}   "
        f"VIDAS {lives}"
    )

    print(
        BLUE
        + "║ "
        + WHITE
        + status.ljust(42)
        + BLUE
        + "║"
        + RESET
    )

    print(
        BLUE
        + "╠════════════════════════════════════════════╣"
        + RESET
    )

    for y in range(HEIGHT):

        line = ""

        for x in range(WIDTH):

            # Pac-Man
            if x == pacman_x and y == pacman_y:

                if direction == (1, 0):
                    symbol = ">"
                elif direction == (-1, 0):
                    symbol = "<"
                elif direction == (0, -1):
                    symbol = "^"
                else:
                    symbol = "v"

                if not mouth_open:
                    symbol = "●"

                line += YELLOW + symbol + RESET
                continue

            # Fantasmas
            ghost_found = None

            for ghost in ghosts:

                if ghost["x"] == x and ghost["y"] == y:
                    ghost_found = ghost
                    break

            if ghost_found:

                line += ghost_found["color"] + "M" + RESET
                continue

            tile = MAZE[y][x]

            if tile == "#":
                line += BLUE + "█" + RESET

            elif tile == ".":
                line += WHITE + "·" + RESET

            elif tile == "o":
                line += MAGENTA + "●" + RESET

            else:
                line += " "

        print(BLUE + "║" + RESET + line + BLUE + "║" + RESET)

    print(
        BLUE
        + "╠════════════════════════════════════════════╣"
        + RESET
    )

    print(
        BLUE
        + "║ "
        + GREEN
        + "WASD/FLECHAS"
        + RESET
        + " mover   "
        + CYAN
        + "P"
        + RESET
        + " pausa   "
        + RED
        + "Q"
        + RESET
        + " salir "
        + BLUE
        + "║"
        + RESET
    )

    print(
        BLUE
        + "╚════════════════════════════════════════════╝"
        + RESET
    )


# ------------------------------------------------------------
# Movimiento Pac-Man
# ------------------------------------------------------------

def move_pacman(dx, dy):

    global pacman_x
    global pacman_y
    global score

    nx = pacman_x + dx
    ny = pacman_y + dy

    if not valid_position(nx, ny):
        return

    pacman_x = nx
    pacman_y = ny

    tile = MAZE[ny][nx]

    if tile == ".":
        score += 10
        MAZE[ny][nx] = " "

    elif tile == "o":
        score += 50
        MAZE[ny][nx] = " "


# ------------------------------------------------------------
# Fantasmas
# ------------------------------------------------------------

def move_ghost(ghost):

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]

    possible = []

    for dx, dy in directions:

        nx = ghost["x"] + dx
        ny = ghost["y"] + dy

        if valid_position(nx, ny):
            possible.append((nx, ny))

    if not possible:
        return

    # Persecución simple
    possible.sort(
        key=lambda p:
        abs(p[0] - pacman_x)
        + abs(p[1] - pacman_y)
    )

    # 70% persecución / 30% aleatorio
    if random.random() < 0.70:
        choice = possible[0]
    else:
        choice = random.choice(possible)

    ghost["x"], ghost["y"] = choice


# ------------------------------------------------------------
# Colisiones
# ------------------------------------------------------------

def check_collision():

    global lives
    global game_over

    for ghost in ghosts:

        if ghost["x"] == pacman_x and ghost["y"] == pacman_y:

            lives -= 1

            if lives <= 0:
                game_over = True
            else:
                reset_positions()

            return


# ------------------------------------------------------------
# Teclado
# ------------------------------------------------------------

def read_keyboard():

    global direction
    global paused
    global game_over

    if not msvcrt.kbhit():
        return

    key = msvcrt.getch()

    # Flechas
    if key == b"\xe0":

        key = msvcrt.getch()

        if key == b"H":
            direction = (0, -1)

        elif key == b"P":
            direction = (0, 1)

        elif key == b"K":
            direction = (-1, 0)

        elif key == b"M":
            direction = (1, 0)

        return

    try:
        key = key.decode().lower()
    except UnicodeDecodeError:
        return

    if key == "w":
        direction = (0, -1)

    elif key == "s":
        direction = (0, 1)

    elif key == "a":
        direction = (-1, 0)

    elif key == "d":
        direction = (1, 0)

    elif key == "p":
        paused = not paused

    elif key == "q":
        game_over = True


# ------------------------------------------------------------
# Pantallas
# ------------------------------------------------------------

def game_over_screen():

    clear_screen()

    print()
    print(RED + "╔══════════════════════════════════════╗" + RESET)
    print(RED + "║                                      ║" + RESET)
    print(RED + "║              GAME OVER               ║" + RESET)
    print(RED + "║                                      ║" + RESET)
    print(
        RED
        + f"║          SCORE: {score:<10}          ║"
        + RESET
    )
    print(
        RED
        + f"║          LEVEL: {level:<10}          ║"
        + RESET
    )
    print(RED + "║                                      ║" + RESET)
    print(RED + "║        Pulsa Q para salir            ║" + RESET)
    print(RED + "║                                      ║" + RESET)
    print(RED + "╚══════════════════════════════════════╝" + RESET)

    while True:

        if msvcrt.kbhit():

            key = msvcrt.getch().lower()

            if key == b"q":
                break

        time.sleep(0.05)


# ------------------------------------------------------------
# Bucle principal
# ------------------------------------------------------------

def main():

    global mouth_open
    global level

    last_frame = time.time()
    last_ghost_move = time.time()

    draw()

    while not game_over:

        read_keyboard()

        if paused:
            time.sleep(0.05)
            continue

        now = time.time()

        # Pac-Man
        if now - last_frame >= 0.10:

            move_pacman(*direction)

            mouth_open = not mouth_open

            last_frame = now

        # Fantasmas
        ghost_speed = max(
            0.18,
            0.35 - level * 0.015
        )

        if now - last_ghost_move >= ghost_speed:

            for ghost in ghosts:
                move_ghost(ghost)

            last_ghost_move = now

        check_collision()

        # Nuevo nivel
        if count_dots() == 0:

            level += 1
            score += 500

            # Reiniciar puntos
            for y in range(HEIGHT):
                for x in range(WIDTH):

                    if MAP_TEXT[y][x] in (".", "o"):
                        MAZE[y][x] = MAP_TEXT[y][x]

            reset_positions()

        draw()

        time.sleep(0.01)

    game_over_screen()


if __name__ == "__main__":
    main()
