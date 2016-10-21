
CARDS = set([
    '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac',
    '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
])


class Player(object):
    def __init__(self, username):
        self.username = username

def get_player_object(name):
    #return player object from input name
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
    if card2[1] == card1[1]:  #check that suit matches
        if card_value(card1) < card_value(card2):
            return True 
    else:
        return False
  

class Trick(object):
    def __init__(self, cards_played):
        '''
            A Trick is an ordering of cards and who played them.
            The `cards` attribute is the raw trick data, a list
            of pairs (player, card)
        '''
        self.cards_played = cards_played

    def leading_suit(self):
        #returns the suit that was led
        #either 'c', 'd', 's', 'h'
        card = self.cards_played[0][1]
        card_type = card[1]
                           
        return card_type
  

    def winner(self):
        '''
            Return the player who won the trick
        '''
        winner, winning_card = self.cards_played[0]
                
        for (player, card) in self.cards_played[1:]:
            if if_dominates(winning_card, card) == True:
                winner = player
                winning_card = card     
    
        return winner

    def leader(self):
        '''
            Return the player who led the trick
        '''
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
    def deserialize(data):
        '''
            Convert the serialized representation back to a Python object
        '''

        return Trick()  # FIXME: implement this


class Hand(set):
    def __init__(self, cards):
        if not all(c in CARDS for c in cards):
            raise ValueError('A hand can only contain values from: {}'.format(CARDS))
        super().__init__(cards)


class Round(object):
    def __init__(self, players):
        '''
            A Round object tracks the state of a given round.
        '''
        self.players = players
        self.hands = dict()      # Player -> Hand
        self.tricks = []
        self.turn = None

    def is_valid_play(self, player, card):
        '''
            Validate if the given player is allowed to play the given card.
            Raise a ValueError if the move is invalid.
        '''
        pass

    def play_card(self, player, card):
        '''
            Play a given card (this method assumes the move is valid)
        '''
        pass

    def serialize(self):
        return {
            'players': self.players,
            'turn': None,   # FIXME: add player turn
            'hands': self.hands,
            'tricks': self.tricks.serialize(),
        }
