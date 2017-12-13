function RoomClient(socketClient, roomState) {

  this.refresh = function() {
    this.ui.render(this.state.game != null, this.state);
  }

  this.callbacks = function() {
    return {
      'cardClick': this.cardClick.bind(this),
      'passButtonClick': this.passButtonClick.bind(this)
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
    } else if (this.state.mode() === 'play' || this.state.mode() === 'wait for play') {
      this.socketClient.playCard(card);
    }
  }

  this.passButtonClick = function() {
    console.log('Clicked the pass button!');
    let cards = this.state.chosenCards;
    this.socketClient.passCards(cards);
    console.log('called passCards socket');
  }

  this.socketClient = socketClient;
  this.state = roomState;
  this.ui = new RoomUI(this.callbacks());

  var that = this;
  this.refresh();
  this.socketClient.setupGameUpdateHandler(
    function(data) {
      that.state.gameUpdate(data);
      that.refresh();
    });
}
