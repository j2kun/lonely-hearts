import pytest

from hearts.game.hearts import Card
from hearts.game.hearts import Hand
from hearts.game.hearts import Player
from hearts.game.hearts import Round
from hearts.game.hearts import Trick
from hearts.game.hearts import CARDS

from hearts.game.tests.fake import new_round
from hearts.game.tests.fake import hand
from hearts.game.tests.fake import trick
from hearts.game.tests.fake import cards

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


def test_is_valid_pass_for_player():
    round1, players = new_round()
    round1.hands[players[0]] = hand('4c,Qc,5d,Ad,Kh,Qs')

    selection = cards('Qc,Ad,Qs')
    is_valid, error_string = round1.is_valid_pass_for_player(players[0], selection)
    assert is_valid is True
    assert error_string is None

    invalid_selection = cards('Qs,Ks,As')
    is_valid, message = round1.is_valid_pass_for_player(players[0], invalid_selection)
    assert is_valid is False
    assert message == 'You cannot pass Qs, Ks, As because Ks is not in your hand.'


def test_is_valid_pass_for_player_not_enough_cards():
    round1, players = new_round()
    round1.hands[players[0]] = hand('4c,Qc,5d,Ad')
    selection = cards('Qc,Ad')
    is_valid, message = round1.is_valid_pass_for_player(players[0], selection)
    assert is_valid is False
    assert message == 'You cannot pass Qc, Ad because you must pass three cards.'


def test_add_to_pass_selections():
    round1, players = new_round()
    round1.hands[players[0]] = hand('4c,Qc,5d,Ad,Kh,Qs')

    selected = cards('4c,Qc,5d')
    assert len(round1.pass_selections) == 0

    round1.add_to_pass_selections(players[0], selected)
    assert len(round1.pass_selections) == 1
    assert round1.pass_selections[players[0]] == selected


def test_add_to_pass_selections_not_enough_cards():
    round1, players = new_round()
    round1.hands[players[0]] = hand('4c,Qc,5d,Ad,Kh,Qs')
    selected = cards('4c,Qc')
    with pytest.raises(ValueError):
        round1.add_to_pass_selections(players[0], selected)


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


def test_is_valid_lead_with_2c():
    test_round, _ = new_round()
    P1 = test_round.next_player
    test_round.hands[P1] = hand('4h,Qs,2c')
    is_valid, message = test_round.is_valid_lead(P1, Card('2', 'c'))
    assert is_valid is True
    assert message is None

    is_valid, message = test_round.is_valid_lead(P1, Card('Q', 's'))
    assert is_valid is False
    assert message == ('You cannot play Qs because you must play the two '
                       'of clubs on the first trick.')


def test_is_valid_lead_breaking_hearts():
    test_round, _ = new_round()
    test_round.hearts_broken = False
    test_round.tricks.append(trick())    # Set the first trick
    P1 = test_round.next_player

    test_round.hands[P1] = hand('4h,Qs,2d')
    is_valid, message = test_round.is_valid_lead(P1, Card('4', 'h'))
    assert is_valid is False
    assert message == 'You cannot play 4h because hearts have not been broken yet.'

    test_round.hearts_broken = True
    assert test_round.is_valid_lead(P1, Card('4', 'h'))[0] is True

    test_round.hands[P1] = hand('4h,Qh,2h')
    is_valid, message = test_round.is_valid_lead(P1, Card('4', 'h'))
    assert is_valid is True
    assert message is None


def test_is_valid_follow():
    round1, players = new_round()
    test_player = players[0]

    test_trick = trick(players[:2], '5h,3h,Jh')
    round1.hands[test_player] = hand('Ah,7d,6h,2s')

    assert round1.is_valid_follow(test_player, test_trick, Card('A', 'h'))[0] is True

    is_valid, error_message = round1.is_valid_follow(test_player, test_trick, Card('7', 'd'))
    assert is_valid is False
    assert error_message == 'You cannot play 7d because you still have hearts in your hand.'


def test_lead_the_trick():
    round1, players = new_round()
    first_trick = trick(players, '2c,3c,4c,5c')
    round1.tricks.append(first_trick)
    P1 = round1.next_player
    last_counter = round1.turn_counter
    round1.hands[P1] = hand('7d,6h,Ah,2s')

    round1.lead_the_trick(P1, Card('2', 's'))
    assert round1.tricks[-1] == Trick([(P1, Card('2', 's'))])
    new_hand = hand('7d,6h,Ah')
    assert round1.hands[P1] == new_hand
    assert round1.turn_counter == (last_counter + 1) % 4


