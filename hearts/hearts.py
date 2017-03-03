from random import shuffle


class Player(object):
    def __init__(self, username):
        self.username = username

    def __eq__(self, other):
        return self.username == other.username

    def __hash__(self):
        return hash(self.username)


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

    def is_worth_points(self):
        return self.suit == 'h' or self == Card('Q', 's')

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

    def __repr__(self):
        return self.serialize()

    def __str__(self):
        return self.serialize()


CARDS = [Card.deserialize(c) for c in [
    '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac',
    '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
]]


class Hand(list):
    def __init__(self, cards):     # cards is a list of Card objects
        if not all(c in CARDS for c in cards):
            raise ValueError('A hand can only contain values from: {}'.format(CARDS))
        super().__init__(cards)

    def has_suit(self, suit):
        for card in self:
            if card.suit == suit:
                return True
        return False

    def is_only_hearts(self):
        return all(card.suit == 'h' for card in self)

    def has_only_hearts_and_Qs(self):
        return all(card.is_worth_points() for card in self)

    def hand_sort(self):  # Sort the hand by suit alphabetically, then by rank.
        self.sort(key=lambda card: (card.suit, Card.rank_values[card.rank]))

    def serialize(self):
        return [card.serialize() for card in self]

    @staticmethod
    def deserialize(serialized):
        return Hand([Card.deserialize(some_card) for some_card in serialized])

    def __eq__(self, other):
        return {card.serialize() for card in self} == {card.serialize() for card in other}


class Round(object):
    def __init__(self, players):
        '''
            A Round object tracks the state of a given round.
        '''
        self.players = players   # List of players in seated order
        self.hands = dict()      # Player -> Hand
        self.tricks = []
        self.turn_counter = 0
        self.hearts_broken = False

        self.deal()
        self.set_turn_counter()

    @property
    def next_player(self):
        return self.players[self.turn_counter]

    def deal(self):
        deck = CARDS.copy()
        shuffle(deck)
        for n in range(4):
            start_hand = Hand(deck[13*n:13*(n+1)])
            start_hand.hand_sort()
            self.hands[self.players[n]] = start_hand

    def set_turn_counter(self):
        for index in range(4):
            if Card('2', 'c') in self.hands[self.players[index]]:
                self.turn_counter = index

    def can_follow_suit(self, player, trick):
        hand = self.hands[player]
        return hand.has_suit(trick.suit)

    def is_valid_lead(self, player, card):
        '''
           Return a boolean for whether the player can use the given card
           to start the trick.
        '''
        if len(self.tricks) == 0:
            return card == Card('2', 'c')
        elif card.suit == 'h' and not self.hearts_broken:
            return self.hands[player].is_only_hearts()
        else:
            return True

    def is_valid_follow(self, player, trick, card):
        '''
            Return a boolean for whether the player
            can use the given card to follow the trick
        '''
        if self.can_follow_suit(player, trick):
            return card.suit == trick.suit
        elif len(self.tricks) == 1:
            player_hand = self.hands[player]
            if card.is_worth_points():
                return player_hand.has_only_hearts_and_Qs()
            else:
                return True
        else:
            return True

    def is_player_turn(self, player):
        return self.players[self.turn_counter] == player

    def make_new_trick(self, player, card):
        self.tricks.append(Trick([(player, card)]))

    def add_to_last_trick(self, player, card):
        last_trick = self.tricks[-1]
        last_trick.cards_played.append((player, card))

    def lead_the_trick(self, player, card):
        if self.is_valid_lead(player, card):
            self.make_new_trick(player, card)
            self.upkeep(player, card)
        else:
            raise ValueError('Invalid lead: {}'.format(card))

    def follow_the_trick(self, player, card):
        last_trick = self.tricks[-1]
        if self.is_valid_follow(player, last_trick, card):
            self.add_to_last_trick(player, card)
            self.upkeep(player, card)
        else:
            raise ValueError('Invalid play: {}'.format(card))

    def upkeep(self, player, card):
        '''
        Removes a played card from a hand, updates the turn counter,
        and updates when hearts get broken.
        '''
        self.hands[player].remove(card)
        if self.hearts_broken is False and card.suit == 'h':
            self.hearts_broken = True

        last_trick = self.tricks[-1]
        if len(last_trick) < 4:
            self.turn_counter = (self.turn_counter + 1) % 4
        else:
            self.turn_counter = self.players.index(last_trick.winner())

    def play_card(self, player, card):
        if self.is_player_turn(player):
            if len(self.tricks) == 0 or len(self.tricks[-1]) == 4:
                self.lead_the_trick(player, card)
            else:
                self.follow_the_trick(player, card)
        else:
            raise ValueError("Invalid play: it's not your turn")

    def current_scores(self):
        '''
        Returns {player: int}.  Calculates the current number of points
        for all tricks completed so far. Assumes the basic Hearts rules.
        '''
        scores = {player: 0 for player in self.players}
        for trick in self.tricks:
            scores[trick.winner()] += trick.points()
        return scores

    def shot_the_moon(self):
        '''
        Returns {player: Bool}.  Bool is True if and only if player's
        score is 26 (based on the standard Hearts rules).  Function can
        be called at any time during the round.
        '''
        d = {player: False for player in self.players}
        scores = self.current_scores()
        for player in self.players:
            if scores[player] == 26:
                d[player] = True
                return d
        return d

    def final_scores(self):
        scores = self.current_scores()
        shoot_successes = self.shot_the_moon()
        if all(shoot_successes.values()) is False:
            return scores
        else:
            for (player, attempt) in shoot_successes.items():
                if attempt is True:
                    scores[player] = scores[player] - 26
                if attempt is False:
                    scores[player] = scores[player] + 26
            return scores

    def serialize(self):
        return {
            'players': self.players,
            'turn': self.players[self.turn_counter].username,
            'hands': self.hands,
            'tricks': [trick.serialize() for trick in self.tricks],
            'hearts': str(self.hearts_broken)
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

    def __len__(self):
        return len(self.cards_played)

    def __eq__(self, other):
        return self.cards_played == other.cards_played

    def points(self):
        '''
        Returns the total number of points in the trick if it is complete. Assumes basic Hearts rules.
        '''
        if len(self) < 4:
            return 0
        else:
            points = 0
            for data in self.cards_played:
                if data[1].suit == 'h':
                    points += 1
                elif data[1] == Card('Q', 's'):
                    points += 13
            return points

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
            Return a serialized representation of the trick.
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
