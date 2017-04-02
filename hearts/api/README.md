# API spec

The API consists of two parts: a REST API for all requests not within a room
(joining a room, user login, etc), and a web socket API for actions and notifications
occurring during a game.

## REST API

### `/rooms/`

Operations for creatining, joining, or viewing rooms

#### `POST /rooms/`

Data: empty

Response:

```
{
  'url': str,   # the relative url of the room, e.g., /rooms/abc123/
  'id': str,    # the id of the room, e.g., abc123
}
``` 

Side effect: A new room is created and assigned a bson id.


#### `GET /rooms/<room_id>/`

Response:

The room page, or the homepage if no such room exists.
