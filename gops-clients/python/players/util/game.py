import copy
import random


def get_new_game_state():
    INITIAL_GAME_STATE = {
        "active_bounty": 0,
        "all_bounties": list(range(2, 15)),
        "tie_bounty": 0,
        "my_score": 0,
        "my_bids": list(range(2, 15)),
        "their_score": 0,
        "their_bids": list(range(2, 15)),
        "move_history": list(),
    }

    new_game_state = copy.deepcopy(INITIAL_GAME_STATE)
    new_game_state["active_bounty"] = random.choice(range(2, 15))

    return new_game_state


def get_next_game_state(game_state, my_bid, their_bid):
    new_state = copy.deepcopy(game_state)

    new_state["all_bounties"].remove(new_state["active_bounty"])
    new_state["my_bids"].remove(my_bid)
    new_state["their_bids"].remove(their_bid)
    new_state["move_history"].append((my_bid, their_bid, new_state["active_bounty"], new_state["tie_bounty"]))

    if my_bid == their_bid:
        new_state["tie_bounty"] += new_state["active_bounty"]
        new_state["active_bounty"] = 0
        return new_state

    if my_bid > their_bid:
        new_state["my_score"] += new_state["active_bounty"] + new_state["tie_bounty"]
        new_state["active_bounty"] = new_state["tie_bounty"] = 0

    elif their_bid > my_bid:
        new_state["their_score"] += new_state["active_bounty"] + new_state["tie_bounty"]
        new_state["active_bounty"] = new_state["tie_bounty"] = 0

    return new_state


def swap_perspective(game_state):
    alt_perspective = copy.deepcopy(game_state)
    alt_perspective["my_bids"], alt_perspective["their_bids"] = \
        alt_perspective["their_bids"], alt_perspective["my_bids"]
    alt_perspective["my_score"], alt_perspective["their_score"] = \
        alt_perspective["their_score"], alt_perspective["my_score"]
    return alt_perspective
