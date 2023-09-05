import argparse
import copy
import json
import random

import players
from players.util.game import get_new_game_state, get_next_game_state, swap_perspective

DEFAULT_NUM_GAMES = 1


def sim_game(player_one: players.BasePlayer, player_two: players.BasePlayer, verbose=False):
    game_state = get_new_game_state()
    for i in range(13):
        game_state["active_bounty"] = random.choice(game_state["all_bounties"])
        bids = [player_one.calculate_bid(game_state), player_two.calculate_bid(swap_perspective(game_state))]
        bounty = game_state['active_bounty'] + game_state['tie_bounty']

        game_state = get_next_game_state(
            game_state,
            bids[0],
            bids[1]
        )

        if verbose:
            print(f"------ round {i+1} ------")
            print(f"total bounty: {bounty}")
            print(f"player 1 bid: {bids[0]}")
            print(f"player 2 bid: {bids[1]}\n")

            print(f"remaining bounties: {game_state['all_bounties']}")
            print(f"player 1 bids left: {game_state['my_bids']}")
            print(f"player 2 bids left: {game_state['their_bids']}\n")

            print(f"player 1 score: {game_state['my_score']}")
            print(f"player 2 score: {game_state['their_score']}\n")

    if game_state["my_score"] > game_state["their_score"]:
        return "p1 win"
    elif game_state["their_score"] > game_state["my_score"]:
        return "p2 win"
    else:
        return "tie"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num-games", type=int, default=DEFAULT_NUM_GAMES)
    parser.add_argument("--p1")
    parser.add_argument("--p1-args", type=json.loads, default={})
    parser.add_argument("--p2")
    parser.add_argument("--p2-args", type=json.loads, default={})
    parser.add_argument("--verbose", action='store_true', default=False)

    args = parser.parse_args()
    try:
        PlayerClasses = [getattr(players, args.p1), getattr(players, args.p2)]
        player_one = PlayerClasses[0](**args.p1_args)
        player_two = PlayerClasses[1](**args.p2_args)

    except (AttributeError, NameError):
        print(f"couldn't find player type {args.player}")

    history = {
        "p1 win": 0,
        "p2 win": 0,
        "tie": 0
    }

    for _ in range(args.num_games):
        outcome = sim_game(player_one, player_two, args.verbose)
        history[outcome] += 1

    print(history)
