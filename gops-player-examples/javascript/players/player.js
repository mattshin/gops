const Websocket = require('ws');

class GopsPlayer {
    constructor(strategy) {
        this.strategy = strategy
    }

    run(url='localhost:8000', gameId='test_id') {
        const ws = new Websocket(`ws://${url}/play/${gameId}?verbose=true`)

        ws.on('error', console.error)

        ws.on('message', (buffer) => {
            const data = JSON.parse(buffer.toString())
            if (data.info) {
                console.log(data.msg)
            } else {
                const bid = this.strategy(data)
                ws.send(bid)
            }
        })

        return ws
    }
}

module.exports.GopsPlayer = GopsPlayer
