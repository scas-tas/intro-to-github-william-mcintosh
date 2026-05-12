# Battleship - 2 Player Pygame Edition
# Run: python battleship_pygame.py
# Requires: pip install pygame

import pygame
import sys
import random
import math
import time

# ─────────────────────────────────────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────────────────────────────────────
BOARD_SIZE   = 10
CELL         = 44
MARGIN       = 14
GAP          = 80
LABEL_W      = 24
GRID_PX      = BOARD_SIZE * CELL
BOARD_AREA_W = LABEL_W + GRID_PX
WIN_W        = MARGIN * 2 + BOARD_AREA_W * 2 + GAP
WIN_H        = 720

SHIPS = [
    ("Carrier",    5),
    ("Battleship", 4),
    ("Cruiser",    3),
    ("Submarine",  3),
    ("Destroyer",  2),
]
TOTAL_SHIP_CELLS = sum(s for _, s in SHIPS)
COLS = "ABCDEFGHIJ"

# Cell states
EMPTY = 0
SHIP  = 1
HIT   = 2
MISS  = 3

# Colours
NAVY        = (10,  24,  48)
NAVY_MID    = (18,  42,  80)
NAVY_LIGHT  = (28,  62, 110)
STEEL       = (52,  88, 130)
OCEAN_DARK  = (12,  56,  96)
OCEAN_MID   = (20,  90, 140)
OCEAN_LIGHT = (40, 140, 190)
FOAM        = (180, 220, 240)
WHITE       = (240, 245, 255)
GOLD        = (220, 170,  50)
GOLD_LIGHT  = (255, 215,  80)
RED         = (200,  50,  50)
RED_BRIGHT  = (255,  80,  60)
GREEN_LIGHT = (100, 220, 120)
GREY        = ( 90, 110, 130)
GREY_LIGHT  = (140, 165, 190)
MISS_BLUE   = ( 60, 120, 170)
HIT_ORANGE  = (220, 100,  30)

# Game states
S_MENU    = "menu"
S_SETUP   = "setup"
S_PLACE   = "place"
S_HANDOFF = "handoff"
S_BATTLE  = "battle"
S_VICTORY = "victory"


# ─────────────────────────────────────────────────────────────────────────────
#  BOARD HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def make_board():
    return [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]

def can_place(board, row, col, size, horiz):
    for i in range(size):
        r = row + (0 if horiz else i)
        c = col + (i if horiz else 0)
        if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
            return False
        if board[r][c] != EMPTY:
            return False
    return True

def place_ship(board, row, col, size, horiz):
    for i in range(size):
        r = row + (0 if horiz else i)
        c = col + (i if horiz else 0)
        board[r][c] = SHIP

def all_sunk(board):
    return all(cell != SHIP for row in board for cell in row)

def ships_left(board):
    return sum(1 for row in board for cell in row if cell == SHIP)


# ─────────────────────────────────────────────────────────────────────────────
#  PARTICLES
# ─────────────────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, is_hit):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(1, 6) if is_hit else random.uniform(1, 3)
        self.x        = x + random.uniform(-4, 4)
        self.y        = y + random.uniform(-4, 4)
        self.vx       = math.cos(angle) * speed
        self.vy       = math.sin(angle) * speed - random.uniform(0, 3)
        self.life     = random.uniform(0.4, 1.0)
        self.max_life = self.life
        self.radius   = random.randint(2, 6) if is_hit else random.randint(2, 4)
        if is_hit:
            self.color = random.choice([RED_BRIGHT, HIT_ORANGE, GOLD_LIGHT, WHITE])
        else:
            self.color = random.choice([FOAM, OCEAN_LIGHT, WHITE])

    def update(self, dt):
        self.x    += self.vx
        self.y    += self.vy
        self.vy   += 0.15
        self.life -= dt
        return self.life > 0

    def draw(self, surf):
        a = max(0.0, self.life / self.max_life)
        r, g, b = self.color
        pygame.draw.circle(surf,
                           (int(r * a), int(g * a), int(b * a)),
                           (int(self.x), int(self.y)),
                           self.radius)


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def burst(self, x, y, is_hit, n=None):
        count = n if n else (40 if is_hit else 18)
        for _ in range(count):
            self.particles.append(Particle(x, y, is_hit))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surf):
        for p in self.particles:
            p.draw(surf)


