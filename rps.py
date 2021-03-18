import random
import players as p


class RPSEngine:
    """Runs a best-out-of-three bracket-style tournament of rock, paper, scissors
     with both human and computer bot players/opponents using a command line prompt"""

    def __init__(self):
        self.players = {}
        self.num_players = 0
        self.match_opponents = {}
        self.num_headtohead = 0

    # Section 1 - Player-level functions

    def add_players(self):
        """initalizes Player objects with name input step and adds to player list"""
        name = input('Enter player name here (ENTER when finished): ')
        while name != '':
            self.num_players += 1
            player = p.Player(name)
            self.players[self.num_players] = player
            name = input('Enter player name here (ENTER when finished): ')
        print(f'{len(self.players)} players added!\n')

    def add_bots(self, num_bots):
        """prompts for number of bot opponents to be added and adds to player list"""
        for num in range(1, num_bots + 1):
            bot = p.Bot(f'Intelli-Bot {num}')
            self.players[num] = bot
        print(f"{num_bots} Bot opponents added to match! \n\n")

    # Section 2 - Functions for setting up new game and controlling game play

    def main_game_engine(self):
        """Calls main game functions that set players, start a new game bracket, and begin gameplay"""
        self.player_set()
        self.new_game()
        self.game_play()

    def player_set(self):
        """sets players and/or bot opponents prior to game start"""
        num_bots = input("Please enter number of bot opponents: ")
        num_bots = int(num_bots)
        self.add_bots(num_bots)
        self.num_players += num_bots
        self.add_players()

    def new_game(self):
        """keeps current player set but wipes score information"""
        for player in self.players:
            self.players[player].point_reset()
        self.match_opponents = dict(self.players)

    def game_play(self):
        """Selects two random players and calls single match until only one person
            remains in the match opponent list"""
        while True:
            # Two opponents picked at random
            choice1 = random.choice(list(self.match_opponents.keys()))
            p1 = self.match_opponents.pop(choice1)
            choice2 = random.choice(list(self.match_opponents.keys()))
            p2 = self.match_opponents.pop(choice2)
            print(f'NEW ROUND - NEXT UP IS {p1.name} and {p2.name}')
            # 1v1 best out of 3 match started with single_match
            winner = self.single_match(p1, p2)
            if len(self.match_opponents.keys()) <= 1:
                break
        print(f"\n\n::::::GAME OVER::::::\n::{winner.name} IS THE CHAMPION!::\n\n")
        print(f" Total of {self.num_headtohead} rounds")

    def single_match(self, p1, p2):
        """Calls turn() on p1/p2 then calls player_rps_eval() to start scoring logic"""
        while True:
            if type(p1) is p.Player:
                print(f"\nIt's {p1.name}'s turn")
            elif type(p1) is p.Bot:
                print(f"\n{p1.name} has made its move")
            p1.turn()
            if type(p1) is p.Player:
                print(f"\nIt's {p2.name}'s turn")
            elif type(p2) is p.Bot:
                print(f"\n{p2.name} has made its move\n")
            p2.turn()
            self.player_rps_eval(p1, p2)
            high_score = self.get_high_score(p1, p2)
            self.num_headtohead += 1
            # BEST OUT OF THREE LOGIC
            # if one player has at least two pts and is leading by at least 1 point, winner
            if (high_score >= 2) and (abs(p1.score - p2.score) >= 1):
                winner = self.declare_winner(p1, p2)
                self.insert_winner(winner)
                print(f"\n\nWinner is {winner.name}!\n\n")
                winner.point_reset()
                break
        return winner

    # Section 3 - Point calculation functions during 1v1 match

    @staticmethod
    def player_rps_eval(player1, player2):
        """Identifies a round winner and increases winner points by 1,
            or calls out a tie with no player points awarded"""
        move1 = player1.t_list[-1]
        move2 = player2.t_list[-1]
        p1_wins = [('rock', 'scissors'), ('scissors', 'paper'), ('paper', 'rock')]
        p2_wins = [('scissors', 'rock'), ('paper', 'scissors'), ('rock', 'paper')]
        if (move1, move2) in p1_wins:
            player1.score += 1
        elif (move1, move2) in p2_wins:
            player2.score += 1
        elif move1 == move2:
            print('Tie - no points awarded')

    @staticmethod
    def get_high_score(p1, p2):
        """Identifies the highest score between the two opponents to confirm that a
            player has at least two points (min needed to win bof3)"""
        high_score = max(p1.score, p2.score)
        return high_score

    @staticmethod
    def declare_winner(p1, p2):
        """Accepts two player class instances and compares their scores.
            Returns winner player instance"""
        if p1.score > p2.score:
            winner = p1
        else:
            winner = p2
        return winner

    def insert_winner(self, winner):
        """Adds the winner back into the bracket for gameplay against remaining opponents"""
        try:
            max_key = max(self.match_opponents.keys())
            self.match_opponents[max_key + 1] = winner
        except ValueError:
            pass

    # Section 4 - Private code for admin maintenance

    def _print_players(self):
        """Private function to print details of all player instances"""
        for player, attributes in self.players.items():
            print(attributes.__str__())
            print()


# EXECUTION LINE

if __name__ == '__main__':
    import sys
    r = RPSEngine()
    r.main_game_engine()
    sys.exit()
