import pygame
import time

pygame.init()
pygame.mixer.init()

# Load sounds
kick = pygame.mixer.Sound("kick.wav")
snare = pygame.mixer.Sound("snare.wav")
hihat = pygame.mixer.Sound("hihat.wav")
clap = pygame.mixer.Sound("clap.wav")

sounds = [kick, snare, hihat, clap]

# Screen setup
WIDTH, HEIGHT = 800, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple FL Sequencer")

# Grid setup
ROWS = 4
COLS = 16
CELL_SIZE = 40

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Timing
BPM = 120
step_delay = 60 / BPM / 4  # 16th notes

current_step = 0
running = True
clock = pygame.time.Clock()

last_step_time = time.time()

def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            color = (0, 200, 0) if grid[row][col] else (50, 50, 50)
            
            if col == current_step:
                color = (200, 0, 0)

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (20, 20, 20), rect, 2)

while running:
    screen.fill((30, 30, 30))

    # Handle input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // CELL_SIZE
            row = y // CELL_SIZE

            if row < ROWS and col < COLS:
                grid[row][col] ^= 1  # toggle

    # Timing for sequencer
    current_time = time.time()
    if current_time - last_step_time > step_delay:
        for row in range(ROWS):
            if grid[row][current_step]:
                sounds[row].play()

        current_step = (current_step + 1) % COLS
        last_step_time = current_time

    draw_grid()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()