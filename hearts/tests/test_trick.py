from hearts.hearts import Card
from hearts.hearts import Player
from hearts.hearts import Trick
from hearts.tests.fake import new_round
from hearts.tests.fake import trick

P1 = Player('Lauren')
P2 = Player('Erin')
P3 = Player('Jeremy')
P4 = Player('Daniel')


def test_trick_length():
    trick = Trick([(P1, Card('2', 'c'))])
    assert len(trick) == 1
    trick.cards_played.append((P2, Card('A', 'c')))
    trick.cards_played.append((P3, Card('Q', 'c')))
    assert len(trick) == 3


def test_trick_points():
    round1, players = new_round()
    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]
    trick1 = trick([p0, p1, p2, p3], '2c,3s,4d,5c')
    assert trick1.points() == 0

    trick2 = trick([p1, p2, p3, p0], '3c,Qs,4c,Ah')
    assert trick2.points() == 14
    assert trick2.winner() == p3

    trick3 = trick([p2, p3, p0], '2h,3h,4s')
    assert trick3.points() == 0


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
