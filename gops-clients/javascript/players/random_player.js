const { GopsPlayer } = require("./player")

const calculateBid = (gameState) => {
    randomIndex = ~~(Math.random() * gameState["my_bids"].length)
    return gameState["my_bids"][randomIndex]
}

module.exports.randomPlayer = new GopsPlayer(calculateBid)
