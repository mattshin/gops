import argparse

import players


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("player")

    args = parser.parse_args()
    try:
        PlayerClass = getattr(players, args.player)

    except AttributeError:
        print(f"couldn't find player type {args.player}")

    player = PlayerClass()
    player.run()
