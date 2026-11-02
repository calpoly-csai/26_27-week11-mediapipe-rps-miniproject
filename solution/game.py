"""Game rules -- SOLUTION version."""
import random

MOVES = ["rock", "paper", "scissors"]
WINS_NEEDED = 3

BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}


def computer_move():
    """Return 'rock', 'paper', or 'scissors' at random."""
    return random.choice(MOVES)


def decide_winner(player, computer):
    """Return 'player', 'computer', or 'tie'."""
    if player == computer:
        return "tie"
    if BEATS[player] == computer:
        return "player"
    return "computer"


class Scoreboard:
    def __init__(self):
        self.player = 0
        self.computer = 0

    def record(self, winner):
        """Add a point for 'player' or 'computer'. Ties score nothing."""
        if winner == "player":
            self.player += 1
        elif winner == "computer":
            self.computer += 1

    def is_game_over(self):
        return self.player >= WINS_NEEDED or self.computer >= WINS_NEEDED

    def champion(self):
        """'player', 'computer', or None if the game isn't over."""
        if self.player >= WINS_NEEDED:
            return "player"
        if self.computer >= WINS_NEEDED:
            return "computer"
        return None
