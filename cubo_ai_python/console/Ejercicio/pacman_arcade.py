import math
import random
import sys
import pygame

# ============================================================
# PAC-MAN ARCADE
# Python + Pygame
#
# Controles:
#   Flechas / WASD = mover
#   P             = pausa
#   ESC           = salir
#   ENTER         = iniciar / reiniciar
# ============================================================

pygame.init()

# ------------------------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------------------------

CELL = 24
HUD_HEIGHT = 100
FPS = 60

COLS = 28
ROWS = 31

WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + HUD_HEIGHT

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.DOUBLEBUF
)

pygame.display.set_caption("PAC-MAN NEON ARCADE")

clock = pygame.time.Clock()

# ------------------------------------------------------------
# COLORES
# ------------------------------------------------------------

BLACK = (3, 4, 12)
DARK_BLUE = (5, 8, 30)

BLUE = (25, 80, 255)
BRIGHT_BLUE = (50, 130, 255)
CYAN = (0, 220, 255)

YELLOW = (255, 220, 30)
WHITE = (245, 250, 255)

RED = (255, 50, 70)
PINK = (255, 100, 190)
ORANGE = (255, 150, 40)
GREEN = (70, 255, 150)

GHOST_BLUE = (70, 100, 255)

# ------------------------------------------------------------
# FUENTES
# ------------------------------------------------------------

font_small = pygame.font.SysFont(
    "consolas",
    18,
    bold=True
)

font_medium = pygame.font.SysFont(
    "consolas",
    26,
    bold=True
)

font_large = pygame.font.SysFont(
    "consolas",
    48,
    bold=True
)

font_title = pygame.font.SysFont(
    "consolas",
    64,
    bold=True
)

# ------------------------------------------------------------
# MAPA
# ------------------------------------------------------------

MAP = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#o####.#####.##.#####.####o#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "     #.#####.##.#####.#     ",
    "######.##..........##.######",
    "     #.##.###--###.##.#     ",
    "     #.##.#      #.##.#     ",
    "######.##.# ###  #.##.######",
    "#..........#   #...........#",
    "#.####.###.#####.###.####..#",
    "#o....#..............#....o#",
    "#####.#.###.####.###.#.#####",
    "    #.#.#..........#.#.#    ",
    "####.#.#.##.######.##.#.####",
    "#......#....##....##...#...#",
    "#.#########.##.#########.###",
    "#..........................#",
    "#.####.#####.##.#####.####.#",
    "#o####................####o#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.#####.##.#####.######",
    "#..........................#",
    "#.####.#####.##.#####.####.#",
    "#............##............#",
    "############################",
]

# Normalizar mapa.
MAP = [
    row[:COLS].ljust(COLS)
    for row in MAP[:ROWS]
]

# ------------------------------------------------------------
# FUNCIONES
# ------------------------------------------------------------

def tile_center(x, y):
    return (
        x * CELL + CELL // 2,
        HUD_HEIGHT + y * CELL + CELL // 2
    )


def is_wall(x, y):
    if x < 0 or x >= COLS:
        return False

    if y < 0 or y >= ROWS:
        return True

    return MAP[y][x] == "#"


def can_move(x, y, dx, dy):
    nx = x + dx
    ny = y + dy

    if nx < 0:
        nx = COLS - 1

    elif nx >= COLS:
        nx = 0

    return not is_wall(nx, ny)


def wrap_x(x):
    if x < 0:
        return COLS - 1

    if x >= COLS:
        return 0

    return x


# ------------------------------------------------------------
# PARTÍCULAS
# ------------------------------------------------------------

class Particle:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y

        angle = random.uniform(
            0,
            math.pi * 2
        )

        speed = random.uniform(
            30,
            100
        )

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.uniform(
            0.25,
            0.6
        )

        self.max_life = self.life
        self.color = color
        self.radius = random.randint(2, 4)

    def update(self, dt):

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.vy += 80 * dt

        self.life -= dt

    def draw(self, surface):

        if self.life <= 0:
            return

        alpha = int(
            255 * self.life / self.max_life
        )

        temp = pygame.Surface(
            (self.radius * 4, self.radius * 4),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            temp,
            (*self.color, alpha),
            (self.radius * 2, self.radius * 2),
            self.radius
        )

        surface.blit(
            temp,
            (
                int(self.x - self.radius * 2),
                int(self.y - self.radius * 2)
            )
        )


