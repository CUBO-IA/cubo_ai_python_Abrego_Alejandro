import pygame

from src.core.settings import (
    WIDTH,
    HEIGHT,
    FPS,
    TITLE,
    BACKGROUND_COLOR
)

from src.player.player import Player
from src.world.platform import Platform
from src.camera.camera import Camera


class Game:
    """
    Controlador principal del juego.

    Responsabilidades:
    - Crear la ventana.
    - Gestionar el game loop.
    - Gestionar el nivel.
    - Gestionar checkpoints.
    - Detectar muerte y meta.
    - Dibujar mundo y HUD.
    """

    def __init__(self):

        pygame.init()

        # ==========================================================
        # VENTANA
        # ==========================================================

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()

        self.running = True

        # ==========================================================
        # FUENTES
        # ==========================================================

        self.font_title = pygame.font.SysFont(
            "Arial",
            30,
            bold=True
        )

        self.font_ui = pygame.font.SysFont(
            "Arial",
            20
        )

        self.font_big = pygame.font.SysFont(
            "Arial",
            60,
            bold=True
        )

        # ==========================================================
        # CÁMARA
        # ==========================================================

        self.camera = Camera()

        # ==========================================================
        # ESTADO DEL NIVEL
        # ==========================================================

        self.level_finished = False

        self.level_time = 0.0

        self.death_count = 0

        # ==========================================================
        # CHECKPOINTS
        # ==========================================================

        self.checkpoints = [

            (200, 500),

            (1050, 320),

            (2040, 370),

            (2900, 310),

            (3800, 220),

            (4750, 140)
        ]

        self.current_checkpoint = 0

        # ==========================================================
        # JUGADOR
        # ==========================================================

        self.player = Player(
            *self.checkpoints[
                self.current_checkpoint
            ]
        )

        # ==========================================================
        # NIVEL
        # ==========================================================

        self.platforms = []

        self.create_level()

        # ==========================================================
        # META
        # ==========================================================

        self.finish_rect = pygame.Rect(
            5000,
            100,
            120,
            120
        )

        # ==========================================================
        # LÍMITE DE MUERTE
        # ==========================================================

        self.death_height = 850

    # ==============================================================
    # CREACIÓN DEL NIVEL
    # ==============================================================

    def create_level(self):

        self.platforms = [

            # ------------------------------------------------------
            # ZONA 1 - INICIO
            # ------------------------------------------------------

            Platform(
                0,
                600,
                450,
                120
            ),

            Platform(
                560,
                520,
                180,
                40
            ),

            Platform(
                820,
                450,
                160,
                40
            ),

            # ------------------------------------------------------
            # ZONA 2 - ASCENSO
            # ------------------------------------------------------

            Platform(
                1050,
                380,
                150,
                40
            ),

            Platform(
                1270,
                320,
                180,
                40
            ),

            Platform(
                1520,
                260,
                160,
                40
            ),

            # ------------------------------------------------------
            # ZONA 3 - DESCENSO
            # ------------------------------------------------------

            Platform(
                1740,
                350,
                220,
                40
            ),

            Platform(
                2040,
                430,
                160,
                40
            ),

            Platform(
                2270,
                500,
                250,
                40
            ),

            # ------------------------------------------------------
            # ZONA 4 - SALTO LARGO
            # ------------------------------------------------------

            Platform(
                2600,
                450,
                180,
                40
            ),

            Platform(
                2900,
                370,
                180,
                40
            ),

            Platform(
                3200,
                300,
                220,
                40
            ),

            # ------------------------------------------------------
            # ZONA 5 - TORRE
            # ------------------------------------------------------

            Platform(
                3500,
                500,
                160,
                40
            ),

            Platform(
                3500,
                400,
                160,
                40
            ),

            Platform(
                3500,
                300,
                160,
                40
            ),

            Platform(
                3500,
                200,
                160,
                40
            ),

            # ------------------------------------------------------
            # ZONA 6 - FINAL
            # ------------------------------------------------------

            Platform(
                3800,
                280,
                220,
                40
            ),

            Platform(
                4100,
                380,
                200,
                40
            ),

            Platform(
                4400,
                300,
                300,
                40
            ),

            Platform(
                4750,
                220,
                350,
                40
            ),

            Platform(
                5000,
                220,
                250,
                40
            )
        ]

    # ==============================================================
    # EVENTOS
    # ==============================================================

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                self.running = False

            elif event.type == pygame.KEYDOWN:

                # ESC
                if event.key == pygame.K_ESCAPE:

                    self.running = False

                # R = reiniciar checkpoint
                elif event.key == pygame.K_r:

                    self.respawn_player()

                # ENTER = continuar después de terminar
                elif (
                    event.key == pygame.K_RETURN
                    and self.level_finished
                ):

                    self.restart_level()

    # ==============================================================
    # ACTUALIZACIÓN
    # ==============================================================

    def update(self, dt):

        # El nivel ya terminó
        if self.level_finished:

            return

        # Tiempo del nivel
        self.level_time += dt

        # Actualizar jugador
        self.player.update(
            dt,
            self.platforms
        )

        # Actualizar checkpoint
        self.update_checkpoint()

        # Comprobar muerte
        self.check_player_death()

        # Comprobar meta
        self.check_finish()

        # Cámara
        self.camera.update(
            self.player
        )

    # ==============================================================
    # CHECKPOINTS
    # ==============================================================

    def update_checkpoint(self):

        player_x = self.player.rect.centerx

        for index, checkpoint in enumerate(
            self.checkpoints
        ):

            checkpoint_x = checkpoint[0]

            if (
                player_x >= checkpoint_x
                and index > self.current_checkpoint
            ):

                self.current_checkpoint = index

    # ==============================================================
    # MUERTE
    # ==============================================================

    def check_player_death(self):

        if self.player.rect.top > self.death_height:

            self.death_count += 1

            self.respawn_player()

    # ==============================================================
    # REAPARECER
    # ==============================================================

    def respawn_player(self):

        checkpoint = self.checkpoints[
            self.current_checkpoint
        ]

        self.player.rect.x = checkpoint[0]
        self.player.rect.y = checkpoint[1]

        self.player.velocity_x = 0
        self.player.velocity_y = 0

        self.camera.x = (
            self.player.rect.centerx
            - WIDTH // 2
        )

        self.camera.y = (
            self.player.rect.centery
            - HEIGHT // 2
        )

    # ==============================================================
    # META
    # ==============================================================

    def check_finish(self):

        if self.player.rect.colliderect(
            self.finish_rect
        ):

            self.level_finished = True

    # ==============================================================
    # REINICIAR NIVEL
    # ==============================================================

    def restart_level(self):

        self.current_checkpoint = 0

        self.death_count = 0

        self.level_time = 0

        self.level_finished = False

        checkpoint = self.checkpoints[0]

        self.player.rect.x = checkpoint[0]
        self.player.rect.y = checkpoint[1]

        self.player.velocity_x = 0
        self.player.velocity_y = 0

        self.camera.x = 0
        self.camera.y = 0

    # ==============================================================
    # FONDO
    # ==============================================================

    def draw_background(self):

        self.screen.fill(
            BACKGROUND_COLOR
        )

        # ----------------------------------------------------------
        # CIELO
        # ----------------------------------------------------------

        pygame.draw.rect(
            self.screen,
            (20, 35, 65),
            (
                0,
                0,
                WIDTH,
                HEIGHT
            )
        )

        # ----------------------------------------------------------
        # LUNA / SOL
        # ----------------------------------------------------------

        pygame.draw.circle(
            self.screen,
            (255, 220, 120),
            (WIDTH - 150, 120),
            55
        )

        # ----------------------------------------------------------
        # SILUETAS DE CIUDAD
        # ----------------------------------------------------------

        buildings = [

            (0, 450, 140, 270),
            (150, 390, 180, 330),
            (350, 470, 120, 250),
            (500, 350, 180, 370),
            (700, 430, 150, 290),
            (870, 320, 200, 400),
            (1090, 420, 140, 300)
        ]

        for x, y, width, height in buildings:

            pygame.draw.rect(
                self.screen,
                (15, 25, 45),
                (
                    x,
                    y,
                    width,
                    height
                )
            )

    # ==============================================================
    # META VISUAL
    # ==============================================================

    def draw_finish(self):

        position = self.camera.apply(
            self.finish_rect
        )

        pygame.draw.rect(
            self.screen,
            (255, 200, 40),
            position,
            5
        )

        pygame.draw.line(
            self.screen,
            (255, 200, 40),
            position.topleft,
            position.bottomright,
            5
        )

        pygame.draw.line(
            self.screen,
            (255, 200, 40),
            position.topright,
            position.bottomleft,
            5
        )

    # ==============================================================
    # CHECKPOINTS VISUALES
    # ==============================================================

    def draw_checkpoints(self):

        for index, checkpoint in enumerate(
            self.checkpoints
        ):

            x = checkpoint[0]
            y = checkpoint[1]

            rect = pygame.Rect(
                x - 15,
                y - 40,
                30,
                40
            )

            position = self.camera.apply(
                rect
            )

            if index <= self.current_checkpoint:

                color = (
                    60,
                    230,
                    120
                )

            else:

                color = (
                    100,
                    100,
                    110
                )

            pygame.draw.rect(
                self.screen,
                color,
                position
            )

    # ==============================================================
    # HUD
    # ==============================================================

    def draw_hud(self):

        title = self.font_title.render(
            "PARKOUR // URBAN CHALLENGE",
            True,
            (255, 255, 255)
        )

        self.screen.blit(
            title,
            (25, 20)
        )

        # Tiempo
        minutes = int(
            self.level_time // 60
        )

        seconds = int(
            self.level_time % 60
        )

        time_text = self.font_ui.render(
            f"TIME  {minutes:02d}:{seconds:02d}",
            True,
            (230, 230, 230)
        )

        self.screen.blit(
            time_text,
            (25, 60)
        )

        # Checkpoint
        checkpoint_text = self.font_ui.render(
            f"CHECKPOINT  "
            f"{self.current_checkpoint + 1}"
            f"/{len(self.checkpoints)}",
            True,
            (100, 230, 150)
        )

        self.screen.blit(
            checkpoint_text,
            (25, 90)
        )

        # Muertes
        death_text = self.font_ui.render(
            f"FALLS  {self.death_count}",
            True,
            (255, 120, 120)
        )

        self.screen.blit(
            death_text,
            (25, 120)
        )

        # Controles
        controls = self.font_ui.render(
            "A/D  MOVE     SPACE  JUMP     "
            "R  CHECKPOINT     ESC  EXIT",
            True,
            (190, 190, 200)
        )

        self.screen.blit(
            controls,
            (
                25,
                HEIGHT - 40
            )
        )

    # ==============================================================
    # PANTALLA DE FINAL
    # ==============================================================

    def draw_finish_screen(self):

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 170)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        text = self.font_big.render(
            "LEVEL COMPLETE",
            True,
            (80, 255, 150)
        )

        text_rect = text.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2 - 50
            )
        )

        self.screen.blit(
            text,
            text_rect
        )

        info = self.font_ui.render(
            "Press ENTER to restart",
            True,
            (255, 255, 255)
        )

        info_rect = info.get_rect(
            center=(
                WIDTH // 2,
                HEIGHT // 2 + 30
            )
        )

        self.screen.blit(
            info,
            info_rect
        )

    # ==============================================================
    # RENDER
    # ==============================================================

    def draw(self):

        self.draw_background()

        # Mundo
        for platform in self.platforms:

            platform.draw(
                self.screen,
                self.camera
            )

        # Checkpoints
        self.draw_checkpoints()

        # Meta
        self.draw_finish()

        # Jugador
        self.player.draw(
            self.screen,
            self.camera
        )

        # HUD
        self.draw_hud()

        # Pantalla final
        if self.level_finished:

            self.draw_finish_screen()

        pygame.display.flip()

    # ==============================================================
    # GAME LOOP
    # ==============================================================

    def run(self):

        while self.running:

            dt = (
                self.clock.tick(FPS)
                / 1000.0
            )

            # Evitar valores enormes de dt
            dt = min(
                dt,
                0.033
            )

            self.handle_events()

            self.update(dt)

            self.draw()

        pygame.quit()
