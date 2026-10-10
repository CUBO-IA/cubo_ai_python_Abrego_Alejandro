import pygame

from src.core.settings import (
    GRAVITY,
    PLAYER_SPEED,
    PLAYER_JUMP
)


class Player:
    """
    Controlador principal del jugador.

    Sistema actual:
    - Movimiento izquierda / derecha
    - Aceleración
    - Frenado
    - Sprint
    - Salto
    - Coyote time
    - Jump buffering
    - Gravedad
    - Colisiones horizontales
    - Colisiones verticales
    - Detección de paredes
    - Estado básico del jugador
    """

    # ==========================================================
    # ESTADOS
    # ==========================================================

    IDLE = "idle"
    RUN = "run"
    SPRINT = "sprint"
    JUMP = "jump"
    FALL = "fall"
    LAND = "land"

    # ==========================================================
    # CONFIGURACIÓN
    # ==========================================================

    WIDTH = 40
    HEIGHT = 70

    # Movimiento
    ACCELERATION = 2200
    FRICTION = 2600

    MAX_SPEED = PLAYER_SPEED
    SPRINT_SPEED = PLAYER_SPEED * 1.45

    # Salto
    JUMP_FORCE = PLAYER_JUMP

    # Control aéreo
    AIR_CONTROL = 0.65

    # Coyote time
    COYOTE_TIME = 0.12

    # Jump buffer
    JUMP_BUFFER_TIME = 0.12

    # Velocidad máxima de caída
    MAX_FALL_SPEED = 1300

    def __init__(self, x, y):

        # ======================================================
        # RECTÁNGULO
        # ======================================================

        self.rect = pygame.Rect(
            x,
            y,
            self.WIDTH,
            self.HEIGHT
        )

        # ======================================================
        # VELOCIDAD
        # ======================================================

        self.velocity_x = 0.0
        self.velocity_y = 0.0

        # ======================================================
        # ESTADO
        # ======================================================

        self.state = self.IDLE

        self.on_ground = False

        self.was_on_ground = False

        # ======================================================
        # DIRECCIÓN
        # ======================================================

        self.facing = 1

        # ======================================================
        # TIMERS
        # ======================================================

        self.coyote_timer = 0.0

        self.jump_buffer_timer = 0.0

        # ======================================================
        # CONTROL
        # ======================================================

        self.jump_pressed = False

        self.sprint_pressed = False

        # ======================================================
        # DETECCIÓN DE PAREDES
        # ======================================================

        self.wall_left = False
        self.wall_right = False

    # ==========================================================
    # INPUT
    # ==========================================================

    def handle_input(self):

        keys = pygame.key.get_pressed()

        # ------------------------------------------------------
        # MOVIMIENTO
        # ------------------------------------------------------

        move_direction = 0

        if keys[pygame.K_a]:

            move_direction -= 1

        if keys[pygame.K_d]:

            move_direction += 1

        # ------------------------------------------------------
        # DIRECCIÓN
        # ------------------------------------------------------

        if move_direction < 0:

            self.facing = -1

        elif move_direction > 0:

            self.facing = 1

        # ------------------------------------------------------
        # SPRINT
        # ------------------------------------------------------

        self.sprint_pressed = (
            keys[pygame.K_LSHIFT]
            or keys[pygame.K_RSHIFT]
        )

        # ------------------------------------------------------
        # VELOCIDAD OBJETIVO
        # ------------------------------------------------------

        if self.sprint_pressed:

            target_speed = self.SPRINT_SPEED

        else:

            target_speed = self.MAX_SPEED

        target_speed *= move_direction

        # ------------------------------------------------------
        # ACELERACIÓN
        # ------------------------------------------------------

        if move_direction != 0:

            acceleration = self.ACCELERATION

            # Menor control en el aire
            if not self.on_ground:

                acceleration *= self.AIR_CONTROL

            if self.velocity_x < target_speed:

                self.velocity_x = min(
                    self.velocity_x + acceleration * self._dt,
                    target_speed
                )

            elif self.velocity_x > target_speed:

                self.velocity_x = max(
                    self.velocity_x - acceleration * self._dt,
                    target_speed
                )

        else:

            # --------------------------------------------------
            # FRENADO
            # --------------------------------------------------

            if self.velocity_x > 0:

                self.velocity_x = max(
                    0,
                    self.velocity_x
                    - self.FRICTION * self._dt
                )

            elif self.velocity_x < 0:

                self.velocity_x = min(
                    0,
                    self.velocity_x
                    + self.FRICTION * self._dt
                )

        # ------------------------------------------------------
        # SALTO
        # ------------------------------------------------------

        if keys[pygame.K_SPACE]:

            if not self.jump_pressed:

                self.jump_buffer_timer = (
                    self.JUMP_BUFFER_TIME
                )

            self.jump_pressed = True

        else:

            self.jump_pressed = False

    # ==========================================================
    # UPDATE
    # ==========================================================

    def update(self, dt, platforms):

        # Guardamos dt para los cálculos de input
        self._dt = dt

        # ------------------------------------------------------
        # INPUT
        # ------------------------------------------------------

        self.handle_input()

        # ------------------------------------------------------
        # TIMERS
        # ------------------------------------------------------

        self.update_timers(dt)

        # ------------------------------------------------------
        # SALTO
        # ------------------------------------------------------

        self.process_jump()

        # ------------------------------------------------------
        # GRAVEDAD
        # ------------------------------------------------------

        self.apply_gravity(dt)

        # ------------------------------------------------------
        # MOVIMIENTO HORIZONTAL
        # ------------------------------------------------------

        self.move_horizontal(
            dt,
            platforms
        )

        # ------------------------------------------------------
        # MOVIMIENTO VERTICAL
        # ------------------------------------------------------

        self.move_vertical(
            dt,
            platforms
        )

        # ------------------------------------------------------
        # PAREDES
        # ------------------------------------------------------

        self.detect_walls(
            platforms
        )

        # ------------------------------------------------------
        # ESTADO
        # ------------------------------------------------------

        self.update_state()

    # ==========================================================
    # TIMERS
    # ==========================================================

    def update_timers(self, dt):

        # Coyote time

        if self.on_ground:

            self.coyote_timer = self.COYOTE_TIME

        else:

            self.coyote_timer -= dt

            self.coyote_timer = max(
                0,
                self.coyote_timer
            )

        # Jump buffer

        if self.jump_buffer_timer > 0:

            self.jump_buffer_timer -= dt

            self.jump_buffer_timer = max(
                0,
                self.jump_buffer_timer
            )

    # ==========================================================
    # SALTO
    # ==========================================================

    def process_jump(self):

        can_jump = (
            self.on_ground
            or self.coyote_timer > 0
        )

        buffered_jump = (
            self.jump_buffer_timer > 0
        )

        if can_jump and buffered_jump:

            self.velocity_y = -self.JUMP_FORCE

            self.on_ground = False

            self.coyote_timer = 0

            self.jump_buffer_timer = 0

            self.state = self.JUMP

    # ==========================================================
    # GRAVEDAD
    # ==========================================================

    def apply_gravity(self, dt):

        if not self.on_ground:

            self.velocity_y += (
                GRAVITY * dt
            )

            self.velocity_y = min(
                self.velocity_y,
                self.MAX_FALL_SPEED
            )

    # ==========================================================
    # MOVIMIENTO HORIZONTAL
    # ==========================================================

    def move_horizontal(
        self,
        dt,
        platforms
    ):

        self.rect.x += int(
            self.velocity_x * dt
        )

        for platform in platforms:

            if not self.rect.colliderect(
                platform.rect
            ):
                continue

            # Movimiento hacia la derecha

            if self.velocity_x > 0:

                self.rect.right = (
                    platform.rect.left
                )

                self.velocity_x = 0

            # Movimiento hacia la izquierda

            elif self.velocity_x < 0:

                self.rect.left = (
                    platform.rect.right
                )

                self.velocity_x = 0

    # ==========================================================
    # MOVIMIENTO VERTICAL
    # ==========================================================

    def move_vertical(
        self,
        dt,
        platforms
    ):

        self.was_on_ground = (
            self.on_ground
        )

        self.rect.y += int(
            self.velocity_y * dt
        )

        self.on_ground = False

        for platform in platforms:

            if not self.rect.colliderect(
                platform.rect
            ):
                continue

            # --------------------------------------------------
            # CAÍDA / ATERRIZAJE
            # --------------------------------------------------

            if self.velocity_y > 0:

                self.rect.bottom = (
                    platform.rect.top
                )

                self.velocity_y = 0

                self.on_ground = True

            # --------------------------------------------------
            # GOLPE CONTRA TECHO
            # --------------------------------------------------

            elif self.velocity_y < 0:

                self.rect.top = (
                    platform.rect.bottom
                )

                self.velocity_y = 0

    # ==========================================================
    # DETECTAR PAREDES
    # ==========================================================

    def detect_walls(self, platforms):

        self.wall_left = False
        self.wall_right = False

        # Rectángulo ligeramente desplazado
        # para comprobar los laterales.

        left_sensor = pygame.Rect(
            self.rect.left - 3,
            self.rect.top + 10,
            3,
            self.rect.height - 20
        )

        right_sensor = pygame.Rect(
            self.rect.right,
            self.rect.top + 10,
            3,
            self.rect.height - 20
        )

        for platform in platforms:

            if left_sensor.colliderect(
                platform.rect
            ):

                self.wall_left = True

            if right_sensor.colliderect(
                platform.rect
            ):

                self.wall_right = True

    # ==========================================================
    # ESTADO
    # ==========================================================

    def update_state(self):

        if self.on_ground:

            speed = abs(
                self.velocity_x
            )

            if speed < 10:

                self.state = self.IDLE

            elif self.sprint_pressed:

                self.state = self.SPRINT

            else:

                self.state = self.RUN

        else:

            if self.velocity_y < 0:

                self.state = self.JUMP

            else:

                self.state = self.FALL

    # ==========================================================
    # DIBUJAR
    # ==========================================================

    def draw(self, screen, camera):

        position = camera.apply(
            self.rect
        )

        # ------------------------------------------------------
        # COLOR SEGÚN ESTADO
        # ------------------------------------------------------

        colors = {

            self.IDLE: (
                40,
                180,
                255
            ),

            self.RUN: (
                40,
                200,
                255
            ),

            self.SPRINT: (
                255,
                180,
                40
            ),

            self.JUMP: (
                120,
                100,
                255
            ),

            self.FALL: (
                180,
                80,
                220
            )
        }

        color = colors.get(
            self.state,
            (40, 180, 255)
        )

        # ------------------------------------------------------
        # CUERPO
        # ------------------------------------------------------

        pygame.draw.rect(
            screen,
            color,
            position
        )

        # ------------------------------------------------------
        # BORDE
        # ------------------------------------------------------

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            position,
            2
        )

        # ------------------------------------------------------
        # INDICADOR DE DIRECCIÓN
        # ------------------------------------------------------

        if self.facing > 0:

            eye_x = (
                position.centerx + 8
            )

        else:

            eye_x = (
                position.centerx - 8
            )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                eye_x,
                position.top + 18
            ),
            4
        )

        # ------------------------------------------------------
        # INDICADOR DE ESTADO
        # ------------------------------------------------------

        if self.sprint_pressed:

            pygame.draw.rect(
                screen,
                (255, 220, 60),
                (
                    position.left,
                    position.top - 6,
                    position.width,
                    4
                )
            )
