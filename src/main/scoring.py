from collections import Counter
from configs import *


class Scoring:
    @staticmethod
    def evaluate(dice: list, key: str):
        if not len(dice):
            return 0

        if key in SCORE_MAPS.keys():
            return Scoring.upper_section_eval(dice, key)

        roll_count = Counter(dice).most_common(2)
        roll_count = [count for (_, count) in roll_count]

        if key == "three_pair":
            return Scoring.three_pair_eval(dice, roll_count[0])

        elif key == "four_pair":
            return Scoring.four_pair_eval(dice, roll_count[0])

        elif key == "three_two":
            return Scoring.eval_three_two(roll_count)

        elif key == "straight":
            return Scoring.eval_sequence(dice, roll_count[0])

        return Scoring.eval_full_house(roll_count[0])

    @staticmethod
    def upper_section_eval(dice: list, key: str):
        return sum([s
                    for s in dice
                    if s == SCORE_MAPS[key]])

    @staticmethod
    def three_pair_eval(dice: list, freq: int):
        if freq >= 3:
            return sum(dice)
        return 0

    @staticmethod
    def four_pair_eval(dice: list, freq: int):
        if freq >= 4:
            return sum(dice)

        return 0

    @staticmethod
    def eval_three_two(roll_count: list):
        if roll_count == [3, 2]:
            return SCORE_THREE_TWO

        return 0

    @staticmethod
    def eval_full_house(freq: int):
        if freq == 5:
            return SCORE_FULL_HOUSE

        return 0

    @staticmethod
    def eval_sequence(dice: list, freq: int):
        sorted_dice = sorted(dice)

        if freq == 1:
            if (sorted_dice[-1] - sorted_dice[0]) == 4:
                return SCORE_STRAIGHT

        return 0
