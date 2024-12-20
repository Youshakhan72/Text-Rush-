import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Type Racing Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 64)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load assets
try:
    # Load and scale background image to fit the screen
    bg_image = pygame.image.load("assets/background.jpg")
    bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

    # Sounds
    pygame.mixer.music.load("assets/bg_music.mp3")  # Background music
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    match_sound = pygame.mixer.Sound("assets/match.mp3")  # Correct word
    match_sound.set_volume(0.2)

    game_over_sound = pygame.mixer.Sound("assets/game_over.mp3")  # Game over
    game_over_sound.set_volume(0.7)
except Exception as e:
    print(f"Error loading assets: {e}")
    pygame.quit()
    exit()

# Load word list
word_list = [
    "python", "Lords", "speed", "type", "racing", "programming",
    "Technology", "challenge", "focus", "IT", "code", "developer",
    "script", "debug", "function", "variable", "loop", "array",
]

# Game variables
score = 0
lives = 15
level = 1
speed = 1
input_text = ""
words = []
game_over = False

# Word class
class Word:
    def __init__(self, text, x, y, speed):
        self.text = text
        self.x = x
        self.y = y
        self.speed = speed

    def draw(self):
        text_surface = FONT.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.x, self.y))

    def move(self):
        self.x -= self.speed

# Generate a new word
def generate_word():
    text = random.choice(word_list)
    x = random.randint(WIDTH, WIDTH + 200)
    y = random.randint(50, HEIGHT - 50)
    return Word(text, x, y, speed)

# Reset game
def reset_game():
    global score, lives, level, speed, input_text, words, game_over
    score = 0
    lives = 15
    level = 1
    speed = 1
    input_text = ""
    words = [generate_word() for _ in range(3)]
    game_over = False
    pygame.mixer.music.play(-1)  # Restart background music

# Main game loop
reset_game()
running = True

while running:
    screen.blit(bg_image, (0, 0))  # Draw scaled background
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_RETURN:  # Press Enter to submit
                matched = False
                for word in words:
                    if input_text == word.text:
                        words.remove(word)
                        score += 10
                        speed += 0.2
                        match_sound.play()  # Play match sound
                        matched = True
                        break
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:  # Backspace to delete
                input_text = input_text[:-1]
            else:
                input_text += event.unicode  # Add character to input

    if not game_over:
        # Draw words and move them
        for word in words:
            word.move()
            word.draw()
            if word.x < 0:  # If a word goes off-screen
                words.remove(word)
                lives -= 1
                if lives <= 0:
                    game_over = True
                    game_over_sound.play()  # Play game over sound
                    pygame.mixer.music.stop()  # Stop background music

        # Add new words
        if len(words) < 5:
            words.append(generate_word())

        # Display input text
        input_surface = FONT.render(f"Input: {input_text}", True, GREEN)
        screen.blit(input_surface, (10, HEIGHT - 40))

        # Display score and lives
        score_surface = FONT.render(f"Score: {score}", True, WHITE)
        lives_surface = FONT.render(f"Lives: {lives}", True, RED)
        level_surface = FONT.render(f"Level: {level}", True, BLUE)
        screen.blit(score_surface, (10, 10))
        screen.blit(lives_surface, (WIDTH - 150, 10))
        screen.blit(level_surface, (WIDTH // 2 - 50, 10))

        # Level up
        if score > 0 and score % 50 == 0:
            level += 1
            words.append(generate_word())
            score += 1  # Prevent repeated level-ups for the same score

    else:
        # Game Over screen
        game_over_surface = BIG_FONT.render("GAME OVER", True, RED)
        final_score_surface = FONT.render(f"Your Score: {score}", True, WHITE)
        restart_surface = FONT.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(game_over_surface, (WIDTH // 2 - 150, HEIGHT // 2 - 80))
        screen.blit(final_score_surface, (WIDTH // 2 - 100, HEIGHT // 2))
        screen.blit(restart_surface, (WIDTH // 2 - 200, HEIGHT // 2 + 60))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # Restart game
            reset_game()
        elif keys[pygame.K_q]:  # Quit game
            running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
