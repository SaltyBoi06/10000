import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("10,000 Dice Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and resize dice images
dice_images = [pygame.transform.scale(pygame.image.load(f"dice{i}.png"), (100, 100)) for i in range(1, 7)]

# Font
font = pygame.font.Font(None, 36)

# Roll dice function
def roll_dice(num_dice=6):
    return [random.randint(1, 6) for _ in range(num_dice)]

def score_roll(dice):
    from collections import Counter
    counts = Counter(dice)
    score = 0

    # Scoring rules
    if len(set(dice)) == 6:  # Straight (1-6)
        return 1500
    if list(counts.values()).count(2) == 3:  # Three pairs
        return 1500

    for num, count in counts.items():
        if count >= 3:
            if num == 1:
                score += 1000 * (count - 2)
            else:
                score += num * 100 * (count - 2)

    # Single die scoring (1 and 5 if not part of a triplet)
    if counts[1] < 3:
        score += counts[1] * 100
    if counts[5] < 3:
        score += counts[5] * 50

    return score

def valid_selection(roll, keep_values):
    from collections import Counter
    roll_counts = Counter(roll)
    keep_counts = Counter(keep_values)
    for value, count in keep_counts.items():
        if roll_counts[value] < count:
            return False
    return True

def animate_dice(roll):
    for _ in range(10):
        temp_roll = [random.randint(1, 6) for _ in roll]
        draw_game(temp_roll)
        pygame.time.delay(100)
        pygame.event.pump()

def draw_game(dice, message="", scores=None):
    screen.fill(WHITE)

    # Display dice
    for i, die in enumerate(dice):
        screen.blit(dice_images[die - 1], (100 + i * 100, 200))

    # Display message
    msg_surface = font.render(message, True, BLACK)
    screen.blit(msg_surface, (50, 50))

    # Display scores
    if scores:
        for i, score in enumerate(scores):
            score_text = font.render(f"Player {i + 1}: {score}", True, BLACK)
            screen.blit(score_text, (50, 400 + i * 30))

    pygame.display.flip()

def play_turn(player_total_score):
    dice_remaining = 6
    turn_score = 0

    while True:
        roll = roll_dice(dice_remaining)
        animate_dice(roll)

        roll_score = score_roll(roll)
        if roll_score == 0:
            draw_game(roll, "Farkle! No points scored.")
            pygame.time.delay(2000)
            return 0

        draw_game(roll, f"Current turn score: {turn_score + roll_score}")

        keep_values = []
        selecting = True
        while selecting:
            draw_game(roll, "Press number keys to keep dice, Enter to roll")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        selecting = False
                    elif event.key in range(pygame.K_1, pygame.K_7):
                        die_index = event.key - pygame.K_1
                        if die_index < len(roll):
                            keep_values.append(roll[die_index])

        if not valid_selection(roll, keep_values):
            draw_game(roll, "Invalid selection. Try again.")
            pygame.time.delay(2000)
            continue

        turn_score += score_roll(keep_values)
        dice_remaining -= len(keep_values)

        if dice_remaining == 0:
            dice_remaining = 6

        draw_game(roll, "Press Y to bank points, N to continue")
        deciding = True
        while deciding:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        return turn_score
                    if event.key == pygame.K_n:
                        deciding = False

def play_game():
    num_players = int(input("Enter number of players: "))
    player_scores = [0] * num_players
    current_player = 0

    running = True
    while running:
        draw_game([], f"Player {current_player + 1}'s Turn", player_scores)
        pygame.time.delay(2000)

        turn_score = play_turn(player_scores[current_player])
        player_scores[current_player] += turn_score

        if player_scores[current_player] >= 10000:
            draw_game([], f"Player {current_player + 1} wins!", player_scores)
            pygame.time.delay(5000)
            running = False

        current_player = (current_player + 1) % num_players

    pygame.quit()

play_game()
