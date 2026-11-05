"""Game rules -- YOUR CODE (steps 6 and 7).

No AI here, just plain Python. How main.py uses this file, once per round at "Shoot!":
  1. computer_move()                  -> e.g. "paper"
  2. decide_winner("rock", "paper")   -> "computer"
  3. board.record("computer")         -> adds a point
  4. board.is_game_over()             -> True once someone has WINS_NEEDED points
  5. board.champion()                 -> "player" or "computer", shown on screen

main.py shows '???' for any function below that still raises NotImplementedError.
Delete the `raise` line in each function once you've written it.
"""
import random  # noqa: F401  (you'll need this)

MOVES = ["rock", "paper", "scissors"]
WINS_NEEDED = 3  # first to this many wins takes the game


def computer_move():
    """Return 'rock', 'paper', or 'scissors' at random.

    TODO (step 6): hint -- random.choice(MOVES) picks one item from a list at random,
    each equally likely.
    """
    raise NotImplementedError


def decide_winner(player, computer):
    """Return 'player', 'computer', or 'tie'.

    Rock beats scissors, scissors beats paper, paper beats rock.
    Both arguments are always one of the strings in MOVES.

    TODO (step 6): compare the two moves with if statements. Handle the tie first.
    Shorter alternative: a dict saying what each move beats, e.g.
    {"rock": "scissors", ...}; then the player wins if that dict maps their move to
    the computer's.
    """
    raise NotImplementedError


class Scoreboard:
    """Tracks the score across rounds.

    main.py makes a new Scoreboard at the start of each game (and when you press R)
    and reads self.player / self.computer to draw the score at the top of the screen.
    """

    def __init__(self):
        self.player = 0      # rounds the human has won
        self.computer = 0    # rounds the computer has won

    def record(self, winner):
        """Add a point for `winner` ('player' or 'computer'). Ties score nothing.

        TODO (step 7): add 1 to self.player or self.computer. Nothing to return.
        """
        raise NotImplementedError

    def is_game_over(self):
        """True once either side has WINS_NEEDED points.

        TODO (step 7): compare both counters to WINS_NEEDED and return True/False.
        """
        raise NotImplementedError

    def champion(self):
        """'player' or 'computer' once the game is over, otherwise None.

        TODO (step 7): whoever reached WINS_NEEDED; None if nobody has yet.
        """
        raise NotImplementedError
