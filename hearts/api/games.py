'''
Helper functions for interacting with games.
A game document has the following fields
    {
      '_id': ObjectId,
      'room_id': ObjectId,
      'users': [{'username': str, 'socket_id': str}],
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


def get_game(game_id, deserialize=True):
    '''
    Get a game from the database.
    Input:
        game_id: string or ObjectId
    Output:
        A deserialized Game object if deserilize=True.
        Otherwise, a Game object from the database.
    '''
    try:
        if not isinstance(game_id, ObjectId):
            game_id = ObjectId(game_id)
    except TypeError:
        raise TypeError("game_id must be a string or ObjectId, was {}".format(type(game_id).__name__))

    result = mongo.db.games.find_one({'_id': game_id})
    if not result:
        raise GameDoesNotExist()

    if not deserialize:
        return result
    else:
        return Game.deserialize(result['data'])


def create_game(room_id, max_points=100, deserialize=True):
    '''
    Create a new game based on the users in the given room. Creates
    a 'game_id' field in the room document.

    Input:
        room_id: string or ObjectId
    Output:
        A tuple (Game, ObjectId)
    '''
    room = get_room(room_id)
    users = room['users']
    if len(users) == 4:
        new_game = Game([Player(d['username']) for d in users], points_to_win=max_points)
        new_game.start()
        game_data = new_game.serialize()

        game_id = mongo.db.games.insert({
            'room_id': ObjectId(room_id),
            'users': users,
            'data': game_data
        })
        if not game_id:
            raise GameCreateFailed()

        # Record the id for the current game being played in the room.
        mongo.db.rooms.update_one(
            {'_id': ObjectId(room_id)},
            {'$set': {'game_id': game_id}}
        )

        if deserialize:
            return new_game, game_id
        else:
            game = get_game(game_id, deserialize=False)
            return game, game_id
    else:
        raise NotEnoughPlayers()


def save_game(game, game_id):
    '''
    Serializes a game and updates it in the database.

    Input:
        game: A deserialized Game object
        game_id: ObjectId or string
    '''
    try:
        if not isinstance(game_id, ObjectId):
            game_id = ObjectId(game_id)
    except TypeError:
        raise TypeError("game_id must be a string or ObjectId, was {}".format(type(game_id).__name__))

    mongo.db.games.update_one(
        {'_id': game_id},
        {'$set': {'data': game.serialize()}}
    )
