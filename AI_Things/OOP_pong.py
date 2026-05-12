import pygame
import random

# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 1500, 800
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60


# Set up Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("OOP Pong")
clock = pygame.time.Clock()

# --- CLASSES ---
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.velocity = 10

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self, up=True):
        if up and self.rect.top > 0:
            self.rect.y -= self.velocity
        elif not up and self.rect.bottom < HEIGHT:
            self.rect.y += self.velocity

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)
        self.reset()

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.x_vel = random.choice([-5, 5])
        self.y_vel = random.choice([-3, 3])

    def bounce_y(self):
        self.y_vel *= -1.1

    def bounce_x(self):
        self.x_vel *= -1.1

class Scoreboard:
    def __init__(self):
        self.score1 = 0
        self.score2 = 0
        self.font = pygame.font.Font(None, 74)

    def draw(self, screen):
        s1 = self.font.render(str(self.score1), True, WHITE)
        s2 = self.font.render(str(self.score2), True, WHITE)
        screen.blit(s1, (WIDTH//4, 20))
        screen.blit(s2, (3*WIDTH//4, 20))

# --- MAIN GAME LOOP ---
def main():
    player1 = Paddle(10, HEIGHT//2 - PADDLE_HEIGHT//2)
    player2 = Paddle(WIDTH - 20, HEIGHT//2 - PADDLE_HEIGHT//2)
    ball = Ball()
    scoreboard = Scoreboard()

    running = True
    while running:
        screen.fill(BLACK)
        
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Input Handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: player1.move(up=True)
        if keys[pygame.K_s]: player1.move(up=False)
        if keys[pygame.K_UP]: player2.move(up=True)
        if keys[pygame.K_DOWN]: player2.move(up=False)

        # Game Logic
        ball.move()
        
        # Wall Collision
        if ball.rect.top <= 0 or ball.rect.bottom >= HEIGHT:
            ball.bounce_y()
            
        # Paddle Collision
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            ball.bounce_x()

        # Scoring
        if ball.rect.left <= 0:
            scoreboard.score2 += 1
            ball.reset()
        elif ball.rect.right >= WIDTH:
            scoreboard.score1 += 1
            ball.reset()

        # Draw Everything
        player1.draw(screen)
        player2.draw(screen)
        ball.draw(screen)
        scoreboard.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()