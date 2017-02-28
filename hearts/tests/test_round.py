import pytest

from hearts.hearts import Card
from hearts.hearts import Hand
from hearts.hearts import Player
from hearts.hearts import Round
from hearts.hearts import Trick
from hearts.hearts import CARDS

from hearts.tests.fake import new_round
from hearts.tests.fake import hand
from hearts.tests.fake import trick

P1 = Player('Lauren')
P2 = Player('Erin')
P3 = Player('Jeremy')
P4 = Player('Daniel')
PLAYER_LIST = [P1, P2, P3, P4]
sample_round = Round(PLAYER_LIST)


def test_deal():
    cards = Hand(CARDS)
    dealt = Hand([])
    for player in PLAYER_LIST:
        dealt += sample_round.hands[player]
    cards.hand_sort()
    dealt.hand_sort()
    assert len(dealt.serialize()) == 52
    # Check list equality instead of Hand equality to check for duplicates and all 52 cards
    assert cards.serialize() == dealt.serialize()


def test_can_follow_suit():
    hand1 = Hand.deserialize(['Td', '5c', '7c', 'Qs', 'As'])
    hand2 = Hand.deserialize(['Td', '5c', '7c', 'Kh', 'As'])
    trick = Trick([
        (P1, Card('5', 'h')),
        (P2, Card('3', 'h')),
        (P3, Card('J', 'h'))
    ])
    sample_round.hands[P4] = hand1
    assert not sample_round.can_follow_suit(P4, trick)

    sample_round.hands[P4] = hand2
    assert sample_round.can_follow_suit(P4, trick)


def test_is_valid_lead():
    sample_round.hearts_broken = False
    sample_round.tricks.append(0)

    sample_round.hands[P1] = Hand.deserialize(['4h', 'Qs', '2d'])
    assert not sample_round.is_valid_lead(P1, Card('4', 'h'))

    sample_round.hands[P1] = Hand.deserialize(['4h', 'Qh', '2h'])
    assert sample_round.is_valid_lead(P1, Card('4', 'h'))


def test_is_valid_follow():
    fake_trick = Trick([
        (P1, Card('5', 'h')),
        (P2, Card('3', 'h')),
        (P3, Card('J', 'h'))
    ])
    fake_hand = Hand.deserialize(['Ah', '7d', '6h', '2s'])
    assert sample_round.is_valid_follow(P4, fake_trick, fake_hand[0])
    assert not sample_round.is_valid_follow(P4, fake_trick, fake_hand[1])


def test_lead_the_trick():
    round1 = Round(PLAYER_LIST)
    hand = Hand.deserialize(['7d', '6h', 'Ah', '2s'])
    trick = Trick([(P1, Card('2', 'c'))])
    round1.hands[P4] = hand
    round1.turn_counter = 3
    round1.tricks.append(trick)

    round1.lead_the_trick(P4, Card('2', 's'))
    assert round1.tricks[-1] == Trick([(P4, Card('2', 's'))])
    new_hand = Hand.deserialize(['7d', '6h', 'Ah'])
    assert round1.hands[P4] == new_hand
    assert round1.turn_counter == 0


def test_invalid_follow_on_first_trick():
    round1 = Round(PLAYER_LIST)
    hand = Hand.deserialize(['2d', '6h', 'Ah', 'Qs'])
    counter = round1.turn_counter
    first_player = round1.players[counter]
    round1.play_card(first_player, Card('2', 'c'))

    assert round1.turn_counter == (counter + 1) % 4
    next_player = round1.players[round1.turn_counter]
    round1.hands[next_player] = hand
    assert round1.is_valid_follow(next_player, round1.tricks[-1], Card('2', 'd'))
    assert not round1.is_valid_follow(next_player, round1.tricks[-1], Card('6', 'h'))


def test_breaking_hearts_on_first_trick():
    round1, _ = new_round()
    round1.play_card(round1.next_player, Card('2', 'c'))

    next_player = round1.next_player
    round1.hands[next_player] = hand(cards='5h,Jd')
    with pytest.raises(ValueError):
        round1.play_card(next_player, Card('5', 'h'))
    round1.play_card(next_player, Card('J', 'd'))
    assert round1.hearts_broken is False

    next_player = round1.next_player
    round1.hands[next_player] = hand(cards='9h,Qs')
    round1.play_card(next_player, Card('9', 'h'))
    assert round1.hearts_broken is True


def test_breaking_hearts_on_2nd_trick_by_leading():
    round1, players = new_round()
    first_trick = trick(players, cards='6c,3c,4c,5c')
    round1.tricks.append(first_trick)
    next_player = round1.next_player

    round1.hands[next_player] = hand(cards='2h,3h,4h')
    assert round1.hearts_broken is False
    round1.play_card(next_player, Card('2', 'h'))
    assert round1.hearts_broken is True


