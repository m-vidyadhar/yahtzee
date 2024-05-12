from game import BaseYahtzee

from configs import N_ROLLS_PER_TURN
from configs import SCORES_ATTR


class Yahtzee(BaseYahtzee):
    def __init__(self, n_dice=5):
        super().__init__(n_dice=n_dice)

        return

    def turn(self, ):
        self.reset_turn()

        while True:
            if (self.n_roll + 1) > N_ROLLS_PER_TURN:
                break

            dice_roll = self.dice.roll_set(mask=self.dice_mask)
            self.active_player.score_card.update_scores(dice=dice_roll)
            self.refresh_game()

            self.dice_selection()

            status = self.score_selection()
            if status:
                break

            self.n_roll += 1

        self.active_player.score_card.update_scores([])

        return

    def play(self):
        for _ in SCORES_ATTR:
            for player in self.players:
                self.active_player = player
                self.turn()

        scores = [player.score for player in self.players]
        max_score = max(scores)

        return max_score


if __name__ == "__main__":
    y = Yahtzee()
    print(y.play())
