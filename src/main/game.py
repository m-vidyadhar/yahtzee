from gameutils import DiceSet, Player
from utils import TextFormatter as tx
from configs import N_ROLLS_PER_TURN

import os


def get_freeze_key():
    key = input("Select SCORE CATEGORY to freeze: ")
    return key.strip()


class BaseYahtzee:
    def __init__(self, n_dice=5):

        self.n_players = int(input("Number of players: "))
        self.n_dice = n_dice
        self.dice_mask = []
        self.n_roll = 0
        self.active_player = None

        # Defining the dice set, players
        self.dice = DiceSet(n_dice)
        self.players = self.init_players()

        self.refresh_game()
        return

    def init_players(self):
        player_names = [input(f"Player name {idx + 1}: ")
                        for idx
                        in range(self.n_players)]

        players = [Player(player_name) for player_name in player_names]

        return players

    def score_selection(self, ):
        status = False
        key = ""

        while not status:
            key = get_freeze_key()
            if (self.n_roll + 1) >= N_ROLLS_PER_TURN:
                status = self.active_player.score_card.freeze_score(key)
            else:
                if bool(key):
                    status = self.active_player.score_card.freeze_score(key)
                else:
                    status = True

        self.refresh_game()

        return status and bool(key)

    def dice_selection(self, ):
        if (self.n_roll + 1) < N_ROLLS_PER_TURN:
            self.dice_mask = input("Select DICE to FREEZE: ")
            self.dice_mask = [int(i)
                              for i
                              in self.dice_mask.split()]

            self.refresh_game()
        return

    def reset_turn(self):
        self.dice.reset_dice()
        self.dice_mask = []
        self.n_roll = 0
        self.refresh_game()

        input("Press ENTER to roll: ")

        return

    def get_player_names(self):
        return [player.name for player in self.players]

    def display_line(self):
        print("-" * (15 + 12 * self.n_players))

        return

    def display_title(self, ):
        if self.active_player is None:
            active_name = ""
        else:
            active_name = self.active_player.name

        player_names = []

        for player_ in self.players:
            if player_.name == active_name:
                player_name = "{}{:>12}{}".format(tx.GREEN,
                                                  active_name + "*",
                                                  tx.END)

            else:
                player_name = "{:>12}".format(player_.name)

            player_names.append(player_name)

        title_row = (tx.BOLD + "{:>15}" + "".join(player_names) + tx.END)
        print(title_row.format("Category"))
        self.display_line()

        return

    def display_dice(self,):
        rolled_dice = self.dice.outputs
        rolled_dice = ["{}{:4}{}".format(tx.GREEN if (idx + 1) in self.dice_mask else tx.BLUE,
                                         roll,
                                         tx.END)
                       for (idx, roll) in enumerate(rolled_dice)]

        roll_status = f"Dice ({self.n_roll + 1} / {N_ROLLS_PER_TURN})"
        print("{:>15}".format(roll_status), "".join(rolled_dice))
        self.display_line()

        return

    def display_scores(self):
        score_items = self.players[0].score_card.score_card.items()

        for (key, _) in score_items:
            scores = ["{}{:>12}{}".format((tx.GREEN
                                           if player.score_card.score_card[key]["freeze"]
                                           else tx.FAIL),
                                          player.score_card.score_card[key]["score"],
                                          tx.END)
                      for player
                      in self.players]

            print("{:>15}".format(key) + "".join(scores))

        self.display_line()

        return

    def display_total(self):
        scores = ["{}{:>12}{}".format(tx.GREEN,
                                      player.score_card.score,
                                      tx.END)
                  for player in self.players]

        print(tx.BOLD + "{:>15}".format("Total")
              + "".join(scores)
              + tx.END)

        self.display_line()

        return

    def refresh_game(self, ):
        os.system("clear")

        self.display_title()
        self.display_scores()
        self.display_total()
        self.display_dice()
        return