def test_breaking_hearts_on_2nd_trick_by_following():
    round1, players = new_round()
    first_trick = trick(players, cards='6c,3c,4c,5c')
    round1.tricks.append(first_trick)
    next_player = round1.next_player

    round1.hands[next_player] = hand(cards='As,Ad')
    round1.play_card(next_player, Card('A', 's'))
    next_player = round1.next_player
    round1.hands[next_player] = hand(cards='Ad,Ah')
    assert round1.hearts_broken is False
    round1.play_card(next_player, Card('A', 'h'))
    assert round1.hearts_broken is True


def test_follow_the_trick_with_wrong_suit():
    round1, players = new_round()
    first_trick = trick(players[1:3], cards='2c,3c')
    round1.turn_counter = 3
    round1.tricks.append(first_trick)

    with pytest.raises(ValueError):
        next_hand = hand(cards='4c,9d,4h')
        next_player = round1.next_player
        round1.hands[next_player] = next_hand
        round1.follow_the_trick(next_player, Card('9', 'd'))


def test_follow_the_trick_with_first_trick_dumping():
    round1, players = new_round()
    first_trick = trick(players[1:3], cards='2c,3c')
    round1.turn_counter = 3
    round1.tricks.append(first_trick)
    next_player = round1.next_player
    round1.hands[next_player] = hand('Ad,Th,Jh,Qs')

    with pytest.raises(ValueError):
        round1.follow_the_trick(next_player, Card('Q', 's'))
    with pytest.raises(ValueError):
        round1.follow_the_trick(next_player, Card('T', 'h'))


def test_follow_the_trick_upkeep_on_an_incomplete_trick():
    '''After a played card, test for the last trick being updated,
    the turn counter moved, and the last player's hand updated'''

    round1, players = new_round()
    first_trick = trick(players[1:3], cards='2c,3c')
    round1.turn_counter = 3
    round1.tricks.append(first_trick)
    next_player = round1.next_player
    round1.hands[next_player] = hand('Ad,Th,Jh,Qs')
    round1.follow_the_trick(next_player, Card('A', 'd'))

    updated_trick = trick(players[1:], cards='2c,3c,Ad')
    assert round1.tricks[-1] == updated_trick
    assert round1.turn_counter == 0
    previous_player = round1.players[round1.turn_counter-1]
    assert previous_player == next_player
    assert round1.hands[previous_player] == hand('Th,Jh,Qs')


def test_follow_the_trick_upkeep_on_a_completed_trick():
    '''
    After a played card, test for the last trick being updated,
    the turn counter moved to the trick's winner,
    and the last player's hand updated.
    '''
    round1, players = new_round()
    first_trick = trick(players[1:3], cards='2c,3c')
    round1.turn_counter = 3
    round1.tricks.append(first_trick)
    next_player = round1.next_player
    round1.hands[next_player] = hand('Ad,Th,Jh,Qs')
    round1.follow_the_trick(next_player, Card('A', 'd'))
    next_player = round1.next_player
    round1.hands[next_player] = hand(cards='2d,3d,4h')
    round1.follow_the_trick(next_player, Card('2', 'd'))

    players_in_order = players[1:] + players[:1]
    updated_trick = trick(players_in_order, cards='2c,3c,Ad,2d')
    assert round1.tricks[-1] == updated_trick
    assert round1.turn_counter == 2     # position of trick winner
    assert round1.hands[round1.players[0]] == hand(cards='3d,4h')


def test_play_card_out_of_turn():
    round1, players = new_round()
    wrong_player = players[(round1.turn_counter + 1) % 4]
    with pytest.raises(ValueError):
        round1.play_card(wrong_player, Card('K', 'c'))

    first_trick = trick(players[:4], cards='2c,3c,Ac')
    round1.turn_counter = 3
    round1.tricks.append(first_trick)
    next_player = round1.next_player

    wrong_player = players[(round1.turn_counter + 1) % 4]
    with pytest.raises(ValueError):
        round1.play_card(wrong_player, Card('K', 'c'))

    round1.hands[next_player] = hand('Kc,Th')
    round1.play_card(next_player, Card('K', 'c'))
    first_trick = trick(players[:], cards='2c,3c,Ac,Kc')
    assert round1.tricks[-1] == first_trick

    wrong_player = round1.players[0]
    with pytest.raises(ValueError):
        round1.play_card(wrong_player, Card('2', 'd'))

    next_player = round1.next_player
    round1.hands[next_player] = hand('2d,2h')
    round1.play_card(next_player, Card('2', 'd'))
    next_trick = trick([next_player], '2d')
    assert round1.tricks[-1] == next_trick

'''
def test_full_round_no_errors():
    r = Round()
    # set hands

    # play a full game

    P1.play_card(Card('A', 'h'))
    P2.play_card(Card('A', 'h'))


def test_play_first_trick():
    pass


def test_play_trick_sequence():
    pass


def test_serialize_Round():
    pass
'''
