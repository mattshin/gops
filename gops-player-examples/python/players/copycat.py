from .base import BasePlayer


class CopycatPlayer(BasePlayer):
    def calculate_bid(self, game_state):
        return game_state["active_bounty"]
