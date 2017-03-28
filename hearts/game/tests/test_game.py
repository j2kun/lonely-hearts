from hearts.game.tests.fake import new_game
from hearts.game.tests.fake import new_round

from hearts.hearts import Game
from hearts.hearts import Player


def test_start_game_and_create_round():
    game1, _ = new_game()
    assert game1.round_number == 0
    assert len(game1.rounds) == 0
    game1.start()
    assert len(game1.rounds) == 1
    assert game1.rounds[-1].pass_to == 'left'
    game1.round_number = 7
    game1.create_round()
    assert game1.rounds[-1].pass_to == 'keep'


def test_is_over():
    test_game, players = new_game(points_to_win=27)
    test_plays = [(0, '2c,3c,4c,5c'),   # players[1] shoots the moon
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
                  (1, 'Qs,2s,3s,4s'),
                  (1, '2c,3c,4c,5c')]
    round1, _ = new_round(players, test_plays)
    test_game.rounds.append(round1)
    assert test_game.is_over() is False

    test_plays = [(0, '2c,3c,4c,5c'),  # players[1] takes 13 points, players[3] takes 13 pts
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
                  (1, '2c,3c,4c,5c')]
    round2, _ = new_round(players, test_plays)
    test_game.rounds.append(round2)

    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    assert test_game.scores == [{p0: 26, p1:  0, p2: 26, p3: 26},
                                {p0:  0, p1: 13, p2:  0, p3: 13}]
    assert test_game.total_scores == {p0: 26,
                                      p1: 13,
                                      p2: 26,
                                      p3: 39}
    assert test_game.is_over() is True


def test_rankings():
    test_game, players = new_game(points_to_win=27)
    test_plays = [(0, '2c,3c,4c,5c'),   # players[1] shoots the moon
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
                  (1, 'Qs,2s,3s,4s'),
                  (1, '2c,3c,4c,5c')]
    round1, _ = new_round(players, test_plays)
    test_game.rounds.append(round1)

    test_plays = [(0, '2c,3c,4c,5c'),  # players[1] takes 13 points, players[3] takes 13 pts
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
                  (1, '2c,3c,4c,5c')]
    round2, _ = new_round(players, test_plays)
    test_game.rounds.append(round2)

    p0 = players[0]
    p1 = players[1]
    p2 = players[2]
    p3 = players[3]

    assert test_game.total_scores == {p0: 26,
                                      p1: 13,
                                      p2: 26,
                                      p3: 39}
    assert test_game.rankings() == {p0: 2,
                                    p1: 1,
                                    p2: 2,
                                    p3: 4}


def test_deserialize_game_check_player_data():
    test_players = [Player('Lauren'), Player('Erin'), Player('Jeremy'), Player('Daniel')]
    test_game, _ = new_game(test_players, points_to_win=27)
    test_game.start()
    test_game.players = test_players  # Seat players in the order: Lauren, Erin, Jeremy, Daniel

    assert test_game.players == [Player('Lauren'), Player('Erin'), Player('Jeremy'), Player('Daniel')]
    assert test_game.serialize()['players'] == [Player('Lauren'), Player('Erin'), Player('Jeremy'), Player('Daniel')]
    assert Game.deserialize(test_game.serialize()).players == [Player('Lauren'),
                                                               Player('Erin'),
                                                               Player('Jeremy'),
                                                               Player('Daniel')]


def test_deserialize_game_with_no_rounds():
    test_players = [Player('Lauren'), Player('Erin'), Player('Jeremy'), Player('Daniel')]
    game, _ = new_game(test_players, points_to_win=27)
    deserialized = Game.deserialize(game.serialize())
    assert deserialized.players == test_players
    assert deserialized.rounds == []
    assert deserialized.round_number == 0
    assert deserialized == game


def test_deserialize_game_with_rounds():
    game, _ = new_game(points_to_win=27)
    game.start()
    randomized_players = game.players

    test_plays = [(0, '2c,3c,4c,5c'),   # players[1] shoots the moon
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
                  (1, 'Qs,2s,3s,4s'),
                  (1, '2c,3c,4c,5c')]
    round1, _ = new_round(randomized_players, test_plays)
    game.rounds[0] = round1

    test_plays = [(0, '2c,3c,4c,5c'),  # players[1] takes 13 points, players[3] takes 13 pts
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
                  (1, '2c,3c,4c,5c')]
    round2, _ = new_round(randomized_players, test_plays)
    game.rounds.append(round2)
    game.round_number = 1

    deserialized = Game.deserialize(game.serialize())
    assert deserialized.players == randomized_players
    assert deserialized.rounds == game.rounds
    assert deserialized.round_number == game.round_number
    assert deserialized == game
