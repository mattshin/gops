from .base import BasePlayer
from .polarized import PolarizedPlayer
from .util.game import get_new_game_state

class HeuristicPlayer(BasePlayer):
    SCORE_MAGIC_NUMBER = 52

    REMAINING_BID_WEIGHT = 1
    SCORE_WEIGHT = 1.2

    POLARIZATION = 0.5


    def _get_polarized_guess(self, game_state):
        polarized_player = PolarizedPlayer(polarization=self.POLARIZATION)
        return polarized_player.calculate_bid(game_state)


    def _get_heuristic(self, game_state):
        if game_state["my_score"] >= self.SCORE_MAGIC_NUMBER:
            return 10000
        elif game_state["their_score"] >= self.SCORE_MAGIC_NUMBER:
            return -10000

        bid_diff = sum(game_state["my_bids"]) - sum(game_state["their_bids"])
        score_diff = game_state["my_score"] - game_state["their_score"]

        return bid_diff * self.REMAINING_BID_WEIGHT + score_diff * self.SCORE_WEIGHT
    

    def calculate_bid(self, game_state):
        """
        1. guess opponents bid given distribution of own guess
        2. return bid that maximizes heuristic against guess
        """

        polarized_guess = self._get_polarized_guess(game_state)
        opponent_heuristics = list()
        for opponent_bid in game_state["their_bids"]:
            new_state = get_new_game_state(game_state, my_bid=polarized_guess, their_bid=opponent_bid)
            opponent_heuristics.append(self._get_heuristic(new_state))
        
        opponent_guess = game_state["their_bids"][opponent_heuristics.index(min(opponent_heuristics))]
        best_bid = -1
        best_score = -10001
        for bid in game_state["my_bids"]:
            new_state = get_new_game_state(game_state, my_bid=bid, their_bid=opponent_guess)
            if heuristic := self._get_heuristic(new_state) > best_score:
                best_score = heuristic
                best_bid = bid

        return best_bid
