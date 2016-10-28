
CARDS = set([
    '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac',
    '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
])


def get_player_object(name):
    # return player object from input name
    pass


def card_value(card):
    number = card[0]
    if number == 'T':
        return 10
    elif number == 'J':
        return 11
    elif number == 'Q':
        return 12
    elif number == 'K':
        return 13
    elif number == 'A':
        return 14
    else:
        return int(number)


def if_dominates(card1, card2):
    if card2[1] == card1[1] and card_value(card1) < card_value(card2):
        return True
    else:
        return False


class Player(object):
    def __init__(self, username):
        self.username = username


class Game(object):
    def __init___(self, players):
        pass


class Hand(set):
    def __init__(self, cards):     # cards is a list of cardnames
        if not all(c in CARDS for c in cards):
            raise ValueError('A hand can only contain values from: {}'.format(CARDS))
        super().__init__(cards)

    def has_suit(self, suit):  # suit is either 'c', 'd', 'h', or 's'
        for card in self:
            if card[1] == suit:
                return True
        return False


class Round(object):
    def __init__(self, players):
        '''
            A Round object tracks the state of a given round.
            TO DO: 1. Keep track of who_starts and whose turn it is
        '''
        self.players = players   # List of players in seated order
        self.hands = dict()      # Player -> Hand
        self.tricks = []         # Should all 13 tricks be initialized at the beginning?
        self.turn = None
        self.hearts_broken = False
        self.who_starts = None   # Player with '2c'

        self.deal()

    def deal(self):
        # Populate self.hands with a random deal
        pass

    def can_follow_suit(self, player, trick):
        current_hand = self.hands[player]
        return current_hand.has_suit(trick.suit)

    def is_hearts_broken(self):
        if self.hearts_broken:
            return
        else:
            # Raise an error "hearts haven't been broken!"
            pass

    def is_valid_play(self, player, card, trick):
        '''
            Validate if the given player is allowed to play the given card.
            Raise a ValueError if the card is invalid.  Assume that the play
            is a continuation of a trick.
        '''
        pass

    def play_card(self, player, card):
        '''
            Play a given card (assuming it's the player's turn and card is valid)
        '''
        last_trick = self.tricks[-1]

        # The very first play
        if '2c' in self.hands[player]:
            new_trick = Trick([(player, '2c')])
            self.tricks.append(new_trick)

        # Check if player is the winner of previous hand to start new trick
        elif len(last_trick.cards_played) == 4 and player == last_trick.winner():
            if card[1] == 'h':
                try:
                    self.is_hearts_broken()
                    new_trick = Trick([player, card])
                    self.tricks.append(new_trick)
                except ValueError:
                    # Hearts have not been broken
                    pass
        else:
            try:
                self.is_valid_play(player, card, last_trick)
                last_trick.cards_played.append((player, card))
            except ValueError:
                # Do something (card is not the same suit as the leading suit
                # and player has that suit.
                pass

    def serialize(self):
        return {
            'players': self.players,
            'turn': None,   # FIXME: add player turn
            'hands': self.hands,
            'tricks': [trick.serialize() for trick in self.tricks],
        }


class Trick(object):
    def __init__(self, cards_played):
        '''
            A Trick is an ordering of cards and who played them.
            The `cards` attribute is the raw trick data, a list
            of pairs (player, card).  Trick is assumed to be initialized by
            a non-empty list.
        '''
        self.cards_played = cards_played
        self.suit = self.cards_played[0][1][1]

    def winner(self):

        winner, winning_card = self.cards_played[0]

        for (player, card) in self.cards_played[1:]:
            if if_dominates(winning_card, card):
                winner = player
                winning_card = card
        return winner

    def leader(self):
        # return the Player who led the trick
        return self.cards_played[0][0]

    def serialize(self):
        '''
            Return a serialized representation of the trick
        '''
        return {
            player.username: dict(turn=i, card=card)
            for (i, (player, card)) in enumerate(self.cards_played)
        }

    @staticmethod
    def deserialize(trick_data):
        # trick_data is a dictionary with keys('player name')
        # and values( dict{ 'turn': int, 'card': 'cardname'} )

        play_sequence = [0, 0, 0, 0]
        for username, play in trick_data.items():
            play_sequence[play['turn']] = (Player(username), play['card'])
        return Trick(play_sequence)
