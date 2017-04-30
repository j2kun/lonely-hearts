'''
Helper functions for interacting with rooms.

A room object has the following fields

    {
      '_id': ObjectId,
      'users': iterable of strings,
    }
'''

from bson.objectid import ObjectId

from hearts import mongo


class RoomDoesNotExist(Exception):
    '''
    Exception thrown when trying to get a room that does not exist
    '''
    pass


class RoomCreateFailed(Exception):
    '''
    Exception thrown when room creation fails
    '''
    pass


def get_room(room_id):
    '''
    Get a room from the database

    Input:
        room_id: string or ObjectId

    Output:
        {
          '_id': ObjectId,
          'users': iterable of strings,
        }
    '''
    try:
        if not isinstance(room_id, ObjectId):
            room_id = ObjectId(room_id)
    except TypeError:
        raise TypeError("room_id must be a string or ObjectId, was {}".format(type(room_id).__name__))

    result = mongo.db.rooms.find_one({'_id': room_id})
    if not result:
        raise RoomDoesNotExist()

    return result


def create_room(users=tuple()):
    '''
    Create a new room with the given users

    Input:
        users: iterable of strings

    Output:
        {
          '_id': ObjectId,
          'users': iterable of strings,
        }
    '''
    room_id = mongo.db.rooms.insert({'users': users})
    if room_id:
        return get_room(room_id)
    else:
        raise RoomCreateFailed()
