"""Game rules -- YOUR CODE (steps 6 and 7).

main.py shows '???' for any function below that still raises NotImplementedError.
Delete the `raise` line in each function once you've written it.
"""
import random  # noqa: F401  (you'll need this)

MOVES = ["rock", "paper", "scissors"]
WINS_NEEDED = 3  # first to this many wins takes the game


def computer_move():
    """Return 'rock', 'paper', or 'scissors' at random.

    TODO (step 6): hint -- random.choice(MOVES)
    """
    raise NotImplementedError


def decide_winner(player, computer):
    """Return 'player', 'computer', or 'tie'.

    Rock beats scissors, scissors beats paper, paper beats rock.

    TODO (step 6): compare the two moves with if statements.
    """
    raise NotImplementedError


class Scoreboard:
    """Tracks the score across rounds."""

    def __init__(self):
        self.player = 0
        self.computer = 0

    def record(self, winner):
        """Add a point for `winner` ('player' or 'computer'). Ties score nothing.

        TODO (step 7)
        """
        raise NotImplementedError

    def is_game_over(self):
        """True once either side has WINS_NEEDED points.

        TODO (step 7)
        """
        raise NotImplementedError

    def champion(self):
        """'player' or 'computer' once the game is over, otherwise None.

        TODO (step 7)
        """
        raise NotImplementedError