# ─────────────────────────────────────────────────────────────────────────────
#  WAVE BACKGROUND
# ─────────────────────────────────────────────────────────────────────────────
class WaveBackground:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.t = 0.0

    def update(self, dt):
        self.t += dt * 0.4

    def draw(self, surf):
        surf.fill(NAVY)
        for y in range(0, self.h, 6):
            offset = int(math.sin(self.t + y * 0.04) * 4)
            alpha  = max(0, min(255, int(18 + 10 * math.sin(self.t * 1.3 + y * 0.06))))
            s = pygame.Surface((self.w, 3), pygame.SRCALPHA)
            s.fill((40, 90, 150, alpha))
            surf.blit(s, (offset, y))


# ─────────────────────────────────────────────────────────────────────────────
#  BUTTON
# ─────────────────────────────────────────────────────────────────────────────
class Button:
    def __init__(self, rect, text, font, color=GOLD, text_color=NAVY):
        self.rect       = pygame.Rect(rect)
        self.text       = text
        self.font       = font
        self.color      = color
        self.text_color = text_color
        self.hovered    = False

    def draw(self, surf):
        col = GOLD_LIGHT if self.hovered else self.color
        pygame.draw.rect(surf, col,   self.rect, border_radius=6)
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=6)
        lbl = self.font.render(self.text, True, self.text_color)
        surf.blit(lbl, lbl.get_rect(center=self.rect.center))

    def update(self, event):
        """Returns True if this button was clicked."""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False


# ─────────────────────────────────────────────────────────────────────────────
#  GRID HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def grid_origin(idx):
    return (MARGIN + idx * (BOARD_AREA_W + GAP), 130)

def cell_rect(idx, row, col):
    ox, oy = grid_origin(idx)
    return pygame.Rect(ox + LABEL_W + col * CELL,
                       oy + LABEL_W + row * CELL,
                       CELL, CELL)

