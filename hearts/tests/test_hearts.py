import pytest
from hearts import hearts


def test_hand():
    hand = hearts.Hand(['Ah', '7d', '6c', '2s'])
    assert '7d' in hand

    with pytest.raises(ValueError):
        hearts.Hand(['1h'])

    with pytest.raises(ValueError):
        hearts.Hand(['Xq'])