def test_is_valid_follow_on_first_trick():
    round1, _ = new_round()
    counter = round1.turn_counter
    first_player = round1.players[counter]
    round1.play_card(first_player, Card('2', 'c'))

    assert round1.turn_counter == (counter + 1) % 4
    next_player = round1.players[round1.turn_counter]
    round1.hands[next_player] = hand('2d,6h,Ah,Qs')
    assert round1.is_valid_follow(next_player, round1.tricks[-1], Card('2', 'd'))[0] is True


def test_is_valid_follow_on_first_trick_dropping_points():
    round1, _ = new_round()
    counter = round1.turn_counter
    first_player = round1.players[counter]
    round1.play_card(first_player, Card('2', 'c'))
    next_player = round1.players[round1.turn_counter]

    round1.hands[next_player] = hand('6h,Ah,Qs')   # forced to drop points
    assert round1.is_valid_follow(next_player, round1.tricks[-1], Card('6', 'h'))[0] is True

    round1.hands[next_player] = hand('2d,6h,Ah,Qs')
    is_valid, error_message = round1.is_valid_follow(next_player, round1.tricks[-1], Card('6', 'h'))
    assert is_valid is False
    assert error_message == ('You cannot play 6h because you cannot play hearts '
                             'or the queen of spades on the first trick.')


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


def test_current_scores_no_points():
    round1, players = new_round()
    assert round1.current_scores() == {player: 0 for player in players}

    test_plays = [(0, '2c,Ac,Kc,As'),
                  (1, 'Ad,Qd,Ah')]   # incomplete trick has no points
    round2, players = new_round(trick_plays=test_plays)
    assert round2.current_scores() == {player: 0 for player in players}


def test_current_scores_with_points():
    round1, players = new_round()
    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    trick1 = trick([p0, p1, p2, p3], '2c,Ac,Kc,As')
    round1.tricks.append(trick1)
    assert round1.current_scores() == {p0: 0, p1: 0, p2: 0, p3: 0}

    trick2 = trick([p1, p2, p3, p0], 'Kd,Qd,Ad,2h')
    round1.tricks.append(trick2)
    assert round1.current_scores() == {p0: 0, p1: 0, p2: 0, p3: 1}

    trick3 = trick([p3, p0, p1, p2], '2d,Qs,4d,3d')
    round1.tricks.append(trick3)
    assert round1.current_scores() == {p0: 0, p1: 13, p2: 0, p3: 1}

    trick4 = trick([p1, p2, p3, p0], '2h,4h,5h,3s')
    round1.tricks.append(trick4)
    assert round1.current_scores() == {p0: 0, p1: 13, p2: 0, p3: 4}


def test_shot_the_moon():
    test_plays = [(0, '2c,3c,4c,5c'),   # p1 loses tricks without points
                  (0, '2c,3c,4c,5c'),
                  (0, '2c,Ac,2h,3c'),   # p1 wins every trick it follows
                  (0, '2c,Ac,3h,3c'),
                  (0, '2c,Ac,3c,4h'),
                  (0, '2c,Ac,3c,5h'),
                  (0, '2c,Ac,3c,6h'),
                  (0, '2c,Ac,3c,7h'),
                  (0, '8h,Jh,9h,Th'),
                  (1, 'Kh,Qh,3c,3c'),   # p1 wins by leading the trick
                  (1, 'Ah,3c,3c,3c'),
                  (1, 'Qs,2s,3s,4s'),
                  (1, '2c,3c,4c,5c')]   # irrelevant trick

    round1, players = new_round(trick_plays=test_plays)
    assert round1.shot_the_moon() == {players[0]: False,
                                      players[1]: True,
                                      players[2]: False,
                                      players[3]: False}


def test_final_scores_shot_the_moon():

    test_plays = [(0, '2c,3c,4c,5c'),   # p1 loses tricks without points
                  (0, '2c,3c,4c,5c'),
                  (0, '2c,Ac,2h,3c'),   # p1 wins every trick it follows
                  (0, '2c,Ac,3h,3c'),
                  (0, '2c,Ac,3c,4h'),
                  (0, '2c,Ac,3c,5h'),
                  (0, '2c,Ac,3c,6h'),
                  (0, '2c,Ac,3c,7h'),
                  (0, '8h,Jh,9h,Th'),
                  (1, 'Kh,Qh,3c,3c'),   # p1 wins by leading the trick
                  (1, 'Ah,3c,3c,3c'),
                  (1, 'Qs,2s,3s,4s'),
                  (1, '2c,3c,4c,5c')]   # irrelevant trick

    round1, players = new_round(trick_plays=test_plays)
    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    assert round1.current_scores() == {p0: 0, p1: 26, p2: 0, p3: 0}
    assert round1.shot_the_moon() == {p0: False, p1: True, p2: False, p3: False}
    assert round1.is_over()
    assert round1.final_scores() == {p0: 26, p1: 0, p2: 26, p3: 26}


