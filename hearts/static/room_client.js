function RoomClient(socket_client, room_state) {

  this.refresh = function() {
    this.ui.render(this.state.game != null, this.state);
  }

  this.callbacks = function() {
    return {
      'card_click': this.cardClick.bind(this)
    };
  }

  this.cardClick = function(card, div) {
    console.log('clicked ' + card);
    if (this.state.mode === 'passing') {
      if (this.state.chooseOrUnchooseCard(card)) {
        this.ui.chooseOrUnchooseCard(div);
      }

      if (this.state.chosenCards.length == 3) {
        this.ui.renderPassButton(true, this.state.round.direction);
      } else {
        this.ui.renderPassButton(false);
      }
    } else if (this.state.mode === 'play') {
      var success = true; // playCard(card);  // call the API
      if (success) {
        var index = this.state.hand.indexOf(card);
        this.state.hand.splice(index, 1);
        this.state.trick.push(card);
        this.ui.render();
      }
    }
  }

  this.socket_client = socket_client;
  this.state = room_state;
  this.ui = new RoomUI(this.callbacks());

  var that = this;
  this.refresh();
  this.socket_client.setup_game_update_handler(
    function(data) {
      that.state.gameUpdate(data);
      that.refresh();
    });
}
