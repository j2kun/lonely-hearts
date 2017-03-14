

def test_create_room(api, db):
    response = api.post('/rooms/')
    assert response['url']
    cursor = db.rooms.find({"id": 17})
    assert cursor.count() == 1