# ------------------------------------------------------------
# PAC-MAN
# ------------------------------------------------------------

class Pacman:

    def __init__(self):
        self.reset()

    def reset(self):

        self.x = 13
        self.y = 15

        self.direction = (0, 0)
        self.next_direction = (0, 0)

        self.mouth = 0
        self.mouth_dir = 1

        self.move_timer = 0

        self.alive = True
        self.death_timer = 0

    def update(self, dt, game):

        if not self.alive:

            self.death_timer += dt

            return

        self.move_timer += dt

        # Animación de boca.
        self.mouth += (
            self.mouth_dir
            * dt
            * 8
        )

        if self.mouth > 1:
            self.mouth = 1
            self.mouth_dir = -1

        if self.mouth < 0:
            self.mouth = 0
            self.mouth_dir = 1

        # Intentar cambiar dirección.
        if self.next_direction != (0, 0):

            if can_move(
                self.x,
                self.y,
                *self.next_direction
            ):
                self.direction = self.next_direction

        # Velocidad.
        speed = 0.105

        if self.move_timer < speed:
            return

        self.move_timer = 0

        if self.direction != (0, 0):

            dx, dy = self.direction

            if can_move(
                self.x,
                self.y,
                dx,
                dy
            ):

                self.x += dx
                self.y += dy

                self.x = wrap_x(self.x)

                game.consume(self.x, self.y)

    def draw(self, surface):

        cx, cy = tile_center(
            self.x,
            self.y
        )

        radius = CELL // 2 - 2

        # Aura.
        glow = pygame.Surface(
            (CELL * 3, CELL * 3),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (255, 220, 30, 30),
            (CELL * 1.5, CELL * 1.5),
            CELL
        )

        surface.blit(
            glow,
            (
                cx - CELL * 1.5,
                cy - CELL * 1.5
            )
        )

        # Muerte.
        if not self.alive:

            progress = min(
                self.death_timer / 1.0,
                1
            )

            start = 0.2 + progress * 0.8

            pygame.draw.arc(
                surface,
                YELLOW,
                (
                    cx - radius,
                    cy - radius,
                    radius * 2,
                    radius * 2
                ),
                math.pi * start,
                math.pi * (2 - start),
                radius
            )

            return

        # Dirección visual.
        direction = self.direction

        if direction == (0, 0):
            direction = (1, 0)

        angle = math.atan2(
            direction[1],
            direction[0]
        )

        mouth_angle = (
            0.15
            + self.mouth * 0.35
        )

        pygame.draw.circle(
            surface,
            YELLOW,
            (cx, cy),
            radius
        )

        # Boca.
        p1 = (
            cx,
            cy
        )

        p2 = (
            cx + math.cos(
                angle + mouth_angle
            ) * radius,
            cy + math.sin(
                angle + mouth_angle
            ) * radius
        )

        p3 = (
            cx + math.cos(
                angle - mouth_angle
            ) * radius,
            cy + math.sin(
                angle - mouth_angle
            ) * radius
        )

        pygame.draw.polygon(
            surface,
            BLACK,
            [p1, p2, p3]
        )


# ------------------------------------------------------------
# FANTASMA
# ------------------------------------------------------------

