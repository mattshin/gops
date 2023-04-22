from .base import BasePlayer
from .polarized import PolarizedPlayer
from .util.game import get_next_game_state, swap_perspective

class HeuristicPlayer(BasePlayer):
    SCORE_MAGIC_NUMBER = 52

    REMAINING_BID_WEIGHT = 1.2
    SCORE_WEIGHT = 1

    POLARIZATION = -0.8

    def __init__(self):
        self.polarized_player = PolarizedPlayer(polarization=self.POLARIZATION)


    def _get_normalized_distribution(self, game_state):
        weights = self.polarized_player._get_probability_distribution(game_state)
        return [ float(weight)/sum(weights) for weight in weights ]


    def _get_heuristic(self, game_state):
        if game_state["my_score"] > self.SCORE_MAGIC_NUMBER:
            return 99999
        elif game_state["their_score"] > self.SCORE_MAGIC_NUMBER:
            return -99999

        bid_diff = sum(game_state["my_bids"]) - sum(game_state["their_bids"])
        score_diff = game_state["my_score"] - game_state["their_score"]

        return bid_diff * self.REMAINING_BID_WEIGHT + score_diff * self.SCORE_WEIGHT
    

    def calculate_bid(self, game_state):
        opponent_guess_weights = self._get_normalized_distribution(swap_perspective(game_state))

        best_bid = -1
        best_score = -100000
        for bid in game_state["my_bids"]:
            heuristics = [
                self._get_heuristic(get_next_game_state(game_state, my_bid=bid, their_bid=their_bid))
                for their_bid in game_state["their_bids"]
            ]
            weighted_heuristic = sum(h * w for (h, w) in zip(heuristics, opponent_guess_weights))
            if weighted_heuristic > best_score:
                best_score = weighted_heuristic
                best_bid = bid

        return best_bid
