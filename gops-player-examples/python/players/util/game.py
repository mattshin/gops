import copy

def get_new_game_state(game_state, my_bid, their_bid):
    new_state = copy.deepcopy(game_state)

    new_state["all_bounties"].remove(new_state["active_bounty"])
    new_state["my_bids"].remove(my_bid)
    new_state["their_bids"].remove(their_bid)
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
