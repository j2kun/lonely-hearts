from hearts.hearts import Card
from hearts.hearts import Hand
from hearts.hearts import Player
from hearts.hearts import Round
from hearts.hearts import Trick


def players(names='Lauren,Erin,Jeremy,Daniel'):
    return [Player(x) for x in names.split(',')]


def new_round(players_list=None, trick_plays=None):   # trick_plays is in the form: [(leader_position, trick_string)]
    if not players_list:
        the_players = players()
    test_round = Round(the_players)

    if trick_plays:
        for leader_position, trick_string in trick_plays:
            ordered_players = the_players[leader_position:] + the_players[:leader_position]
            test_round.tricks.append(trick(ordered_players, trick_string))

    return test_round, the_players


def hand(cards='Ah,7d,6h,2s'):
    return Hand([Card.deserialize(c) for c in cards.split(',')])


def trick(players, cards='5h,3h,Jh,Qs'):
    return Trick([(p, Card.deserialize(c)) for (p, c) in zip(players, cards.split(','))])

'''
def play_full_round():
    # randomize the hand
    while round_is_not_over:
        player = get_next_player()
        for card in player.hand:
            try:
                round.play_card(card)
            except:
                pass
'''