class Ghost:

    def __init__(
        self,
        x,
        y,
        color,
        name
    ):

        self.start_x = x
        self.start_y = y

        self.x = x
        self.y = y

        self.color = color
        self.name = name

        self.direction = random.choice([
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ])

        self.timer = 0

    def reset(self):

        self.x = self.start_x
        self.y = self.start_y

        self.direction = random.choice([
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ])

    def choose_direction(self, game):

        options = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        valid = []

        for d in options:

            if can_move(
                self.x,
                self.y,
                *d
            ):
                valid.append(d)

        if not valid:
            return self.direction

        opposite = (
            -self.direction[0],
            -self.direction[1]
        )

        if len(valid) > 1:

            valid = [
                d for d in valid
                if d != opposite
            ]

        # Power mode:
        # huir de Pac-Man.
        if game.power_mode:

            valid.sort(
                key=lambda d:
                abs(
                    self.x + d[0]
                    - game.pacman.x
                )
                +
                abs(
                    self.y + d[1]
                    - game.pacman.y
                ),
                reverse=True
            )

        else:

            # Perseguir.
            valid.sort(
                key=lambda d:
                abs(
                    self.x + d[0]
                    - game.pacman.x
                )
                +
                abs(
                    self.y + d[1]
                    - game.pacman.y
                )
            )

        # Algo de imprevisibilidad.
        if random.random() < 0.18:

            return random.choice(valid)

        return valid[0]

    def update(self, dt, game):

        self.timer += dt

        interval = (
            0.13
            if not game.power_mode
            else 0.17
        )

        if self.timer < interval:
            return

        self.timer = 0

        self.direction = self.choose_direction(
            game
        )

        dx, dy = self.direction

        if can_move(
            self.x,
            self.y,
            dx,
            dy
        ):

            self.x += dx
            self.y += dy

            self.x = wrap_x(self.x)

    def draw(self, surface, frightened):

        cx, cy = tile_center(
            self.x,
            self.y
        )

        color = (
            GHOST_BLUE
            if frightened
            else self.color
        )

        radius = CELL // 2 - 2

        # Glow.
        glow = pygame.Surface(
            (CELL * 3, CELL * 3),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            glow,
            (*color, 30),
            (CELL * 1.5, CELL * 1.5),
            CELL
        )

        surface.blit(
            glow,
            (
                cx - CELL * 1.5,
                cy - CELL * 1.5
            )
        )

        # Cabeza.
        pygame.draw.circle(
            surface,
            color,
            (cx, cy - 2),
            radius
        )

        # Cuerpo.
        body = pygame.Rect(
            cx - radius,
            cy - 2,
            radius * 2,
            radius
        )

        pygame.draw.rect(
            surface,
            color,
            body
        )

        # Ondas inferiores.
        for i in range(3):

            wx = (
                cx
                - radius
                + i * radius
            )

            pygame.draw.circle(
                surface,
                color,
                (
                    wx + radius // 2,
                    cy + radius - 2
                ),
                radius // 2
            )

        # Ojos.
        eye_y = cy - 5

        pygame.draw.circle(
            surface,
            WHITE,
            (
                cx - 6,
                eye_y
            ),
            5
        )

        pygame.draw.circle(
            surface,
            WHITE,
            (
                cx + 6,
                eye_y
            ),
            5
        )

        # Pupilas.
        dx, dy = self.direction

        pygame.draw.circle(
            surface,
            BLACK,
            (
                cx - 6 + dx * 2,
                eye_y + dy * 2
            ),
            2
        )

        pygame.draw.circle(
            surface,
            BLACK,
            (
                cx + 6 + dx * 2,
                eye_y + dy * 2
            ),
            2
        )


# ------------------------------------------------------------
# JUEGO
# ------------------------------------------------------------

