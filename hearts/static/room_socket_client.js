function RoomSocketClient(apiUrl) {
  this.apiUrl = apiUrl;
  this.socket = io();

  this.joinRoom = function(roomId, username) {
    console.log("Joining room " + roomId + " as " + username);
    var returnedMessage = this.socket.emit('join', {
      room: roomId,
      username: username,
    });
    return returnedMessage;
  };

  this.passCards = function(cards) {
    var data = {
      cards: cards
    };
    this.socket.emit('pass_cards', data, function(result){
      console.log('received confirmation', result);
    });
  };

  this.playCard = function(card) {
    var data = {
      card: card
    };
    var result = this.socket.emit('play_card', data);   // The emit function does not return values.  Instead,
                                                        // use a callback function that takes the server-side
                                                        // returned value as input.  See passCards above.
    return result.status;
  };

  this.setupGameUpdateHandler = function(gameUpdateFn) {
    this.socket.on('game_update', function(data) {
      console.log('received game update: ');
      console.log(JSON.stringify(data, null, 2));
      gameUpdateFn(data);
    });
  };
}
