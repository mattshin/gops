import random

from .base import BasePlayer

DEFAULT_POLARIZATION = 0.5

class PolarizedPlayer(BasePlayer):
    """
    Polarization should be between [-1, 1] and measures concavity.
    Low polarization favors bids near the bounty. High polarization
    favors bids far from the bounty.

    A polarization of 0 is the uniform distribution.
    """

    def __init__(self, polarization=DEFAULT_POLARIZATION):
        self.polarization = polarization


    def _get_probability_distribution(self, game_state):
        bounty = game_state["active_bounty"]
        bounty_index = game_state["all_bounties"].index(bounty)
        lower_bids = game_state["my_bids"][:bounty_index]
        upper_bids = game_state["my_bids"][bounty_index:]

        lower_weights = [(bounty - bid)/len(lower_bids) for bid in lower_bids]
        upper_weights = [(bid - bounty + 1)/(len(upper_bids) + 1) for bid in upper_bids]

        polarized_weights = [
            (1 - self.polarization) +
            (2 * self.polarization * weight)
            for weight in lower_weights + upper_weights
        ]

        distribution = [weight - min(polarized_weights) + 1 for weight in polarized_weights]
        return distribution
    

    def calculate_bid(self, game_state):
        bid_distribution = self._get_probability_distribution(game_state)
        return random.choices(game_state["my_bids"], weights=bid_distribution)[0]
