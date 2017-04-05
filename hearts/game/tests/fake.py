from hearts.game.hearts import Card
from hearts.game.hearts import Hand
from hearts.game.hearts import Player
from hearts.game.hearts import Round
from hearts.game.hearts import Game
from hearts.game.hearts import Trick


def players(names='Lauren,Erin,Jeremy,Daniel'):
    return [Player(x) for x in names.split(',')]


def new_round(players_list=None, trick_plays=None, pass_to='left'):
    # trick_plays is in the form: [(leader_position, trick_string)]
    the_players = players_list or players()
    test_round = Round(the_players, pass_to)

    if trick_plays:
        for leader_position, trick_string in trick_plays:
            ordered_players = the_players[leader_position:] + the_players[:leader_position]
            test_round.tricks.append(trick(ordered_players, trick_string))

    return test_round, the_players


def new_game(players_list=None, points_to_win=100):
    the_players = players_list or players()
    my_game = Game(the_players, points_to_win)
    return my_game, the_players


def cards(cards='Ah,7d,6h,2s'):
    return [Card.deserialize(c) for c in cards.split(',')]


def hand(cards='Ah,7d,6h,2s'):
    return Hand([Card.deserialize(c) for c in cards.split(',')])


def trick(players_list=None, cards='5h,3h,Jh,Qs'):
    the_players = players_list or players()
    return Trick([(p, Card.deserialize(c)) for (p, c) in zip(the_players, cards.split(','))])
