import argparse

import players


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("player")

    args = parser.parse_args()
    try:
        PlayerClass = getattr(players, args.player)
        player = PlayerClass()

    except (AttributeError, NameError):
        print(f"couldn't find player type {args.player}")

    player.run()
