import random


class GameState:
    available_bounties = list(range(2, 15))
    available_bids = [list(range(2, 15)), list(range(2, 15))]
    scores = [0, 0]
    tie = 0

    live = False

    _active_bounty = None
    _active_bids = [None, None]
    _players_available = [0, 1]

    def __init__(self):
        self._active_bounty = random.choice(self.available_bounties)

    def _is_live(self):
        return not len(self._players_available) and not self.game_over()

    def get_next_player_id(self, game_id):
        if not self._players_available:
            raise RuntimeError(f"Tried to get third player for {game_id=}")
        current_player = self._players_available.pop(0)

        self.live = self._is_live()
        return current_player

    def remove_player(self, player_id):
        if player_id not in range(2):
            return None
        if player_id in self._players_available:
            return None

        self._players_available.append(player_id)
        self.live = False

    def get_state(self, player: int = 0):
        return {
            "bounties": self.available_bounties,
            "tie_bounty": self.tie,
            "my_score": self.scores[player],
            "my_bids": self.available_bids[player],
            "their_score": self.scores[1 - player],
            "their_bids": self.available[1 - player],
        }

    def get_bounty(self) -> int:
        if not len(self.available_bounties):
            return -1

        if not self._active_bounty:
            self._active_bounty = random.choice(self.available_bounties)

        return self._active_bounty

    def _process_bids(self) -> int:
        if not all(self._active_bids):
            raise RuntimeError("Cannot process bids without both bids")

        self.available_bounties.remove(self._active_bounty)
        for player in range(2):
            self.available_bids[player].remove(self._active_bids[player])

        if self._active_bids[0] == self._active_bids[1]:
            self.tie += self._active_bounty
            self._active_bounty = None
            self._last_round_details = {
                "tie": True,
                "tie_bounty": self.tie
            }
            return -1

        winner = 0 if self._active_bids[0] > self._active_bids[1] else 1
        self.scores[winner] += self._active_bounty + self.tie
        self._last_round_details = {
                "tie": False,
                "winner": winner,
                "total_won": self._active_bounty + self.tie,
                "winning_bid": self._active_bids[winner]
            }
        self.tie = 0
        self._active_bounty = None
        self._active_bids = [None, None]

        return winner

    # Returns True if bid ended auction for turn, False otherwise
    def queue_bid(self, player, bid) -> bool:
        if bid not in self.available_bids[player]:
            return False
        if self._active_bids[player]:  # Already bid!
            return False

        self._active_bids[player] = bid
        if all(self._active_bids):
            self._process_bids()
            return True

        return False

    def game_over(self) -> bool:
        self.live = False
        return not bool(len(self.available_bounties))

    def winner(self) -> int:
        match self.scores[0] - self.scores[1]:
            case diff if diff < 0:
                return 1
            case 0:
                return -1
            case diff if diff > 0:
                return 0
    
    def last_round_details(self):
        details = self._last_round_details
        if details["tie"]:
            return f"last round was a tie. tie bounty is now {details['tie_bounty']}"
        return f"player {details['winner']} won the bounty of {details['total_won']} with a bid of {details['winning_bid']}"

    def deserialize(self):
        return f"""
Current Bounty: {self._active_bounty}
All Available Bounties: {self.available_bounties}
Tie Bounty: {self.tie}
Player 0:
    Score: {self.scores[0]}
    Remaining Bids: {self.available_bids[0]}
Player 1:
    Score: {self.scores[1]}
    Remaining Bids: {self.available_bids[1]}
"""
