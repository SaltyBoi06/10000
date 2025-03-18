import random

def roll_dice(num_dice=6):
    """Rolls a given number of dice and returns the result as a list."""
    return [random.randint(1, 6) for _ in range(num_dice)]

def score_roll(dice):
    """Calculates the score based on the dice roll."""
    from collections import Counter
    counts = Counter(dice)
    score = 0

    # Scoring rules
    if len(set(dice)) == 6:  # Straight (1-6)
        return 1500
    if list(counts.values()).count(2) == 3:  # Three pairs
        return 600

    for num, count in counts.items():
        if count >= 3:
            if num == 1:
                score += 1000 * (count - 2)  # 1000 for three 1s, 2000 for four 1s, etc.
            else:
                score += num * 100 * (count - 2)  # Three 5s = 500, Three 2s = 200, etc.

    # Single die scoring (only counts if not part of a triplet or more)
    if counts[1] < 3:
        score += counts[1] * 100
    if counts[5] < 3:
        score += counts[5] * 50

    return score

def valid_selection(roll, keep_values):
    """Checks if the selected dice are valid based on the roll."""
    from collections import Counter
    roll_counts = Counter(roll)
    keep_counts = Counter(keep_values)
    for value, count in keep_counts.items():
        if roll_counts[value] < count:
            return False
    return True

def play_turn(player_total_score):
    """Handles a single turn for the player."""
    dice_remaining = 6
    turn_score = 0

    while True:
        print(f"Rolling {dice_remaining} dice...")
        roll = roll_dice(dice_remaining)
        print(f"You rolled: {roll}")

        roll_score = score_roll(roll)
        if roll_score == 0:
            print("Farkle! No points scored this round.")
            return 0

        print(f"Current turn score: {turn_score + roll_score}")

        # Allow user to select which dice to keep
        keep_input = input("Enter the dice values you want to keep, separated by spaces: ")
        keep_values = list(map(int, keep_input.split()))

        # Verify selected dice are valid
        if not valid_selection(roll, keep_values):
            print("Invalid selection. Please choose only from rolled dice.")
            return 0

        # Update score only with the selected dice
        turn_score += score_roll(keep_values)

        dice_remaining -= len(keep_values)

        # Reset dice if all dice are used
        if dice_remaining == 0:
            print("You used all dice! Rolling all 6 again.")
            dice_remaining = 6

        if turn_score >= 1000 or player_total_score + turn_score >= 1000:
            keep_playing = input("Bank points? (y/n) ").lower()
            if keep_playing == 'y':
                return turn_score
        else:
            print("You need at least 1000 total score or turn score to bank points.")

def play_game():
    """Multiplayer game loop."""
    num_players = int(input("Enter number of players: "))
    player_scores = [0] * num_players
    current_player = 0

    while max(player_scores) < 10000:
        print(f"\n--- Player {current_player + 1}'s Turn ---")
        turn_score = play_turn(player_scores[current_player])
        player_scores[current_player] += turn_score

        print(f"Player {current_player + 1}'s total score: {player_scores[current_player]}")

        if player_scores[current_player] >= 10000:
            print(f"Congratulations! Player {current_player + 1} reached 10,000 points and won the game.")
            break

        # Move to the next player
        current_player = (current_player + 1) % num_players

play_game()