class Game:

    def __init__(self):

        self.running = True

        self.state = "TITLE"

        self.score = 0
        self.high_score = 0

        self.level = 1
        self.lives = 3

        self.power_mode = False
        self.power_timer = 0

        self.flash_timer = 0

        self.particles = []

        self.pacman = Pacman()

        self.ghosts = [
            Ghost(
                12,
                13,
                RED,
                "BLINKY"
            ),

            Ghost(
                14,
                13,
                PINK,
                "PINKY"
            ),

            Ghost(
                12,
                14,
                CYAN,
                "INKY"
            ),

            Ghost(
                14,
                14,
                ORANGE,
                "CLYDE"
            )
        ]

        self.reset_pellets()

    # --------------------------------------------------------
    # PUNTOS
    # --------------------------------------------------------

    def reset_pellets(self):

        self.pellets = set()
        self.power_pellets = set()

        for y in range(ROWS):

            for x in range(COLS):

                cell = MAP[y][x]

                if cell == ".":

                    self.pellets.add(
                        (x, y)
                    )

                elif cell == "o":

                    self.power_pellets.add(
                        (x, y)
                    )

    # --------------------------------------------------------
    # CONSUMIR
    # --------------------------------------------------------

    def consume(self, x, y):

        pos = (x, y)

        if pos in self.pellets:

            self.pellets.remove(pos)

            self.score += 10

            self.spawn_particles(
                x,
                y,
                WHITE,
                3
            )

        elif pos in self.power_pellets:

            self.power_pellets.remove(pos)

            self.score += 50

            self.power_mode = True
            self.power_timer = 7

            self.spawn_particles(
                x,
                y,
                CYAN,
                14
            )

        if (
            not self.pellets
            and not self.power_pellets
        ):

            self.next_level()

    # --------------------------------------------------------
    # PARTÍCULAS
    # --------------------------------------------------------

    def spawn_particles(
        self,
        x,
        y,
        color,
        amount
    ):

        px, py = tile_center(
            x,
            y
        )

        for _ in range(amount):

            self.particles.append(
                Particle(
                    px,
                    py,
                    color
                )
            )

    # --------------------------------------------------------
    # NIVEL
    # --------------------------------------------------------

    def next_level(self):

        self.level += 1

        self.score += 500

        self.reset_pellets()

        self.pacman.reset()

        for ghost in self.ghosts:
            ghost.reset()

        self.power_mode = False
        self.power_timer = 0

    # --------------------------------------------------------
    # COLISIONES
    # --------------------------------------------------------

    def check_collisions(self):

        for ghost in self.ghosts:

            if (
                ghost.x == self.pacman.x
                and ghost.y == self.pacman.y
            ):

                if self.power_mode:

                    self.score += 200

                    self.spawn_particles(
                        ghost.x,
                        ghost.y,
                        CYAN,
                        18
                    )

                    ghost.reset()

                else:

                    self.lose_life()

                    return

    # --------------------------------------------------------
    # VIDA
    # --------------------------------------------------------

    def lose_life(self):

        self.lives -= 1

        self.pacman.alive = False
        self.pacman.death_timer = 0

        if self.lives <= 0:

            self.state = "GAMEOVER"

        else:

            pygame.time.delay(450)

            self.pacman.reset()

            for ghost in self.ghosts:
                ghost.reset()

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(self, dt):

        if self.state != "PLAYING":
            return

        self.pacman.update(
            dt,
            self
        )

        for ghost in self.ghosts:

            ghost.update(
                dt,
                self
            )

        self.check_collisions()

        # Power timer.
        if self.power_mode:

            self.power_timer -= dt

            if self.power_timer <= 0:

                self.power_timer = 0
                self.power_mode = False

        # Flash.
        if self.flash_timer > 0:

            self.flash_timer -= dt

        # Partículas.
        for particle in self.particles:

            particle.update(dt)

        self.particles = [
            p for p in self.particles
            if p.life > 0
        ]

    # --------------------------------------------------------
    # DIBUJAR MAPA
    # --------------------------------------------------------

    def draw_maze(self):

        # Fondo.
        pygame.draw.rect(
            screen,
            BLACK,
            (
                0,
                HUD_HEIGHT,
                WIDTH,
                HEIGHT
            )
        )

        # Paredes.
        for y in range(ROWS):

            for x in range(COLS):

                if MAP[y][x] != "#":
                    continue

                rect = pygame.Rect(
                    x * CELL,
                    HUD_HEIGHT + y * CELL,
                    CELL,
                    CELL
                )

                # Glow.
                glow = pygame.Surface(
                    (CELL * 3, CELL * 3),
                    pygame.SRCALPHA
                )

                pygame.draw.rect(
                    glow,
                    (20, 70, 255, 25),
                    (
                        CELL,
                        CELL,
                        CELL,
                        CELL
                    ),
                    2
                )

                screen.blit(
                    glow,
                    (
                        rect.x - CELL,
                        rect.y - CELL
                    )
                )

                pygame.draw.rect(
                    screen,
                    DARK_BLUE,
                    rect
                )

                pygame.draw.rect(
                    screen,
                    BLUE,
                    rect,
                    2
                )

                # Línea interior.
                pygame.draw.rect(
                    screen,
                    BRIGHT_BLUE,
                    rect.inflate(-5, -5),
                    1
                )

        # Puntos.
        for x, y in self.pellets:

            cx, cy = tile_center(
                x,
                y
            )

            pygame.draw.circle(
                screen,
                WHITE,
                (cx, cy),
                2
            )

        # Power pellets animadas.
        pulse = (
            math.sin(
                pygame.time.get_ticks()
                * 0.008
            )
            + 1
        ) / 2

        radius = int(
            5 + pulse * 3
        )

        for x, y in self.power_pellets:

            cx, cy = tile_center(
                x,
                y
            )

            pygame.draw.circle(
                screen,
                CYAN,
                (cx, cy),
                radius
            )

    # --------------------------------------------------------
    # HUD
    # --------------------------------------------------------

    def draw_hud(self):

        pygame.draw.rect(
            screen,
            (7, 8, 22),
            (0, 0, WIDTH, HUD_HEIGHT)
        )

        pygame.draw.line(
            screen,
            BLUE,
            (0, HUD_HEIGHT - 1),
            (WIDTH, HUD_HEIGHT - 1),
            2
        )

        score_text = font_small.render(
            "SCORE",
            True,
            CYAN
        )

        score_value = font_medium.render(
            f"{self.score:06d}",
            True,
            WHITE
        )

        high_text = font_small.render(
            "HIGH SCORE",
            True,
            CYAN
        )

        high_value = font_medium.render(
            f"{self.high_score:06d}",
            True,
            WHITE
        )

        level_text = font_small.render(
            "LEVEL",
            True,
            CYAN
        )

        level_value = font_medium.render(
            str(self.level),
            True,
            WHITE
        )

        screen.blit(
            score_text,
            (20, 12)
        )

        screen.blit(
            score_value,
            (20, 34)
        )

        screen.blit(
            high_text,
            (230, 12)
        )

        screen.blit(
            high_value,
            (230, 34)
        )

        screen.blit(
            level_text,
            (470, 12)
        )

        screen.blit(
            level_value,
            (470, 34)
        )

        # Vidas.
        for i in range(self.lives):

            x = WIDTH - 35 - i * 28

            pygame.draw.circle(
                screen,
                YELLOW,
                (x, 38),
                10
            )

            pygame.draw.polygon(
                screen,
                (7, 8, 22),
                [
                    (x, 38),
                    (x + 10, 31),
                    (x + 10, 45)
                ]
            )

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    def draw_title(self):

        screen.fill(BLACK)

        # Fondo decorativo.
        for i in range(30):

            x = random.randrange(
                0,
                WIDTH
            )

            y = random.randrange(
                HUD_HEIGHT,
                HEIGHT
            )

            pygame.draw.circle(
                screen,
                (10, 25, 70),
                (x, y),
                2
            )

        title = font_title.render(
            "PAC-MAN",
            True,
            YELLOW
        )

        subtitle = font_medium.render(
            "NEON ARCADE",
            True,
            CYAN
        )

        press = font_medium.render(
            "PRESS ENTER TO START",
            True,
            WHITE
        )

        controls = font_small.render(
            "WASD / ARROWS    P = PAUSE    ESC = EXIT",
            True,
            (140, 160, 190)
        )

        screen.blit(
            title,
            (
                WIDTH // 2
                - title.get_width() // 2,
                150
            )
        )

        screen.blit(
            subtitle,
            (
                WIDTH // 2
                - subtitle.get_width() // 2,
                225
            )
        )

        # Pac-Man decorativo.
        pygame.draw.circle(
            screen,
            YELLOW,
            (WIDTH // 2, 330),
            55
        )

        pygame.draw.polygon(
            screen,
            BLACK,
            [
                (WIDTH // 2, 330),
                (WIDTH // 2 + 55, 300),
                (WIDTH // 2 + 55, 360)
            ]
        )

        screen.blit(
            press,
            (
                WIDTH // 2
                - press.get_width() // 2,
                440
            )
        )

        screen.blit(
            controls,
            (
                WIDTH // 2
                - controls.get_width() // 2,
                490
            )
        )

    # --------------------------------------------------------
    # PAUSA
    # --------------------------------------------------------

    def draw_pause(self):

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 160)
        )

        screen.blit(
            overlay,
            (0, 0)
        )

        text = font_title.render(
            "PAUSED",
            True,
            CYAN
        )

        sub = font_small.render(
            "Press P to continue",
            True,
            WHITE
        )

        screen.blit(
            text,
            (
                WIDTH // 2
                - text.get_width() // 2,
                HEIGHT // 2 - 50
            )
        )

        screen.blit(
            sub,
            (
                WIDTH // 2
                - sub.get_width() // 2,
                HEIGHT // 2 + 25
            )
        )

    # --------------------------------------------------------
    # GAME OVER
    # --------------------------------------------------------

    def draw_gameover(self):

        screen.fill(BLACK)

        text = font_title.render(
            "GAME OVER",
            True,
            RED
        )

        score = font_medium.render(
            f"SCORE  {self.score:06d}",
            True,
            WHITE
        )

        restart = font_small.render(
            "PRESS ENTER TO PLAY AGAIN",
            True,
            CYAN
        )

        screen.blit(
            text,
            (
                WIDTH // 2
                - text.get_width() // 2,
                180
            )
        )

        screen.blit(
            score,
            (
                WIDTH // 2
                - score.get_width() // 2,
                290
            )
        )

        screen.blit(
            restart,
            (
                WIDTH // 2
                - restart.get_width() // 2,
                390
            )
        )

    # --------------------------------------------------------
    # RENDER
    # --------------------------------------------------------

    def draw(self):

        if self.state == "TITLE":

            self.draw_title()

            pygame.display.flip()

            return

        if self.state == "GAMEOVER":

            self.draw_gameover()

            pygame.display.flip()

            return

        self.draw_maze()
        self.draw_hud()

        # Partículas detrás de personajes.
        for particle in self.particles:
            particle.draw(screen)

        # Fantasmas.
        for ghost in self.ghosts:

            ghost.draw(
                screen,
                self.power_mode
            )

        # Pac-Man.
        self.pacman.draw(screen)

        if self.state == "PAUSED":
            self.draw_pause()

        pygame.display.flip()

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    def handle_input(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    self.running = False

                elif event.key == pygame.K_RETURN:

                    if self.state in (
                        "TITLE",
                        "GAMEOVER"
                    ):

                        self.score = 0
                        self.level = 1
                        self.lives = 3

                        self.reset_pellets()

                        self.pacman.reset()

                        for ghost in self.ghosts:
                            ghost.reset()

                        self.power_mode = False
                        self.state = "PLAYING"

                elif event.key == pygame.K_p:

                    if self.state == "PLAYING":

                        self.state = "PAUSED"

                    elif self.state == "PAUSED":

                        self.state = "PLAYING"

                # Movimiento.
                elif self.state == "PLAYING":

                    direction = None

                    if event.key in (
                        pygame.K_UP,
                        pygame.K_w
                    ):

                        direction = (0, -1)

                    elif event.key in (
                        pygame.K_DOWN,
                        pygame.K_s
                    ):

                        direction = (0, 1)

                    elif event.key in (
                        pygame.K_LEFT,
                        pygame.K_a
                    ):

                        direction = (-1, 0)

                    elif event.key in (
                        pygame.K_RIGHT,
                        pygame.K_d
                    ):

                        direction = (1, 0)

                    if direction:

                        self.pacman.next_direction = direction

    # --------------------------------------------------------
    # LOOP
    # --------------------------------------------------------

    def run(self):

        while self.running:

            dt = clock.tick(FPS) / 1000.0

            self.handle_input()

            self.update(dt)

            self.draw()

        pygame.quit()
        sys.exit()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    game = Game()
    game.run()
