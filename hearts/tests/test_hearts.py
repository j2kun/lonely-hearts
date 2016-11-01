import pytest

from hearts.hearts import Card
from hearts.hearts import Hand
from hearts.hearts import Player
from hearts.hearts import Round
from hearts.hearts import Trick
from hearts.hearts import Error
from hearts.hearts import CardError
from hearts.hearts import HeartsError

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
    assert hand.has_suit('h') == True
    assert hand.has_suit('c') == False


def test_hand_sort():
    test = Hand([
        Card('2', 'd'),
        Card('T', 's'),
        Card('2','c'),
        Card('K','h'),
        Card('J', 'c'),
        Card('6','s'),
        Card('A', 'c')
    ])
    expected = Hand([
        Card('2', 'c'),
        Card('J', 'c'),
        Card('A','c'),
        Card('2','d'),
        Card('K', 'h'),
        Card('6','s'),
        Card('T', 's')
    ])
    test.hand_sort()
    assert [card.serialize() for card in test] == [card.serialize() for card in expected]


def test_serialize_hand():
    hand = Hand([Card('2', 'c'), Card('3','h'), Card('4', 's'), Card('Q', 'h')])
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
        (Player('Daniel'), Card('Q', 's')),
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
    hand1 = Hand([Card('T', 'd'), Card('5', 'c'), Card('7', 'c'), Card('Q', 's'), Card('A', 's')])
    hand2 = Hand([Card('T', 'd'), Card('5', 'c'), Card('7', 'c'), Card('K', 'h'), Card('A', 's')])
    trick = Trick([
        (P1, Card('5', 'h')),
        (P2, Card('3', 'h')),
        (P3, Card('J', 'h'))
    ])
    sample_round.hands[P4] = hand1
    assert sample_round.can_follow_suit(P4, trick) == False

    sample_round.hands[P4] = hand2
    assert sample_round.can_follow_suit(P4, trick) == True


def test_is_valid_lead():
    sample_round.hearts_broken = False
    with pytest.raises(HeartsError):
        sample_round.is_valid_lead(P1, Card('4', 'h'))


def test_is_valid_follow():
    fake_trick = Trick([
        (P1, Card('5', 'h')),
        (P2, Card('3', 'h')),
        (P3, Card('J', 'h'))
    ])
    fake_hand = Hand([
        Card('A', 'h'),
        Card('7', 'd'),
        Card('6', 'h'),
        Card('2', 's')
    ])
    with pytest.raises(CardError):
        sample_round.is_valid_follow(P4, fake_trick, fake_hand[1])

def test_lead_the_trick():
    fake_hand = Hand([
        Card('7', 'd'),
        Card('6', 'h'),
        Card('A', 'h'),
        Card('2', 's')
    ])
    sample_round.hands[P1] = fake_hand
    sample_round.lead_the_trick(P1, Card('2', 's'))
    # assert sample_round.tricks[-1] == Trick([(P1, Card('2', 's'))])

    new_hand = Hand([
        Card('7', 'd'),
        Card('6', 'h'),
        Card('A', 'h')
    ])
    assert sample_round.hands[P1] == new_hand

def test_play_card():
    pass


def test_serialize_Round():
    pass
