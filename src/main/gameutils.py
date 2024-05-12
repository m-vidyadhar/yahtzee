import random

from configs import *
from utils import TextFormatter as tx
from scoring import Scoring


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.score_card = PlayerScoreCard()
        return


class Dice:
    def __init__(self, n_sides):
        self.output = None
        self.n_sides = n_sides
        self.choices = list(range(1, n_sides + 1))
        return

    def roll(self):
        return random.choice(self.choices)


class DiceSet:
    def __init__(self, n_dice, n_sides=DICE_SIDES):
        self.n_dice = n_dice
        self.n_sides = n_sides
        self.outputs = self.reset_dice()
        self.dice_set = {(idx + 1): Dice(n_sides)
                         for idx
                         in range(self.n_dice)}

        return

    def reset_dice(self):
        self.outputs = [0] * self.n_dice
        return self.outputs

    def roll_set(self, mask=None):
        if mask is None:
            mask = []

        for (idx, dice) in self.dice_set.items():
            if idx in mask:
                continue

            self.outputs[idx - 1] = dice.roll()

        return self.outputs


class PlayerScoreCard:
    def __init__(self):
        self.score_card = {key: {"score": 0, "freeze": False}
                           for key in SCORES_ATTR}

        return

    def update_scores(self, dice: list, ):
        for (key, score_map) in self.score_card.items():
            if score_map["freeze"]:
                continue

            score = Scoring.evaluate(dice, key)
            self.score_card[key]["score"] = score

        return

    def freeze_score(self, key: str):
        if key not in self.score_card.keys():
            return False

        if self.score_card[key]["freeze"]:
            return False

        self.score_card[key]["freeze"] = True

        return True

    def display_scorecard(self, player_name: str):
        print("{}{:>15} {:>12}{}".format(tx.BOLD,
                                         "Category",
                                         player_name,
                                         tx.END))

        for (key, val) in self.score_card.items():
            color = tx.GREEN if val["freeze"] else tx.FAIL
            print("{:>15} {}{:>12}{}".format(key,
                                             color,
                                             val["score"],
                                             tx.END))

        return

    @property
    def score(self):
        return sum([score_maps["score"]
                    for score_maps
                    in self.score_card.values()
                    if score_maps["freeze"]])
