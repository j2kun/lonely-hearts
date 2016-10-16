import pytest
from hearts.hearts import Hand, Player, Trick


def test_hand():
    hand = Hand(['Ah', '7d', '6c', '2s'])
    assert '7d' in hand

    with pytest.raises(ValueError):
        Hand(['1h'])

    with pytest.raises(ValueError):
        Hand(['Xq'])


def test_trick_serialize():
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
    assert trick == Trick.deserialize(trick.serialize())
