import pygame
import random
from array import array

# Initialize Pygame and mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
FPS = 60
PADDLE_SPEED = 20  # Increased paddle speed for more responsive gameplay
BALL_X_SPEED = 7   # Adjusted for balanced gameplay
BALL_Y_SPEED = 7   # Adjusted for balanced gameplay

# Function to generate beep sounds
def generate_beep_sound(frequency, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Sound effects
hit_sound = generate_beep_sound(523.25)  # High beep for paddle hit
score_sound = generate_beep_sound(440, 0.2)  # Lower, longer beep for score

# Define the Paddle class
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, ai=False):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ai = ai
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_up:
            self.move_up()
        if self.moving_down:
            self.move_down()

    def move_up(self):
        if self.rect.y > 0:
            self.rect.y -= PADDLE_SPEED

    def move_down(self):
        if self.rect.y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            self.rect.y += PADDLE_SPEED

    def ai_move(self, ball):
        if self.ai:
            if self.rect.centery < ball.rect.centery:
                self.move_down()
            else:
                self.move_up()

# Define the Ball class
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reset()

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y *= -1
            hit_sound.play()
        # Check for scoring
        if self.rect.x < 0:
            score_sound.play()
            self.reset()
            score[1] += 1  # Score for AI
        elif self.rect.x > SCREEN_WIDTH:
            score_sound.play()
            self.reset()
            score[0] += 1  # Score for player

    def reset(self):
        self.image = pygame.Surface([BALL_SIZE, BALL_SIZE])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed_x = BALL_X_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_Y_SPEED * random.choice([-1, 1])

# Setup display and font
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong with Sound")
font = pygame.font.Font(None, 36)

# Score initialization
score = [0, 0]  # [player_score, ai_score]

# Create sprite groups
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

paddles = pygame.sprite.Group()
ball = Ball()
player_paddle = Paddle(30, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
ai_paddle = Paddle(SCREEN_WIDTH - 40 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, ai=True)
paddles.add(player_paddle, ai_paddle)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_paddle.moving_up = True
            elif event.key == pygame.K_DOWN:
                player_paddle.moving_down = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_paddle.moving_up = False
            elif event.key == pygame.K_DOWN:
                player_paddle.moving_down = False

    # AI movement
    ai_paddle.ai_move(ball)

    # Update game objects
    ball.update()
    paddles.update()

    # Drawing
    screen.fill(BLACK)
    paddles.draw(screen)
    screen.blit(ball.image, ball.rect)
    player_score_text = font.render(f"Player: {score[0]}", True, WHITE)
    ai_score_text = font.render(f"AI: {score[1]}", True, WHITE)
    screen.blit(player_score_text, (50, 20))
    screen.blit(ai_score_text, (SCREEN_WIDTH - 150, 20))

    # Update the display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
