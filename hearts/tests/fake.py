from hearts.hearts import Card
from hearts.hearts import Hand
from hearts.hearts import Player
from hearts.hearts import Round
from hearts.hearts import Trick


def players(names='Lauren,Erin,Jeremy,Daniel'):
    return [Player(x) for x in players.split(',')]


def new_round(players):
    return Round(players=players)


def hand(cards='Ah,7d,6h,2s'):
    return Hand([Card.deserialize(c) for c in cards.split(',')])


def trick(players, cards='5h,3h,Jh,Qs'):
    return Trick([(p, Card.deserialize(c)) for (p, c) in zip(players, cards)])
