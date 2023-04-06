GOPS
> Game of Pure Strategy

Game of Pure Strategy (GOPS) is a two player turn-based game where the
objective is to win as many "bounties" by bidding more than your
opponent over the course of 13 rounds. 

This repository contains the code to run the server for playing games, as well
as some example clients that can be used to interact with the server.

# GOPS Rules

After setting up, play 13 rounds as described below. After the 13th round,
whichever player has collected the highest value of bounties is the winner.

### Setup
Both players get a pool of 13 "bids", numbered 2 through 14. There is also a
pool of 13 "bounties", also valued 2 through 14.

### Gameplay
At the start of each round, randomly reveal a bounty from the pool. Each player
secretly picks a bid from their remaining pool of available bids. Once both
players have chosen, the player that bid the higher amount takes the bounty.

If there was a tie, the bounty is set aside and the next round is played. The
winner of the second round takes both the bounty for that round as well the
bounties for all the tied rounds leading up to that round.

If the game ends with a tie round, nobody wins the tie bounty.

At the end of all 13 rounds, each player sums the value of their won bounties.
The player with the highest score wins!

# Server
The server is a FastAPI python server that uses websockets to manage games.
For more info, refer to the README in `gops-engine`.

# Client
There is technically a dev UI that can be used to play games, but it is highly
recommended to write ones own client that can interact with the server and play
games. Example clients are provided in the `gops-player-template` directory.