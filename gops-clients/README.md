# Player (Client)

This directory provides a variety of player clients that can interface with the
server in `/gops-engine`

## Communication

The server provides two types of messages via websockets, informational and
game state. All messages are JSON. Informational messages have the `info`
field set to `true` and contain non-critical info messages. The game state
message model is as follows:
```json5
{
    "info": false,

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

### Configuration

The following environment variables can be set to configure the player:
```
GOPS_SERVER - server address        (default "localhost:8000")
GAME_ID     - game to connect to    (default "test_id")
```

### Writing a new player

To write a new player, simply extend the `BasePlayer` class from
`players/base.py` and override the `calculate_bid` function.

The `calculate_bid` function takes the above game state as
`game_state` and returns the bid as an `int`. 


## Javascript

### quickstart
```
$ npm install
$ npm install --global pm2 # Optional

$ npx pm2 start run_player.js
```

### Writing a new player

To write a new player, create a new `.js` file that imports the `GopsPlayer`
class from `players/player.js` and pass to the constructor a function that
accepts the game state as described above and returns a bid.
