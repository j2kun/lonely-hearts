from hearts.tests.fake import new_game
from hearts.tests.fake import new_round


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

    test_game, players = new_game(points_to_win=27)

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

    round1, players = new_round(players, test_plays)
    test_game.rounds.append(round1)
    assert test_game.is_over() is False

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
    round2, players = new_round(players, test_plays)
    test_game.rounds.append(round2)
    assert test_game.is_over() is True

    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    assert test_game.scores == {1: {p0: 26, p1:  0, p2: 26, p3: 26},
                                2: {p0:  0, p1: 13, p2:  0, p3: 13}}
    assert test_game.total_scores == {p0: 26,
                                      p1: 13,
                                      p2: 26,
                                      p3: 39}
