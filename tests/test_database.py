

def test_insert(db):
    db.my_collection.drop()
    result = db.my_collection.insert_many([{'wat': 'whoa'}, {'wat': 'dude'}])
    assert len(result.inserted_ids) == 2
    cursor = db.my_collection.find({"wat": "dude"})
    assert cursor.count() == 1
