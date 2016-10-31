from random import shuffle


def get_player_object(name):
    # return player object from input name
    pass


class Player(object):
    def __init__(self, username):
        self.username = username


class Game(object):
    def __init___(self, players):
        pass


class Card(object):
    rank_values = {
        '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
        'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14,
    }

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def validate(self):
        if self.rank not in Card.rank_values:
            raise ValueError('Invalid rank {}'.format(self.rank))
        if self.suit not in ['h', 's', 'c', 'd']:
            raise ValueError('Invalid suit {}'.format(self.suit))

    @staticmethod
    def deserialize(serialized):
        rank, suit = serialized[0], serialized[1]
        card = Card(rank, suit)
        card.validate()
        return card

    def serialize(self):
        return ''.join([self.rank, self.suit])

    @property
    def integer_rank(self):
        return Card.rank_values[self.rank]

    def dominates(self, other):
        return self.suit == other.suit and self.integer_rank > other.integer_rank

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit


CARDS = [Card.deserialize(c) for c in [
    '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac',
    '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
]]


class Hand(list):
    def __init__(self, cards):     # cards is a list of cardnames
        if not all(c in CARDS for c in cards):
            raise ValueError('A hand can only contain values from: {}'.format(CARDS))
        super().__init__(cards)

    def has_suit(self, suit):  # suit is either 'c', 'd', 'h', or 's'
        for card in self:
            if card.suit == suit:
                return True
        return False

    def sorted(self):
        pass


class Error(Exception):
    pass


class CardError(Error):
    pass


class HeartsError(Error):
    pass


class EarlyDumpError(Error):
    ''' For when a player tries to dump on the first round'''
    pass


class Round(object):
    def __init__(self, players):
        '''
            A Round object tracks the state of a given round.
        '''
        self.players = players   # List of players in seated order
        self.hands = dict()      # Player -> Hand
        self.tricks = []         # Should all 13 tricks be initialized at the beginning?
        self.turn = None
        self.hearts_broken = False
        self.who_starts = None   # Player with '2c'

        self.deal()

    def deal(self):
        deck = CARDS
        shuffle(deck)
        for n in range(4):
            self.hands[self.players[n]] = Hand(deck[13*n:13*(n+1)])

    def can_follow_suit(self, player, trick):
        hand = self.hands[player]
        return hand.has_suit(trick.suit)

    def is_valid_lead(self, player, card):
        if card.suit == 'h' and not self.hearts_broken:
            if not all(card.suit == 'h' for card in self.hands[player]):
                raise HeartsError
            else:  # Player has no other available suit to lead with
                self.hearts_broken = True
        return

    def is_valid_follow(self, player, trick, card):
        if card.suit == trick.suit:
            return
        else:
            if self.can_follow_suit(player, trick):
                raise CardError
            else:
                if card.suit == 'h':
                    self.heartsbroken = True
                return

    def make_new_trick(self, player, card):
        self.tricks.append(Trick([(player, card)]))

    def add_to_last_trick(self, player, card):
        last_trick = self.tricks[-1]
        last_trick.cards_played.append((player, card))

    def lead_the_trick(self, player, card):
        try:
            # Check if led card is valid
            self.make_new_trick(player, card)
        except HeartsError:
            # Player tries to lead with 'h' but hearts are not broken
            pass

    def follow_the_trick(self, player, trick, card):
        try:
            self.is_valid_follow(player, trick, card)
            self.add_to_last_trick(player, card)
        except CardError:  # Player has suit but did not follow
            pass

    def play_card(self, player, card):
        last_trick = self.tricks[-1]

        # First Hand
        if True:
            pass

        # leading a Trick
        elif last_trick.size == 4 and player == last_trick.winner():
            self.lead_the_trick(player, card)

        # following a Trick
        else:
            self.follow_the_trick(player, last_trick, card)

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
        first_card = self.cards_played[0][1]
        self.suit = first_card.suit
        self.size = len(self.cards_played)

    def winner(self):
        winner, winning_card = self.cards_played[0]

        for (player, card) in self.cards_played[1:]:
            if card.dominates(winning_card):
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
            player.username: dict(turn=i, card=card.serialize())
            for (i, (player, card)) in enumerate(self.cards_played)
        }

    @staticmethod
    def deserialize(trick_data):
        # trick_data is a dictionary with keys('player name')
        # and values( dict{ 'turn': int, 'card': 'cardname'} )

        play_sequence = [0, 0, 0, 0]
        for username, play in trick_data.items():
            play_sequence[play['turn']] = (Player(username), Card.deserialize(play['card']))
        return Trick(play_sequence)
