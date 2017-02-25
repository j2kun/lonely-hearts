import pytest

from hearts.hearts import Card
from hearts.hearts import Hand
from hearts.hearts import Player
from hearts.hearts import Trick

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


def test_trick_length():
    trick = Trick([(P1, Card('2', 'c'))])
    assert len(trick) == 1
    trick.cards_played.append((P2, Card('A', 'c')))
    trick.cards_played.append((P3, Card('Q', 'c')))
    assert len(trick) == 3


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
