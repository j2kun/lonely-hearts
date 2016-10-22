import pytest
from hearts.hearts import Hand, Player, Trick
from hearts.hearts import card_value, if_dominates

P1 = Player('Lauren')
P2 = Player('Erin')
P3 = Player('Jeremy')
P4 = Player('Daniel')

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


def test_hand():
    hand = Hand(['Ah', '7d', '6c', '2s'])
    assert '7d' in hand

    with pytest.raises(ValueError):
        Hand(['1h'])

    with pytest.raises(ValueError):
        Hand(['Xq'])

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

