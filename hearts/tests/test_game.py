import pytest

from hearts.hearts import Game
from hearts.hearts import Round

from hearts.tests.fake import new_game


def test_create_round():
    game1, players = new_game()
    assert game1.round_number == 1
    game1.create_round()
    assert len(game1.rounds) == 1
    assert game1.rounds[-1].pass_to == 'left'
    game1.round_number = 8
    game1.create_round()
    assert game1.rounds[-1].pass_to == 'keep'


def test_is_over():
    pass


