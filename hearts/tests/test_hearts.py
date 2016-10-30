import pytest

from hearts.hearts import Card
from hearts.hearts import Hand
from hearts.hearts import Player
from hearts.hearts import Round
from hearts.hearts import Trick

P1 = Player('Lauren')
P2 = Player('Erin')
P3 = Player('Jeremy')
P4 = Player('Daniel')
PLAYER_LIST = [P1, P2, P3, P4]

CARDS = [
    '2h', '3h', '4h', '5h', '6h', '7h', '8h', '9h', 'Th', 'Jh', 'Qh', 'Kh', 'Ah',
    '2s', '3s', '4s', '5s', '6s', '7s', '8s', '9s', 'Ts', 'Js', 'Qs', 'Ks', 'As',
    '2c', '3c', '4c', '5c', '6c', '7c', '8c', '9c', 'Tc', 'Jc', 'Qc', 'Kc', 'Ac',
    '2d', '3d', '4d', '5d', '6d', '7d', '8d', '9d', 'Td', 'Jd', 'Qd', 'Kd', 'Ad',
]

""" Card class tests """


def test_card_serialize():
    card = Card('A', 'h')
    assert 'Ah' == card.serialize()
    assert card == Card.deserialize('Ah')


""" Hand Class Tests """


def test_hand():
    hand = Hand(['Ah', '7d', '6h', '2s'])
    assert '7d' in hand
    assert hand.has_suit('h') == True
    assert hand.has_suit('c') == False

    with pytest.raises(ValueError):
        Hand(['1h'])

    with pytest.raises(ValueError):
        Hand(['Xq'])


"""Trick Class Tests"""


def test_trick_winner():
    trick = Trick([
        (P1, '5h'),
        (P2, '3h'),
        (P3, 'Jh'),
        (P4, 'Qs'),
    ])
    assert trick.winner() == P3


def test_trick_leader():
    trick = Trick([
        (P3, '5h'),
        (P2, '3h'),
        (P1, 'Jh'),
        (P4, 'Qs'),
    ])
    assert trick.leader() == P3


def test_serialize():
    trick = Trick([
        (Player('Lauren'), '2h'),
        (Player('Erin'), '8s'),
        (Player('Jeremy'), '6h'),
        (Player('Daniel'), 'Qs'),
    ])

    expected_serialized = {
        'Lauren': dict(turn=0, card='2h'),
        'Erin': dict(turn=1, card='8s'),
        'Jeremy': dict(turn=2, card='6h'),
        'Daniel': dict(turn=3, card='Qs'),
    }

    assert expected_serialized == trick.serialize()

    deserialized = Trick.deserialize(trick.serialize())

    for i in range(4):
        assert trick.cards_played[i][0].username == deserialized.cards_played[i][0].username
        assert trick.cards_played[i][1] == deserialized.cards_played[i][1]


"""Round Class Tests"""


sample_round = Round(PLAYER_LIST)


def test_deal():
    # Check for duplicates and all 52 cards
    pass


def test_can_follow_suit():
    hand1 = Hand(['Td', '5c', '7c', 'Qs', 'As'])
    hand2 = Hand(['Td', '5c', '7c', 'Kh', 'As'])
    trick = Trick([
        (P1, '5h'),
        (P2, '3h'),
        (P3, 'Jh')
    ])
    sample_round.hands[P4] = hand1
    assert sample_round.can_follow_suit(P4, trick) == False

    sample_round.hands[P4] = hand2
    assert sample_round.can_follow_suit(P4, trick) == True


def test_play_card():
    pass


def test_serialize_Round():
    pass
