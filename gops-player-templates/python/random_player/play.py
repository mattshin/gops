import json
import os
import random


import rel
import websocket


def on_message(ws, message):
    try:
        data = json.loads(message)

    except Exception as e:
        print("did not receive json, ignoring")
        print(repr(e))
        return

    if data["info"]:
        print(data)
        return

    available_bids = data["my_bids"]
    bid = random.choice(available_bids)

    print(f"sending {bid=}")
    ws.send(str(bid))


def on_error(ws, error):
    print(error)
    ws.close()


def on_close(ws, close_status_code, close_msg):
    print(f"ws connection closed with status code {close_status_code}")
    print(close_msg)


if __name__ == '__main__':
    websocket.enableTrace(True)
    gops_server = os.environ.get("GOPS_SERVER", "localhost:8000")
    game_id = os.environ.get("GAME_ID", "test_id")

    ws = websocket.WebSocketApp(f"ws://{gops_server}/play/{game_id}?verbose=true",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever(dispatcher=rel, reconnect=5)
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
