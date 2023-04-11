import json
import os

import rel
import websocket


class BasePlayer():

    def calculate_bid(self, game_state) -> int:
        raise NotImplementedError

    def on_message(self, ws, message):
        try:
            data = json.loads(message)

        except Exception as e:
            print("did not receive json, ignoring")
            print(repr(e))
            return

        if data["info"]:
            print(data)
            return

        bid = self.calculate_bid(data)

        print(f"sending {bid=}")
        ws.send(str(bid))

    def on_error(self, ws, error):
        print(error)
        ws.close()

    def on_close(self, _, close_status_code, close_msg):
        print(f"ws connection closed with status code {close_status_code}")
        print(close_msg)

    def run(self):
        websocket.enableTrace(True)
        gops_server = os.environ.get("GOPS_SERVER", "localhost:8000")
        game_id = os.environ.get("GAME_ID", "test_id")

        ws = websocket.WebSocketApp(f"ws://{gops_server}/play/{game_id}?verbose=true",
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)

        ws.run_forever(dispatcher=rel, reconnect=5)
        rel.signal(2, rel.abort)  # Keyboard Interrupt
        rel.dispatch()