def test_final_scores_without_shooting_the_moon():
    test_plays = [(0, '2c,3c,4c,5c'),   # p1 loses tricks without points
                  (0, '2c,3c,4c,5c'),
                  (0, '2c,Ac,2h,3c'),   # p1 wins every trick it follows
                  (0, '2c,Ac,3h,3c'),
                  (0, '2c,Ac,3c,4h'),
                  (0, '2c,Ac,3c,5h'),
                  (0, '2c,Ac,3c,6h'),
                  (0, '2c,Ac,3c,7h'),
                  (0, '8h,Jh,9h,Th'),
                  (1, 'Kh,Qh,3c,3c'),   # p1 wins by leading the trick
                  (1, 'Ah,3c,3c,3c'),
                  (1, 'Qs,2s,As,4s'),   # p3 takes the queen of spades
                  (1, '2c,3c,4c,5c')]   # irrelevant trick

    round1, players = new_round(trick_plays=test_plays)
    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    assert round1.current_scores() == {p0: 0, p1: 13, p2: 0, p3: 13}
    assert round1.shot_the_moon() == {p0: False, p1: False, p2: False, p3: False}
    assert round1.is_over()
    assert round1.final_scores() == {p0: 0, p1: 13, p2: 0, p3: 13}


def test_pass_cards_left():
    round1, players = new_round(pass_to='left')
    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    round1.hands[p0] = hand('2c,Kc,3d,7h,Qs')
    round1.hands[p1] = hand('3c,4c,Jd,Kd,As')
    round1.hands[p2] = hand('4c,Ac,Th,Qh,Kh')
    round1.hands[p3] = hand('Tc,Qc,Jh,Ah,Ks')

    selections = {p0: cards('Kc,7h,Qs'),
                  p1: cards('Jd,Kd,As'),
                  p2: cards('Th,Qh,Kh'),
                  p3: cards('Tc,Qc,Ks')}
    round1.pass_cards(selections)
    assert Card('K', 'c') not in round1.hands[p0]
    assert Card('K', 'c') in round1.hands[p3]

    assert round1.hands[p0] == hand('2c,3d,Jd,Kd,As')
    assert round1.hands[p1] == hand('3c,4c,Th,Qh,Kh')
    assert round1.hands[p2] == hand('4c,Tc,Qc,Ac,Ks')
    assert round1.hands[p3] == hand('Kc,7h,Jh,Ah,Qs')


def test_pass_cards_right():
    round1, players = new_round(pass_to='right')
    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    round1.hands[p0] = hand('2c,Kc,3d,7h,Qs')
    round1.hands[p1] = hand('3c,4c,Jd,Kd,As')
    round1.hands[p2] = hand('4c,Ac,Th,Qh,Kh')
    round1.hands[p3] = hand('Tc,Qc,Jh,Ah,Ks')

    selections = {p0: cards('Kc,7h,Qs'),
                  p1: cards('Jd,Kd,As'),
                  p2: cards('Th,Qh,Kh'),
                  p3: cards('Tc,Qc,Ks')}

    round1.pass_cards(selections)
    assert Card('K', 'c') not in round1.hands[p0]
    assert Card('K', 'c') in round1.hands[p1]

    assert round1.hands[p0] == hand('2c,Tc,Qc,3d,Ks')
    assert round1.hands[p1] == hand('3c,4c,Kc,7h,Qs')
    assert round1.hands[p2] == hand('4c,Ac,Jd,Kd,As')
    assert round1.hands[p3] == hand('Th,Jh,Qh,Kh,Ah')


def test_pass_cards_across():
    round1, players = new_round(pass_to='across')
    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    round1.hands[p0] = hand('2c,Kc,3d,7h,Qs')
    round1.hands[p1] = hand('3c,4c,Jd,Kd,As')
    round1.hands[p2] = hand('4c,Ac,Th,Qh,Kh')
    round1.hands[p3] = hand('Tc,Qc,Jh,Ah,Ks')

    selections = {p0: cards('Kc,7h,Qs'),
                  p1: cards('Jd,Kd,As'),
                  p2: cards('Th,Qh,Kh'),
                  p3: cards('Tc,Qc,Ks')}

    round1.pass_cards(selections)
    assert Card('K', 'c') not in round1.hands[p0]
    assert Card('K', 'c') in round1.hands[p2]
    assert round1.hands[p0] == hand('2c,3d,Th,Qh,Kh')
    assert round1.hands[p2] == hand('4c,Kc,Ac,7h,Qs')
    assert round1.hands[p1] == hand('3c,4c,Tc,Qc,Ks')
    assert round1.hands[p3] == hand('Jd,Kd,Jh,Ah,As')


