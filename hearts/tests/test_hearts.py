import pytest

from hearts.hearts import Card
from hearts.hearts import Hand
from hearts.hearts import Player
from hearts.hearts import Round
from hearts.hearts import Trick
from hearts.hearts import CARDS

P1 = Player('Lauren')
P2 = Player('Erin')
P3 = Player('Jeremy')
P4 = Player('Daniel')
PLAYER_LIST = [P1, P2, P3, P4]

""" Card class tests """


def test_card_serialize():
    card = Card('A', 'h')
    assert 'Ah' == card.serialize()
    assert card == Card.deserialize('Ah')


def test_card_validate():
    with pytest.raises(ValueError):
        Card.deserialize('Ch')
    with pytest.raises(ValueError):
        Card.deserialize('Q4')
    with pytest.raises(ValueError):
        Card.deserialize('2t')


""" Hand Class Tests """


def test_hand():
    hand = Hand([
        Card('A', 'h'),
        Card('7', 'd'),
        Card('6', 'h'),
        Card('2', 's')
    ])
    assert Card('7', 'd') in hand
    assert hand.has_suit('h')
    assert not hand.has_suit('c')
    with pytest.raises(ValueError):
        hand = Hand([Card('d', '6')])
    assert not hand.is_only_hearts()
    hand = Hand([Card('A', 'h'), Card('7', 'h'), Card('2', 'h')])
    assert hand.is_only_hearts()


def test_hand_sort():
    test = Hand.deserialize(['2d', 'Ts', '2c', 'Kh', 'Jc', '6s', 'Ac'])
    test.hand_sort()

    expected = Hand.deserialize(['2c', 'Jc', 'Ac', '2d', 'Kh', '6s', 'Ts'])
    assert test == expected


def test_serialize_hand():
    hand = Hand([Card('2', 'c'), Card('3', 'h'), Card('4', 's'), Card('Q', 'h')])
    assert Hand.deserialize(hand.serialize()) == hand


"""Trick Class Tests"""


def test_trick_winner():
    trick = Trick([
        (P1, Card('5', 'h')),
        (P2, Card('3', 'h')),
        (P3, Card('J', 'h')),
        (P4, Card('Q', 's')),
    ])
    assert trick.winner() == P3


def test_trick_leader():
    trick = Trick([
        (P3, Card('5', 'h')),
        (P2, Card('3', 'h')),
        (P1, Card('J', 'h')),
        (P4, Card('Q', 's')),
    ])
    assert trick.leader() == P3


def test_serialize():
    trick = Trick([
        (Player('Lauren'), Card('2', 'h')),
        (Player('Erin'), Card('8', 's')),
        (Player('Jeremy'), Card('6', 'h')),
        (Player('Daniel'), Card('Q', 's'))
    ])

    expected_serialized = {
        'Lauren': dict(turn=0, card='2h'),
        'Erin': dict(turn=1, card='8s'),
        'Jeremy': dict(turn=2, card='6h'),
        'Daniel': dict(turn=3, card='Qs')
    }
    assert expected_serialized == trick.serialize()

    deserialized = Trick.deserialize(trick.serialize())
    assert deserialized == trick


"""Round Class Tests"""


sample_round = Round(PLAYER_LIST)


def test_deal():
    cards = Hand(CARDS)
    dealt = Hand([])
    for player in PLAYER_LIST:
        dealt += sample_round.hands[player]
    cards.hand_sort()
    dealt.hand_sort()
    assert len(dealt.serialize()) == 52
    # Check list equality instead of Hand equality to check for duplicates and all 52 cards
    assert cards.serialize() == dealt.serialize()


def test_can_follow_suit():
    hand1 = Hand.deserialize(['Td', '5c', '7c', 'Qs', 'As'])
    hand2 = Hand.deserialize(['Td', '5c', '7c', 'Kh', 'As'])
    trick = Trick([
        (P1, Card('5', 'h')),
        (P2, Card('3', 'h')),
        (P3, Card('J', 'h'))
    ])
    sample_round.hands[P4] = hand1
    assert not sample_round.can_follow_suit(P4, trick)

    sample_round.hands[P4] = hand2
    assert sample_round.can_follow_suit(P4, trick)


