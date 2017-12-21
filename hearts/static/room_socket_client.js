function RoomSocketClient(apiUrl) {
  this.apiUrl = apiUrl;
  this.socket = io(this.apiUrl);

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
    this.socket.emit('play_card', data, function(result){
      console.log('received play_card confirmation', result);
    });
  };

  this.setupGameUpdateHandler = function(gameUpdateFn) {
    this.socket.on('game_update', function(data) {
      console.log('received game update: ');
      console.log(JSON.stringify(data, null, 2));
      gameUpdateFn(data);
    });
  };
}
