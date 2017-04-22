from bson.objectid import ObjectId

from hearts import mongo


class RoomDoesNotExist(Exception):
    pass


def get_room(room_id):
    try:
        if not isinstance(room_id, ObjectId):
            room_id = ObjectId(room_id)
    except TypeError:
        raise TypeError("room_id must be a string or ObjectId, was {}".format(type(room_id).__name__))

    result = mongo.db.rooms.find_one({'_id': room_id})
    if not result:
        raise RoomDoesNotExist()

    return result
