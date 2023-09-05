import random

from app.exceptions import AlreadyBidError, UnavailableBidError


class GameState:
    available_bounties = list(range(2, 15))
    available_bids = [list(range(2, 15)), list(range(2, 15))]
    scores = [0, 0]
    tie = 0
    move_history = list()

    live = False

    _active_bounty = None
    _active_bids = [None, None]
    _players_available = [0, 1]

    def __init__(self):
        self._active_bounty = random.choice(self.available_bounties)
        print(self.deserialize())

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
            "player_id": player,
            "active_bounty": self._active_bounty,
            "all_bounties": self.available_bounties,
            "tie_bounty": self.tie,
            "my_score": self.scores[player],
            "my_bids": self.available_bids[player],
            "their_score": self.scores[1 - player],
            "their_bids": self.available_bids[1 - player],
            "move_history": self.move_history,
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

        def _reset_round():
            self._active_bounty = None
            self._active_bids = [None, None]

        self.available_bounties.remove(self._active_bounty)
        for player in range(2):
            self.available_bids[player].remove(self._active_bids[player])

        self.move_history.append((self._active_bounty, self._active_bids[0], self._active_bids[1]))

        if self._active_bids[0] == self._active_bids[1]:
            self.tie += self._active_bounty
            self._last_round_details = {
                "tie": True,
                "bid": self._active_bids[0],
                "tie_bounty": self.tie
            }
            _reset_round()
            return -1

        winner = 0 if self._active_bids[0] > self._active_bids[1] else 1
        self.scores[winner] += self._active_bounty + self.tie
        self._last_round_details = {
                "tie": False,
                "winner": winner,
                "total_won": self._active_bounty + self.tie,
                "winning_bid": self._active_bids[winner],
                "losing_bid": self._active_bids[1-winner]
            }
        self.tie = 0
        _reset_round()

        return winner

    # Returns True if bid ended auction for turn, False otherwise
    def queue_bid(self, player, bid) -> bool:
        if bid not in self.available_bids[player]:
            raise UnavailableBidError(f"bid value {bid} already used")
        if self._active_bids[player]:  # Already bid!
            raise AlreadyBidError(f"already placed bid of {self._active_bids[player]}")

        self._active_bids[player] = bid
        if all(self._active_bids):
            self._process_bids()
            return True

        return False

    def turn_number(self) -> int:
        if not self._is_live():
            return -1
        return 14 - len(self.available_bounties)

    def game_over(self) -> bool:
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
            return (f"last round was a tie, both bids were {details['bid']}. "
                    f"tie bounty is now {details['tie_bounty']}")
        return (f"player {details['winner']} "
                f"won the bounty of {details['total_won']} "
                f"with a bid of {details['winning_bid']}. "
                f"player {1-details['winner']}'s bid was {details['losing_bid']}")

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
