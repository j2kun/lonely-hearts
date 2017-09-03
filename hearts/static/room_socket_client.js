function RoomSocketClient(api_url) {
  this.api_url = api_url;
  this.socket = io(this.api_url);

  this.join_room = function(room_id, username) {
    console.log("Joining room " + room_id + " as " + username);
    var returned_message = this.socket.emit('join', {
      room: room_id,
      username: username,
    });
    return returned_message;
  };

  this.pass_cards = function(cards) {
    var data = {
      cards: cards
    };
    var result = this.socket.emit('pass_cards', data);
    return result.status;
  };

  this.setup_game_update_handler = function(gameUpdateFn) {
    this.socket.on('game_update', function(data) {
      console.log('received game update: ');
      console.log(JSON.stringify(data, null, 2));
      gameUpdateFn(data);
    });
  };
}
