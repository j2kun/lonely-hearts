from random import shuffle

from hearts.api.strings import INVALID_PASS
from hearts.api.strings import INVALID_PLAY
from hearts.api.strings import NOT_THREE
from hearts.api.strings import NOT_IN_HAND
from hearts.api.strings import NOT_HEARTS_BROKEN
from hearts.api.strings import NOT_FOLLOWING_SUIT
from hearts.api.strings import NOT_TWO_CLUBS
from hearts.api.strings import NOT_YOUR_TURN
from hearts.api.strings import NO_FIRST_TRICK_POINTS
from hearts.api.strings import message


class Player(object):
    def __init__(self, username):
        self.username = username

    def __eq__(self, other):
        return self.username == other.username

    def __hash__(self):
        return hash(self.username)


class Game(object):
    def __init__(self, players, points_to_win=100):
        self.max_points = points_to_win
        self.players = players[:]
        self.rounds = []
        self.round_number = 0

    def __eq__(self, other):
        return (
            self.players == other.players and
            self.max_points == other.max_points and
            self.rounds == other.rounds and
            self.round_number == other.round_number
        )

    def start(self):
        shuffle(self.players)
        self.create_round()

    def create_round(self):
        pass_direction = ['left', 'right', 'across', 'keep']
        new_round = Round(self.players, pass_direction[self.round_number % 4])
        self.rounds.append(new_round)

    @property
    def scores(self):
        # Returns a list of the form: [{Player: score}]
        # self.rounds is assumed to be not empty after a Game object is initialized.
        scores = []
        for the_round in self.rounds:
            if the_round.is_over():
                scores.append(the_round.final_scores())
            else:
                scores.append({player: 0 for player in self.players})
        return scores

    @property
    def total_scores(self):
        # Game --> {Player: int}
        totals = {player: 0 for player in self.players}
        for round_score in self.scores:
            for player, player_score in round_score.items():
                totals[player] += player_score
        return totals

    def is_over(self):
        return any(score >= self.max_points for score in self.total_scores.values())

    def upkeep(self):
        if self.rounds[-1].is_over() and not self.is_over():
            self.round_number += 1
            self.create_round()

    def rankings(self):
        '''
        Returns a dictionary {Player: int} which ranks players based on
        total scores when the Game is over.
        Follows "standard competition ranking ("1224" ranking)".
        '''
        rankings = {}
        scores = sorted(self.total_scores.items(), key=lambda x: x[1])

        previous_score = -1   # Store the previous score and rank in the calculation here.
        previous_rank = -1    # Actual scores and ranks are assumed to be greater than -1.

        for i in range(len(scores)):
            (player, score) = scores[i]
            if score > previous_score:
                rankings[player] = i + 1
                previous_rank = i + 1
            else:
                rankings[player] = previous_rank
            previous_score = score

        return rankings

    def serialize(self, for_player=None):
        '''
        Return a json-serializable representation of the Game, from which the
        object can be reconstructed using Game.deserialize.

        When for_player is specified, return only the information that the
        specified player is allowed to see, as per the rules of the game.
        This information will be sent directly to the client.

        Output:
        {
            'players': [str],
            'max_points': int,
            'rounds': A list of serialized Round objects,
            'round_number': int,
            'scores': [{str: int}]
            'final_scores': {str: int}
            'is_over': boolean
        }
        '''
        def serialize_the_score(score_dict):
            # Return a score dictionary with Player replaced by its username
            return {player.username: points for (player, points) in score_dict.items()}

        return {
            'players': [player.username for player in self.players],
            'max_points': self.max_points,
            'rounds': [the_round.serialize(for_player=for_player) for the_round in self.rounds],
            'round_number': self.round_number,
            'scores': [serialize_the_score(round_score) for round_score in self.scores],
            'total_scores': serialize_the_score(self.total_scores),
            'is_over': self.is_over()
        }

    @staticmethod
    def deserialize(serialized):
        deserialized = Game([Player(name) for name in serialized['players']], serialized['max_points'])
        deserialized.rounds = [Round.deserialize(the_round) for the_round in serialized['rounds']]
        deserialized.round_number = serialized['round_number']
        return deserialized


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
    def __init__(self, players, pass_to='left'):
        '''
        A Round object tracks the state of a given round.
        pass_to is either 'left', 'right', 'across', or 'keep'.
        '''
        self.players = players   # List of players in seated order
        self.hands = dict()      # Player -> Hand
        self.pass_to = pass_to
        self.pass_selections = {}  # A dictionary {player: [card]}
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

    def is_valid_pass_for_player(self, player, cards):
        # [Card] --> (Bool, string)
        is_valid = True
        string_of_cards = ', '.join(str(card) for card in cards)
        error_string = None

        if len(cards) != 3:
            error_string = message(INVALID_PASS, NOT_THREE).format(string_of_cards)
            is_valid = False
        elif not all(card in self.hands[player] for card in cards):
            illegal_card = [str(card) for card in cards if card not in self.hands[player]][0]
            error_string = message(INVALID_PASS, NOT_IN_HAND).format(string_of_cards, illegal_card)
            is_valid = False
        return (is_valid, error_string)

    def add_to_pass_selections(self, player, cards):
        '''
        Input: player: A Player object
               cards: A list of Card objects
        Verifies that cards is a valid list of cards to pass and appends
        it to the pass_selections attribute of Round.
        '''
        is_valid, error_message = self.is_valid_pass_for_player(player, cards)
        if is_valid:
            self.pass_selections[player] = cards
        else:
            raise ValueError(error_message)

    def pass_cards(self):
        '''
        Distribute the cards in the pass_selections of the round to the intended player.
        '''
        passing_shift = {'left': -1, 'right': 1, 'across': 2}

        for passer, cards in self.pass_selections.items():
            for card in cards:
                self.hands[passer].remove(card)
        for passer, cards in self.pass_selections.items():
            shift = passing_shift[self.pass_to]
            passer_position = self.players.index(passer)
            receiver = self.players[(passer_position + shift) % 4]

            self.hands[receiver] += self.pass_selections[passer]
            self.hands[receiver].hand_sort()

    def can_follow_suit(self, player, trick):
        hand = self.hands[player]
        return hand.has_suit(trick.suit)

    def is_valid_lead(self, player, card):
        '''
           Returns (bool, string) to validate whether the player can use the given card
           to start the trick.
        '''
        is_valid = True
        error_message = None

        if len(self.tricks) == 0 and card != Card('2', 'c'):
            is_valid = False
            error_message = message(INVALID_PLAY, NOT_TWO_CLUBS).format(str(card))
        elif (card.suit == 'h' and not self.hearts_broken and not self.hands[player].is_only_hearts()):
            is_valid = False
            error_message = message(INVALID_PLAY, NOT_HEARTS_BROKEN).format(str(card))
        return (is_valid, error_message)

    def is_valid_follow(self, player, trick, card):
        '''
            Returns (bool, string) to verify whether the player
            can use the given card to follow the trick.
        '''
        is_valid = True
        error_message = None
        if self.can_follow_suit(player, trick) and card.suit != trick.suit:
            is_valid = False
            suits = {'c': 'clubs', 'd': 'diamonds', 'h': 'hearts', 's': 'spades'}
            error_message = message(INVALID_PLAY, NOT_FOLLOWING_SUIT).format(str(card), suits[trick.suit])
        elif (len(self.tricks) == 1 and
              card.is_worth_points() and
              not self.hands[player].has_only_hearts_and_Qs()):
            is_valid = False
            error_message = message(INVALID_PLAY, NO_FIRST_TRICK_POINTS).format(str(card))
        return (is_valid, error_message)

    def is_player_turn(self, player):
        return self.players[self.turn_counter] == player

    def make_new_trick(self, player, card):
        self.tricks.append(Trick([(player, card)]))

    def add_to_last_trick(self, player, card):
        last_trick = self.tricks[-1]
        last_trick.cards_played.append((player, card))

    def lead_the_trick(self, player, card):
        is_valid, error_message = self.is_valid_lead(player, card)
        if is_valid:
            self.make_new_trick(player, card)
            self.upkeep(player, card)
        else:
            raise ValueError(error_message)

    def follow_the_trick(self, player, card):
        last_trick = self.tricks[-1]
        is_valid, error_message = self.is_valid_follow(player, last_trick, card)

        if is_valid:
            self.add_to_last_trick(player, card)
            self.upkeep(player, card)
        else:
            raise ValueError(error_message)

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
            error_message = message(INVALID_PLAY, NOT_YOUR_TURN).format(str(card))
            raise ValueError(error_message)

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
        return {player: score == 26 for (player, score) in self.current_scores().items()}

    def final_scores(self):
        if self.is_over:
            scores = self.current_scores()
            shoot_successes = self.shot_the_moon()

            if any(shoot_successes.values()):
                for (player, shoot_success) in shoot_successes.items():
                    scores[player] = 0 if shoot_success else 26
            return scores
        else:
            return None

    def is_over(self):
        return len(self.tricks) == 13 and len(self.tricks[-1]) == 4

    def serialize(self, for_player=None):
        '''
        Return a json-serializable representation of the Round, from which the
        object can be reconstructed using Round.desearialize.

        When for_player is specified, return only the information that the
        specified player is allowed to see, as per the rules of the game.
        This information will be sent directly to the client.

        Output:
        {
            'players': [str],
            'direction': str,
            'pass_selections': {str: [str, str, str]}
            'turn': int,
            'hands': [str],
            'tricks': {str: {int: str}}
            'hearts': boolean
            'current_scores': {str: int}
            'final_scores': {str: int}
            'is_over': boolean
        }
        '''
        if for_player is None:
            hands = {player.username: hand.serialize() for player, hand in self.hands.items()}
        else:
            player = for_player if isinstance(for_player, Player) else Player(for_player)
            hands = {player.username: self.hands[player].serialize()}

        def serialize_pass_selections(pass_selections, for_player=for_player):
            '''
            Converts a dictionary of the form {Player: [Card, Card, Card]}
            to {str: [str, str, str]}.  If for_player is not None, then
            only that player's selected cards are serialized.
            '''
            serialized = {}

            if for_player is None:
                for player, cards in pass_selections.items():  # Serialize all submitted cards.
                    serialized[player.username] = [card.serialize() for card in cards]
            elif for_player in pass_selections:   # Serialize only the cards that for_player chose.
                player = for_player if isinstance(for_player, Player) else Player(for_player)
                serialized[player.username] = [card.serialize() for card in pass_selections[player]]
            return serialized

        def serialize_the_score(score_dict):
            # Return a score dictionary with Player replaced by its username
            return {player.username: points for (player, points) in score_dict.items()}

        return {
            'players': [player.username for player in self.players],
            'direction': self.pass_to,
            'pass_selections': serialize_pass_selections(self.pass_selections, for_player),
            'turn': self.turn_counter,
            'hands': hands,
            'tricks': [trick.serialize() for trick in self.tricks],
            'hearts': self.hearts_broken,
            'current_scores': serialize_the_score(self.current_scores()),
            'final_scores': serialize_the_score(self.final_scores()),
            'is_over': self.is_over()
        }

    @staticmethod
    def deserialize(serialized):
        player_list = [Player(username) for username in serialized['players']]
        the_round = Round(player_list, pass_to=serialized['direction'])

        selections = {}
        for (username, cards) in serialized['pass_selections'].items():
            selections[Player(username)] = [Card.deserialize(card) for card in cards]
        the_round.pass_selections = selections

        the_round.turn_counter = serialized['turn']
        the_round.hands = {Player(username): Hand.deserialize(hand) for (username, hand) in serialized['hands'].items()}
        the_round.tricks = [Trick.deserialize(trick) for trick in serialized['tricks']]
        the_round.hearts_broken = serialized['hearts']
        return the_round

    def __eq__(self, other):
        return (
            self.players == other.players and
            self.pass_to == other.pass_to and
            self.pass_selections == other.pass_selections and
            self.turn_counter == other.turn_counter and
            self.hearts_broken == other.hearts_broken and
            self.hands.items() == other.hands.items() and
            self.tricks == other.tricks
        )


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
        Output:
            {str: {int: str}}
        '''
        return {
            player.username: dict(turn=i, card=card.serialize())
            for (i, (player, card)) in enumerate(self.cards_played)
        }

    @staticmethod
    def deserialize(trick_data):
        # trick_data is a dictionary with keys--'player name'
        # and values--dict{'turn': int, 'card': string}

        play_sequence = [None] * len(trick_data)
        for username, play in trick_data.items():
            play_sequence[play['turn']] = (Player(username), Card.deserialize(play['card']))
        return Trick(play_sequence)
