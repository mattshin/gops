import random

from .base import BasePlayer


class RandomPlayer(BasePlayer):
    def calculate_bid(self, game_state):
        return random.choice(game_state["my_bids"])
