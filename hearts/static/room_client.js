function RoomClient(socket_client, room_state) {

  this.refresh = function() {
    this.ui.render(this.state.game != null, this.state);
  }

  this.callbacks = function() {
    return {
      'card_click': this.cardClick.bind(this),
      'pass_button_click': this.passButtonClick.bind(this)
    };
  }

  this.cardClick = function(card, div) {
    console.log('clicked ' + card);
    if (this.state.mode() === 'passing') {
      if (this.state.chooseOrUnchooseCard(card)) {
        this.ui.chooseOrUnchooseCard(div);
      }

      if (this.state.chosenCards.length == 3) {
        this.ui.renderPassButton(true, this.state.round().direction);
      } else {
        this.ui.renderPassButton(false);
      }
    } else if (this.state.mode() === 'play') {
      this.socket_client.play_card(card);
    }
  }

  this.passButtonClick = function() {
    console.log('Clicked the pass button!');
    let cards = this.state.chosenCards;
    this.socket_client.pass_cards(cards);      // Function/method names are sometimes camelCase
                                               // and sometimes have underscores.  Confusing!

    // Need to return result of pass attempt
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
