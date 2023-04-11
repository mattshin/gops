# Player (Client)

This directory provides a variety of player clients that can interface with the
server in `/gops-engine`

## Communication

The server provides two types of messages via websockets, informational and
game state. All messages are JSON. The game state message model is as follows:
```json5
{
    "active_bounty": int,        // Bounty for current round
    "all_bounties": List[int],   // All remaining bounties, including active
    "tie_bounty": int,           // Total bounty from unresolved ties
    "my_score": int,             // Player's score
    "my_bids": List[int],        // Player's remaining bids
    "their_score": int,          // Opponent's score
    "their_bids": List[int]      // Opponent's remaining bids
}
```

## Python

### quickstart

```
$ poetry install
$ poetry run python3 run_player.py RandomPlayer
```

### Writing a new player

To write a new player, simply extend the `BasePlayer` class from
`players/base.py` and override the `calculate_bid` function.

The `calculate_bid` function takes the above game state as the
`game_state` parameter and returns an `int`. 


## Javascript

Coming soon :)
