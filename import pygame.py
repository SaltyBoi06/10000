import pygame
import random
from collections import Counter

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("10,000 Dice Game")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

dice_images = [pygame.transform.scale(pygame.image.load(f"dice{i}.png"), (80, 80)) for i in range(1, 7)]
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def roll_dice(num_dice=6):
    return [random.randint(1, 6) for _ in range(num_dice)]

def score_roll(dice):
    counts = Counter(dice)
    score = 0

    if len(set(dice)) == 6:
        return 1500
    if list(counts.values()).count(2) == 3:
        return 1500

    for num, count in counts.items():
        if count >= 3:
            if num == 1:
                score += 1000 * (count - 2)
            else:
                score += num * 100 * (count - 2)

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

    for i, die in enumerate(dice):
        x = 80 + i * 80
        y = 250
        screen.blit(dice_images[die - 1], (x, y))
        label = small_font.render(str(i + 1), True, BLACK)
        screen.blit(label, (x + 20, y - 25))

    msg_surface = font.render(message, True, BLACK)
    screen.blit(msg_surface, (50, 180))

    if scores:
        for i, score in enumerate(scores):
            score_text = font.render(f"Player {i + 1}: {score}", True, BLACK)
            screen.blit(score_text, (50, 450 + i * 40))

    pygame.display.flip()

def bot_choose_dice(roll):
    from collections import Counter
    counts = Counter(roll)
    keep = []

    if len(set(roll)) == 6 or list(counts.values()).count(2) == 3:
        return roll[:]

    used_counts = Counter()

    for num in range(1, 7):
        if counts[num] >= 3:
            keep.extend([num] * counts[num])
            used_counts[num] = counts[num]

    if counts[1] < 3:
        remaining_ones = counts[1] - used_counts[1]
        keep.extend([1] * remaining_ones)
    if counts[5] < 3:
        remaining_fives = counts[5] - used_counts[5]
        keep.extend([5] * remaining_fives)

    return keep

def play_turn(player_total_score, is_bot=False):
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

        if is_bot:
            keep_values = bot_choose_dice(roll)
        else:
            draw_game(roll, f"Current turn score: {turn_score + roll_score}")
            keep_values = []
            selecting = True
            while selecting:
                draw_game(roll, "Press 1–6 to select dice, Enter to roll")
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            selecting = False
                        elif pygame.K_1 <= event.key <= pygame.K_6:
                            index = event.key - pygame.K_1
                            if index < len(roll):
                                keep_values.append(roll[index])

        if not valid_selection(roll, keep_values):
            draw_game(roll, "Invalid selection. Try again.")
            pygame.time.delay(2000)
            if is_bot:
                return 0
            continue

        turn_score += score_roll(keep_values)
        dice_remaining -= len(keep_values)

        if dice_remaining == 0:
            dice_remaining = 6

        if player_total_score + turn_score >= 1000:
            if is_bot:
                if turn_score >= 1000 or random.random() > 0.5:
                    return turn_score
            else:
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
        elif not is_bot:
            draw_game(roll, "Score too low to bank. Press any key to roll again.")
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        waiting = False


def play_game():
    num_players = int(input("Enter number of players (including bot): "))
    bot_index = num_players - 1
    player_scores = [0] * num_players
    current_player = 0
    final_round = False
    final_turns_remaining = [False] * num_players

    running = True
    while running:
        is_bot = current_player == bot_index
        draw_game([], f"{'Bot' if is_bot else f'Player {current_player + 1}'}'s Turn", player_scores)
        pygame.time.delay(2000)

        turn_score = play_turn(player_scores[current_player], is_bot)
        player_scores[current_player] += turn_score

        if player_scores[current_player] >= 10000 and not final_round:
            draw_game([], f"{'Bot' if is_bot else f'Player {current_player + 1}'} triggered final round!", player_scores)
            pygame.time.delay(3000)
            final_round = True
            for i in range(num_players):
                if i != current_player:
                    final_turns_remaining[i] = True

        elif final_round and final_turns_remaining[current_player]:
            final_turns_remaining[current_player] = False

        elif final_round and not any(final_turns_remaining):
            highest_score = max(player_scores)
            winner = player_scores.index(highest_score)
            winner_text = "Bot" if winner == bot_index else f"Player {winner + 1}"
            draw_game([], f"{winner_text} wins with {highest_score} points!", player_scores)
            pygame.time.delay(5000)
            running = False

        current_player = (current_player + 1) % num_players

    pygame.quit()

play_game()
