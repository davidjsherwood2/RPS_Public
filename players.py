import random


def validate_move():
    """Global function runs an input prompt and ensures it is in [rock,paper,scissors]"""
    while True:
        try:
            move = input('ENTER MOVE [ Rock | Paper | Scissors ]: ').lower()
            assert move in ['rock', 'paper', 'scissors']
            break
        except AssertionError:
            print('Invalid entry - please enter Rock, Paper, or Scissors')
    return move


class Player:
    """Class to hold all instances of players entered in RPS bracket. Takes player name as input."""

    def __init__(self, name):
        self.name = name
        self.score, self.t_nums, self.round_nums = 0, 0, 0
        self.t_list = []

    def turn(self, move=''):
        """Calls validate_move() if player isnt a Bot, otherwise accepts explicit move selection."""
        self.t_nums += 1
        if not move:
            move = validate_move()
        self.t_list.append(move)
        self.t_nums += 1
        return move

    def add_point(self):
        """function to add one point to score"""
        self.score += 1
        return self.score

    def point_reset(self):
        """resets point vals on player"""
        self.score, self.t_nums = 0, 0
        self.t_list = []

    def __str__(self):
        """Private function for admin access to player attributes"""
        return f"""
            Player: {self.name}
            Score: {self.score}
            Num Turns: {self.t_nums}
            Moves: {self.t_list}
            """


class Bot(Player):
    """Sub class of player to serve as a computer bot against 1 or more opponents in match"""

    def __init__(self, name):
        super().__init__(name)

    def turn(self, move=''):
        """function to represent back end turn"""
        self.t_nums += 1
        if not move:
            move = random.choice(['rock', 'paper', 'scissors'])
        self.t_list.append(move)
        return move

    def add_point(self):
        super().add_point()

    def point_reset(self):
        super().point_reset()

    def __str__(self):
        super().add_point()