def draw_grid(surf, board, reveal, grid_idx, font_sm,
              hover=None, preview=None):
    ox, oy = grid_origin(grid_idx)

    for c in range(BOARD_SIZE):
        x = ox + LABEL_W + c * CELL + CELL // 2
        lbl = font_sm.render(COLS[c], True, GREY_LIGHT)
        surf.blit(lbl, lbl.get_rect(center=(x, oy + LABEL_W // 2)))

    for r in range(BOARD_SIZE):
        y = oy + LABEL_W + r * CELL + CELL // 2
        lbl = font_sm.render(str(r + 1), True, GREY_LIGHT)
        surf.blit(lbl, lbl.get_rect(center=(ox + LABEL_W // 2, y)))

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            rect  = cell_rect(grid_idx, r, c)
            state = board[r][c]
            base  = OCEAN_DARK if (r + c) % 2 == 0 else OCEAN_MID
            pygame.draw.rect(surf, base, rect)

            if state == SHIP and reveal:
                pygame.draw.rect(surf, STEEL,      rect)
                pygame.draw.rect(surf, NAVY_LIGHT, rect, 1)
            elif state == HIT:
                pygame.draw.rect(surf, (60, 20, 10), rect)
                ctr = rect.center
                pygame.draw.circle(surf, RED,        ctr, CELL // 3)
                pygame.draw.circle(surf, HIT_ORANGE, ctr, CELL // 5)
                pygame.draw.circle(surf, GOLD_LIGHT, ctr, CELL // 8)
                m = 7
                pygame.draw.line(surf, WHITE,
                                 (rect.x + m, rect.y + m),
                                 (rect.right - m, rect.bottom - m), 2)
                pygame.draw.line(surf, WHITE,
                                 (rect.right - m, rect.y + m),
                                 (rect.x + m, rect.bottom - m), 2)
            elif state == MISS:
                pygame.draw.rect(surf, MISS_BLUE, rect)
                ctr = rect.center
                pygame.draw.circle(surf, FOAM,  ctr, CELL // 4, 2)
                pygame.draw.circle(surf, WHITE, ctr, 3)

            pygame.draw.rect(surf, NAVY_MID, rect, 1)

    if hover:
        hr, hc = hover
        r = cell_rect(grid_idx, hr, hc)
        s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
        s.fill((255, 255, 255, 45))
        surf.blit(s, r.topleft)
        pygame.draw.rect(surf, WHITE, r, 2)

    if preview:
        pr, pc, psz, ph, valid = preview
        col = (60, 200, 100, 130) if valid else (200, 60, 60, 130)
        for i in range(psz):
            r = pr + (0 if ph else i)
            c = pc + (i if ph else 0)
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                rect = cell_rect(grid_idx, r, c)
                s = pygame.Surface((CELL, CELL), pygame.SRCALPHA)
                s.fill(col)
                surf.blit(s, rect.topleft)

    border = pygame.Rect(ox + LABEL_W, oy + LABEL_W, GRID_PX, GRID_PX)
    pygame.draw.rect(surf, STEEL, border, 2)

def mouse_to_cell(pos, grid_idx):
    ox, oy = grid_origin(grid_idx)
    gx = ox + LABEL_W
    gy = oy + LABEL_W
    mx, my = pos
    if gx <= mx < gx + GRID_PX and gy <= my < gy + GRID_PX:
        return (my - gy) // CELL, (mx - gx) // CELL
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  GAME
# ─────────────────────────────────────────────────────────────────────────────
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_W, WIN_H))
        pygame.display.set_caption("Battleship")
        self.clock  = pygame.time.Clock()

        self.f_title = pygame.font.SysFont("Georgia",      42, bold=True)
        self.f_lg    = pygame.font.SysFont("Georgia",      28, bold=True)
        self.f_md    = pygame.font.SysFont("Trebuchet MS", 20, bold=True)
        self.f_sm    = pygame.font.SysFont("Trebuchet MS", 15)
        self.f_xs    = pygame.font.SysFont("Trebuchet MS", 12)

        self.wave = WaveBackground(WIN_W, WIN_H)
        self.ps   = ParticleSystem()

        # ── Every attribute the game ever needs is set here ──────────────────
        self.state         = S_MENU
        self.names         = ["Player 1", "Player 2"]
        self.boards        = [make_board(), make_board()]
        self.turn          = 0
        self.placer        = 0
        self.ship_idx      = 0
        self.horiz         = True
        self.hover         = None
        self.msg           = ""
        self.msg_timer     = 0.0
        self.handoff_msg   = ""
        self.after_handoff = S_BATTLE
        self.winner        = 0
        self.name_inputs   = ["Player 1", "Player 2"]
        self.active_input  = 0

        # Buttons — built once here, rebuilt as needed
        cx = WIN_W // 2
        self.menu_btns = [
            Button((cx - 120, 340, 240, 50), "New Game", self.f_md),
            Button((cx - 120, 408, 240, 50), "Quit",     self.f_md,
                   color=GREY, text_color=WHITE),
        ]
        self.setup_btn   = Button((cx - 100, 510, 200, 48), "Start >",    self.f_md)
        self.handoff_btn = Button((cx - 130, 440, 260, 52), "I'm ready >", self.f_md)
        self.victory_btns = [
            Button((cx - 130, 480, 260, 50), "Play Again", self.f_md),
            Button((cx - 130, 548, 260, 50), "Quit",       self.f_md,
                   color=GREY, text_color=WHITE),
        ]

    # ─── Reset for a new game ────────────────────────────────────────────────
    def _new_game(self):
        self.boards        = [make_board(), make_board()]
        self.turn          = 0
        self.placer        = 0
        self.ship_idx      = 0
        self.horiz         = True
        self.hover         = None
        self.msg           = ""
        self.msg_timer     = 0.0
        self.handoff_msg   = ""
        self.after_handoff = S_BATTLE
        self.winner        = 0
        self.name_inputs   = list(self.names)
        self.active_input  = 0
        self.state         = S_SETUP

    # ─── Main loop ───────────────────────────────────────────────────────────
    def run(self):
        prev = time.time()
        while True:
            now = time.time()
            dt  = min(now - prev, 0.05)
            prev = now

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self._handle(event)

            self.wave.update(dt)
            self.ps.update(dt)
            if self.msg_timer > 0:
                self.msg_timer -= dt

            self._draw()
            pygame.display.flip()
            self.clock.tick(60)

    # ─── Event routing ───────────────────────────────────────────────────────
    def _handle(self, event):
        if   self.state == S_MENU:    self._ev_menu(event)
        elif self.state == S_SETUP:   self._ev_setup(event)
        elif self.state == S_PLACE:   self._ev_place(event)
        elif self.state == S_HANDOFF: self._ev_handoff(event)
        elif self.state == S_BATTLE:  self._ev_battle(event)
        elif self.state == S_VICTORY: self._ev_victory(event)

    def _ev_menu(self, event):
        if self.menu_btns[0].update(event): self._new_game()
        if self.menu_btns[1].update(event): pygame.quit(); sys.exit()

    def _ev_setup(self, event):
        boxes = [
            pygame.Rect(WIN_W // 2 - 150, 275, 300, 44),
            pygame.Rect(WIN_W // 2 - 150, 375, 300, 44),
        ]
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, box in enumerate(boxes):
                if box.collidepoint(event.pos):
                    self.active_input = i

        if event.type == pygame.KEYDOWN:
            idx = self.active_input
            if event.key == pygame.K_BACKSPACE:
                self.name_inputs[idx] = self.name_inputs[idx][:-1]
            elif event.key == pygame.K_TAB:
                self.active_input = 1 - self.active_input
            elif event.key == pygame.K_RETURN:
                self._start_placement()
            elif len(self.name_inputs[idx]) < 16:
                self.name_inputs[idx] += event.unicode

        if self.setup_btn.update(event):
            self._start_placement()

    def _start_placement(self):
        self.names[0]  = self.name_inputs[0].strip() or "Player 1"
        self.names[1]  = self.name_inputs[1].strip() or "Player 2"
        self.boards    = [make_board(), make_board()]  # fresh boards
        self.placer    = 0
        self.ship_idx  = 0
        self.horiz     = True
        self.hover     = None
        self.state     = S_PLACE

    def _ev_place(self, event):
        p = self.placer
        if event.type == pygame.MOUSEMOTION:
            self.hover = mouse_to_cell(event.pos, 0)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_r, pygame.K_SPACE):
                self.horiz = not self.horiz
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                self.horiz = not self.horiz
            if event.button == 1:
                cell = mouse_to_cell(event.pos, 0)
                if cell:
                    r, c = cell
                    _, sz = SHIPS[self.ship_idx]
                    if can_place(self.boards[p], r, c, sz, self.horiz):
                        place_ship(self.boards[p], r, c, sz, self.horiz)
                        self._next_ship()

    def _next_ship(self):
        self.ship_idx += 1
        if self.ship_idx >= len(SHIPS):
            if self.placer == 0:
                self.placer        = 1
                self.ship_idx      = 0
                self.hover         = None
                self.handoff_msg   = f"Pass to {self.names[1]} to place their fleet!"
                self.after_handoff = S_PLACE
            else:
                self.hover         = None
                self.handoff_msg   = f"Pass to {self.names[0]}  --  BATTLE BEGINS!"
                self.after_handoff = S_BATTLE
            self.state = S_HANDOFF

    def _ev_handoff(self, event):
        if self.handoff_btn.update(event):
            self.state = self.after_handoff
            if self.after_handoff == S_PLACE:
                self.horiz = True
                self.hover = None

    def _ev_battle(self, event):
        attacker = self.turn
        defender = 1 - attacker

        if event.type == pygame.MOUSEMOTION:
            self.hover = mouse_to_cell(event.pos, 1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            cell = mouse_to_cell(event.pos, 1)
            if cell is None:
                return
            r, c = cell

            if self.boards[defender][r][c] in (HIT, MISS):
                self.msg       = "Already fired there!"
                self.msg_timer = 2.0
                return

            cx2, cy2 = cell_rect(1, r, c).center

            if self.boards[defender][r][c] == SHIP:
                self.boards[defender][r][c] = HIT
                self.ps.burst(cx2, cy2, is_hit=True)
                self.msg       = "DIRECT HIT!"
                self.msg_timer = 2.0
                if all_sunk(self.boards[defender]):
                    self.winner = attacker
                    self.state  = S_VICTORY
                    return
            else:
                self.boards[defender][r][c] = MISS
                self.ps.burst(cx2, cy2, is_hit=False)
                self.msg       = "Miss! Splash..."
                self.msg_timer = 2.0

            self.turn          = defender
            self.hover         = None
            self.handoff_msg   = f"Pass to {self.names[defender]}!"
            self.after_handoff = S_BATTLE
            self.state         = S_HANDOFF

    def _ev_victory(self, event):
        if self.victory_btns[0].update(event): self._new_game()
        if self.victory_btns[1].update(event): pygame.quit(); sys.exit()

    # ─── Draw routing ────────────────────────────────────────────────────────
    def _draw(self):
        self.wave.draw(self.screen)
        if   self.state == S_MENU:    self._dr_menu()
        elif self.state == S_SETUP:   self._dr_setup()
        elif self.state == S_PLACE:   self._dr_place()
        elif self.state == S_HANDOFF: self._dr_handoff()
        elif self.state == S_BATTLE:  self._dr_battle()
        elif self.state == S_VICTORY: self._dr_victory()
        self.ps.draw(self.screen)

    def _dr_menu(self):
        t  = time.time()
        cx = WIN_W // 2
        y_bob = int(math.sin(t * 1.2) * 5)
        title = self.f_title.render("BATTLESHIP", True, GOLD)
        self.screen.blit(title, title.get_rect(center=(cx, 180 + y_bob)))
        sub = self.f_md.render("2-Player Naval Combat", True, FOAM)
        self.screen.blit(sub, sub.get_rect(center=(cx, 242)))
        for i in range(40):
            xp = cx - 200 + i * 10
            yp = 287 + int(math.sin(t * 2 + i * 0.4) * 4)
            pygame.draw.circle(self.screen, OCEAN_LIGHT, (xp, yp), 2)
        for btn in self.menu_btns:
            btn.draw(self.screen)
        hint = self.f_xs.render("Requires: pip install pygame", True, GREY)
        self.screen.blit(hint, hint.get_rect(center=(cx, WIN_H - 24)))

    def _dr_setup(self):
        cx = WIN_W // 2
        title = self.f_lg.render("Enter Player Names", True, GOLD)
        self.screen.blit(title, title.get_rect(center=(cx, 200)))
        fields = [("Player 1 Name:", 240, 275), ("Player 2 Name:", 340, 375)]
        for i, (label, ly, iy) in enumerate(fields):
            lbl = self.f_sm.render(label, True, FOAM)
            self.screen.blit(lbl, (cx - 150, ly))
            rect   = pygame.Rect(cx - 150, iy, 300, 44)
            border = GOLD if self.active_input == i else STEEL
            pygame.draw.rect(self.screen, NAVY_MID, rect, border_radius=6)
            pygame.draw.rect(self.screen, border,   rect, 2, border_radius=6)
            txt = self.f_md.render(self.name_inputs[i], True, WHITE)
            self.screen.blit(txt, (rect.x + 10, rect.y + 11))
            if self.active_input == i and int(time.time() * 2) % 2 == 0:
                cw = txt.get_width()
                pygame.draw.line(self.screen, WHITE,
                                 (rect.x + 12 + cw, rect.y + 8),
                                 (rect.x + 12 + cw, rect.y + 36), 2)
        self.setup_btn.draw(self.screen)
        hint = self.f_xs.render("Tab to switch  |  Enter to confirm", True, GREY)
        self.screen.blit(hint, hint.get_rect(center=(cx, 580)))

    def _dr_place(self):
        p = self.placer
        idx = max(0, min(self.ship_idx, len(SHIPS) - 1))
        ship_name, sz = SHIPS[idx]
        preview = None
        if self.hover:
            hr, hc = self.hover
            valid   = can_place(self.boards[p], hr, hc, sz, self.horiz)
            preview = (hr, hc, sz, self.horiz, valid)
        draw_grid(self.screen, self.boards[p], True, 0, self.f_sm,
                  hover=self.hover, preview=preview)

        rx = MARGIN + BOARD_AREA_W + GAP
        ry = 130
        self.screen.blit(self.f_lg.render(f"{self.names[p]}'s Fleet Setup", True, GOLD),
                         (rx, ry))
        self.screen.blit(self.f_md.render(f"Placing: {ship_name}  (size {sz})",
                                          True, GREEN_LIGHT), (rx, ry + 52))
        orient = "Horizontal ->" if self.horiz else "Vertical  v"
        self.screen.blit(self.f_sm.render(f"Direction: {orient}", True, FOAM),
                         (rx, ry + 84))
        for i, h in enumerate(["Click to place ship",
                                "Right-click or R/Space to rotate",
                                "Green = valid,  Red = invalid"]):
            self.screen.blit(self.f_xs.render(h, True, GREY_LIGHT), (rx, ry + 120 + i * 20))
        self.screen.blit(self.f_sm.render("Your fleet:", True, FOAM), (rx, ry + 200))
        for j, (sn, ss) in enumerate(SHIPS):
            if j < self.ship_idx:     col, mark = GREY,        "OK"
            elif j == self.ship_idx:  col, mark = GREEN_LIGHT, ">>"
            else:                     col, mark = WHITE,        "  "
            self.screen.blit(self.f_xs.render(f"  {mark}  {sn} ({ss})", True, col),
                             (rx, ry + 224 + j * 22))

    def _dr_handoff(self):
        cx = WIN_W // 2
        cy = WIN_H // 2 - 40
        overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 185))
        self.screen.blit(overlay, (0, 0))
        heading = self.f_lg.render("PASS THE SCREEN", True, GOLD)
        self.screen.blit(heading, heading.get_rect(center=(cx, cy - 30)))
        sub = self.f_md.render(self.handoff_msg, True, FOAM)
        self.screen.blit(sub, sub.get_rect(center=(cx, cy + 24)))
        self.handoff_btn.draw(self.screen)

    def _dr_battle(self):
        attacker = self.turn
        defender = 1 - attacker
        cx       = WIN_W // 2

        pygame.draw.rect(self.screen, NAVY_MID, (0, 0, WIN_W, 126))
        pygame.draw.line(self.screen, STEEL, (0, 126), (WIN_W, 126), 2)

        tl = self.f_lg.render(f"{self.names[attacker]}'s Turn", True, GOLD)
        self.screen.blit(tl, tl.get_rect(center=(cx, 38)))

        ol = self.f_sm.render(f"Your Fleet  ({self.names[attacker]})", True, FOAM)
        self.screen.blit(ol, ol.get_rect(center=(MARGIN + BOARD_AREA_W // 2, 80)))

        el = self.f_sm.render(f"Enemy Waters  ({self.names[defender]})", True, RED)
        self.screen.blit(el, el.get_rect(center=(WIN_W - MARGIN - BOARD_AREA_W // 2, 80)))

        st = self.f_xs.render(
            f"Your ships: {ships_left(self.boards[attacker])} cells  |  "
            f"Enemy ships: {ships_left(self.boards[defender])} cells",
            True, GREY_LIGHT)
        self.screen.blit(st, st.get_rect(center=(cx, 106)))

        draw_grid(self.screen, self.boards[attacker], True,  0, self.f_sm)
        draw_grid(self.screen, self.boards[defender], False, 1, self.f_sm,
                  hover=self.hover)

        if self.msg and self.msg_timer > 0:
            alpha = min(255, int(255 * self.msg_timer))
            ms = self.f_md.render(self.msg, True, WHITE)
            ms.set_alpha(alpha)
            self.screen.blit(ms, ms.get_rect(center=(cx, WIN_H - 36)))

    def _dr_victory(self):
        cx = WIN_W // 2
        cy = WIN_H // 2 - 60
        overlay = pygame.Surface((WIN_W, WIN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))

        t     = time.time()
        y_bob = int(math.sin(t * 2) * 6)
        star  = self.f_title.render("* VICTORY *", True, GOLD_LIGHT)
        self.screen.blit(star, star.get_rect(center=(cx, cy - 80 + y_bob)))
        wl = self.f_title.render(f"{self.names[self.winner]} WINS!", True, GOLD)
        self.screen.blit(wl, wl.get_rect(center=(cx, cy)))

        loser   = 1 - self.winner
        sl = self.f_md.render(
            f"All of {self.names[loser]}'s ships have been sunk!", True, FOAM)
        self.screen.blit(sl, sl.get_rect(center=(cx, cy + 52)))

        total_hits = sum(1 for row in self.boards[loser] for cell in row if cell == HIT)
        hl = self.f_sm.render(f"Total hits scored: {total_hits}", True, GREY_LIGHT)
        self.screen.blit(hl, hl.get_rect(center=(cx, cy + 90)))

        if random.random() < 0.35:
            self.ps.burst(random.randint(80, WIN_W - 80),
                          random.randint(40, 180), is_hit=True, n=5)

        for btn in self.victory_btns:
            btn.draw(self.screen)


# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    Game().run()