def test_is_valid_lead():
    sample_round.hearts_broken = False
    sample_round.tricks.append(0)

    sample_round.hands[P1] = Hand.deserialize(['4h', 'Qs', '2d'])
    assert not sample_round.is_valid_lead(P1, Card('4', 'h'))

    sample_round.hands[P1] = Hand.deserialize(['4h', 'Qh', '2h'])
    assert sample_round.is_valid_lead(P1, Card('4', 'h'))


def test_is_valid_follow():
    fake_trick = Trick([
        (P1, Card('5', 'h')),
        (P2, Card('3', 'h')),
        (P3, Card('J', 'h'))
    ])
    fake_hand = Hand.deserialize(['Ah', '7d', '6h', '2s'])
    assert sample_round.is_valid_follow(P4, fake_trick, fake_hand[0])
    assert not sample_round.is_valid_follow(P4, fake_trick, fake_hand[1])


def test_lead_the_trick():
    round1 = Round(PLAYER_LIST)
    hand = Hand.deserialize(['7d', '6h', 'Ah', '2s'])
    trick = Trick([(P1, Card('2', 'c'))])
    round1.hands[P4] = hand
    round1.turn_counter = 3
    round1.tricks.append(trick)

    round1.lead_the_trick(P4, Card('2', 's'))
    assert round1.tricks[-1] == Trick([(P4, Card('2', 's'))])
    new_hand = Hand.deserialize(['7d', '6h', 'Ah'])
    assert round1.hands[P4] == new_hand
    assert round1.turn_counter == 0
    assert round1.hearts_broken is False


def test_invalid_follow_on_first_trick():
    round1 = Round(PLAYER_LIST)
    hand = Hand.deserialize(['2d', '6h', 'Ah', 'Qs'])
    counter = round1.turn_counter
    first_player = round1.players[counter]
    round1.play_card(first_player, Card('2', 'c'))

    assert round1.turn_counter == (counter + 1) % 4
    next_player = round1.players[round1.turn_counter]
    round1.hands[next_player] = hand
    assert round1.is_valid_follow(next_player, round1.tricks[-1], Card('2', 'd'))
    assert not round1.is_valid_follow(next_player, round1.tricks[-1], Card('6', 'h'))


"""
def test_follow_the_trick():
    '''
    This test checks for all possible errors when following a trick, including
    playing out of turn, playing invalid cards, and dumping on the first trick.
    '''
    test_round = Round(PLAYER_LIST)
    test_hand = Hand([Card('Q', 's'), Card('3', 'h'), Card('T', 'c')])
    fake_trick = Trick([
        (P2, Card('2', 'c')),
        (P3, Card('K', 'c'))
    ])
    test_round.turn_counter = 2
    test_round.tricks.append(fake_trick)  # Create the first trick.

    '''Catch a player out of turn'''
    with pytest.raises(TurnError):
        test_round.follow_the_trick(P1, Card('T', 'c'))

    '''Catch a player playing invalid card'''
    test_round.turn_counter = 3
    with pytest.raises(CardError):
        test_round.hands[P4] = test_hand
        test_round.follow_the_trick(P4, Card('3', 'h'))

    '''Catch early dumping on the first trick'''
    assert len(test_round.tricks) == 1
    test_round.hands[P4] = Hand([Card('Q', 's'), Card('3', 'h'), Card('7', 'd')])

    with pytest.raises(EarlyDumpError):
        test_round.follow_the_trick(P4, Card('Q', 's'))

    with pytest.raises(EarlyDumpError):
        test_round.follow_the_trick(P4, Card('3', 'h'))

    # FIXME Add a test: when player holds all hearts on first round


def test_full_round_no_errors():
    r = Round()
    # set hands

    # play a full game

    P1.play_card(Card('A', 'h'))
    P2.play_card(Card('A', 'h'))


def test_play_first_trick():
    pass


def test_play_trick_sequence():
    pass


def test_serialize_Round():
    pass
"""
