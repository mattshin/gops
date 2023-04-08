class GameError(Exception):
    pass


class UnavailableBidError(GameError):
    pass


class AlreadyBidError(GameError):
    pass
