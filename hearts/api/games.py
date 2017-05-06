'''
Helper functions for interacting with games.
A game document has the following fields
    {
      '_id': ObjectId,
      'room_id': ObjectId,
      'data': serialized Game object
    }
'''

from bson.objectid import ObjectId

from hearts import mongo
from hearts.game.hearts import Game
from hearts.game.hearts import Player
from hearts.api.rooms import get_room


class GameDoesNotExist(Exception):
    '''
    Exception thrown when trying to get a game that does not exist.
    '''
    pass


class GameCreateFailed(Exception):
    '''
    Exception thrown when database fails to create a game document.
    '''
    pass


class NotEnoughPlayers(Exception):
    '''
    Exception thrown during game creation when not enough players
    present in the room.
    '''
    pass


def get_game(game_id):
    '''
    Get a game from the database.
    Input:
        game_id: string or ObjectId
    Output:
        {
          '_id': ObjectId,
          'data': serialized Game object
        }
    '''
    try:
        if not isinstance(game_id, ObjectId):
            game_id = ObjectId(game_id)
    except TypeError:
        raise TypeError("game_id must be a string or ObjectId, was {}".format(type(game_id).__name__))

    result = mongo.db.games.find_one({'_id': game_id})
    if not result:
        raise GameDoesNotExist()

    return result


def create_game(room_id, max_points=100):
    '''
    Create a new game based on the users in the given room. Creates
    a 'game_id' field in the room document.

    Input:
        room_id: string or ObjectId
    Output:
        A tuple (gameDocument, ObjectId)
    '''
    usernames = get_room(room_id)['users']
    if len(usernames) == 4:
        new_game = Game([Player(name) for name in usernames], points_to_win=max_points)
        new_game.start()
        game_data = new_game.serialize()

        game_id = mongo.db.games.insert({
            'room_id': ObjectId(room_id),
            'users': usernames,
            'data': game_data
        })
        if not game_id:
            raise GameCreateFailed()

        mongo.db.rooms.update_one(
            {'_id': ObjectId(room_id)},
            {'$set': {'game_id': game_id}}
        )

        game = mongo.db.games.find_one({'_id': game_id})
        return game, game_id
    else:
        raise NotEnoughPlayers()
