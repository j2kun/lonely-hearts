from api import strings


class HeartsException(Exception):
    def serialize(self):
        return {
            'error': str(self)
        }


class InvalidPlay(HeartsException):
    def __init__(self, card, reason):
        self.card = card
        self.reason = reason

    def str(self):
        return strings.INVALID_PLAY.format(self.card, self.reason)