def test_is_over():
    test_plays = [(0, '2c,Ac,Kc,As'),
                  (1, 'Ad,Qd,Qc,Ks')]
    round1, players = new_round(trick_plays=test_plays)
    assert not round1.is_over()

    test_plays = [(0, '2c,3c,4c,5c'),
                  (0, '2c,3c,4c,5c'),
                  (0, '2c,Ac,2h,3c'),
                  (0, '2c,Ac,3h,3c'),
                  (0, '2c,Ac,3c,4h'),
                  (0, '2c,Ac,3c,5h'),
                  (0, '2c,Ac,3c,6h'),
                  (0, '2c,Ac,3c,7h'),
                  (0, '8h,Jh,9h,Th'),
                  (1, 'Kh,Qh,3c,3c'),
                  (1, 'Ah,3c,3c,3c'),
                  (1, 'Qs,2s,As,4s'),
                  (1, '2c,3c')]        # Last trick is incomplete.
    round2, players = new_round(trick_plays=test_plays)
    assert not round2.is_over()

    test_plays = [(0, '2c,3c,4c,5c'),
                  (0, '2c,3c,4c,5c'),
                  (0, '2c,Ac,2h,3c'),
                  (0, '2c,Ac,3h,3c'),
                  (0, '2c,Ac,3c,4h'),
                  (0, '2c,Ac,3c,5h'),
                  (0, '2c,Ac,3c,6h'),
                  (0, '2c,Ac,3c,7h'),
                  (0, '8h,Jh,9h,Th'),
                  (1, 'Kh,Qh,3c,3c'),
                  (1, 'Ah,3c,3c,3c'),
                  (1, 'Qs,2s,As,4s'),
                  (1, '2c,3c,4c,5c')]  # Last trick is complete.
    round3, players = new_round(trick_plays=test_plays)
    assert round3.is_over()


def test_full_round_no_errors():
    round1, players = new_round()
    while len(round1.tricks) < 13:
        current_player = round1.next_player
        for card in round1.hands[current_player]:
            try:
                round1.play_card(current_player, card)
                break
            except ValueError:
                pass


def test_serialize_for_player():
    test_plays = [(0, '2c,3c,4c,5c'),  # players[1] has 10 hearts
                  (0, '2c,3c,4c,5c'),
                  (0, '2c,Ac,2h,3c'),
                  (0, '2c,Ac,3h,3c'),
                  (0, '2c,Ac,3c,4h'),
                  (0, '2c,Ac,3c,5h'),
                  (0, '2c,Ac,3c,6h'),
                  (0, '2c,Ac,3c,7h'),
                  (0, '8h,Jh,9h,Th'),
                  (1, 'Kh,Qh')]        # players[3]'s turn is next

    test_round, players = new_round(trick_plays=test_plays, pass_to='across')

    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    test_hands = {p0: hand('2d,3d,4d,5d'),
                  p1: hand('2s,3s,4s'),
                  p2: hand('5s,6s,7s'),
                  p3: hand('8s,9s,Ts,Js')}

    test_round.hands = test_hands
    test_round.turn_counter = 3
    test_round.hearts_broken = True

    for player, _ in test_hands.items():
        serialized = test_round.serialize(for_player=player)
        hands = serialized['hands']
        assert len(hands) == 1
        assert player.username in hands


def test_deserialize_round():
    test_plays = [(0, '2c,3c,4c,5c'),  # players[1] has 10 hearts
                  (0, '2c,3c,4c,5c'),
                  (0, '2c,Ac,2h,3c'),
                  (0, '2c,Ac,3h,3c'),
                  (0, '2c,Ac,3c,4h'),
                  (0, '2c,Ac,3c,5h'),
                  (0, '2c,Ac,3c,6h'),
                  (0, '2c,Ac,3c,7h'),
                  (0, '8h,Jh,9h,Th'),
                  (1, 'Kh,Qh')]        # players[3]'s turn is next

    test_round, players = new_round(trick_plays=test_plays, pass_to='across')

    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    test_hands = {p0: hand('2d,3d,4d,5d'),
                  p1: hand('2s,3s,4s'),
                  p2: hand('5s,6s,7s'),
                  p3: hand('8s,9s,Ts,Js')}

    selections = {p0: hand('As,Ks,Qs'),
                  p1: hand('Ac,Kc,Qc'),
                  p2: hand('Ad,Kd,Qd')}  # p3 has not picked 3 cards yet

    test_round.hands = test_hands
    test_round.pass_selections = selections
    test_round.turn_counter = 3
    test_round.hearts_broken = True
    assert test_round == Round.deserialize(test_round.serialize())
    assert test_round.serialize() == Round.deserialize(test_round.serialize()).serialize()
