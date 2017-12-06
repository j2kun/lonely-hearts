function RoomUI(callbacks) {

  this.cardClickCallback = callbacks['cardClick'];

  this.passButtonClickCallback = callbacks['passButtonClick'];

  this.displayCard = function(apiCard) {
    return apiCard[1] + apiCard[0];
  }

  this.apiCard = function(displayCard) {
    return displayCard[1] + displayCard[0];
  }

  this.displayOpponent = function(position, name) {
    var className = '.opponent.' + position;
    $(className + ' .name').text(name);
  }

  this.displayOpponents = function(player, allPlayers) {
    var orderedPlayers = allPlayers.slice(allPlayers.indexOf(player), allPlayers.length)
              .concat(allPlayers.slice(0, allPlayers.indexOf(player)));
    var opponents = orderedPlayers.slice(1, orderedPlayers.length);
    var positions = ['left', 'top', 'right'];

    for (var i = 0; i < positions.length; i++) {
      this.displayOpponent(positions[i], opponents[i]);
    }
  }

  this.displayTrick = function(trick) {
    // Need to rewrite this
    if (trick) {
      var trickToRender = '';
      var orderedPositions = ['bottom', 'left', 'top', 'right'];
      for (var i = 0; i < trick.length; i++) {
        trickToRender += ('<div class="card ' + orderedPositions[i] +
               '" id="' + this.displayCard(trick[i]) + '"></div>');
      $('#trick').html(trickToRender);
      }
    }
  }

  this.displayHand = function(hand) {
    var handToRender = '';
    for (var i = 0; i < hand.length; i++) {
      handToRender += '<li class="card" id="' + this.displayCard(hand[i]) + '"></li>'
    }
    $('#hand #cards_list').html(handToRender);
    var that = this;
    $('#hand .card').click(function(event) {
      // Pass the api version of the card clicked,
      // and a reference to the div containing the card
      // the parent caller may or may not use this div
      // to call the ui's chooseOrUnchooseCard method
      that.cardClickCallback(that.apiCard(this.id), $(this));
    });
  }

  this.chooseOrUnchooseCard = function(div) {
    div.toggleClass('chosen_to_pass');
  }

  this.renderPassButton = function(enable, direction) {
    var buttonHtml = '';
    if (enable) {
      buttonHtml = ('<button id="pass_button">' +
        'Pass 3 cards ' + direction + '</button>');
      $('#status').html(buttonHtml);
      $('#pass_button').click(this.passButtonClickCallback);
    }
    else {
      console.log('disable pass button');
      $('#pass_button').hide();
    }
  }

  this.renderWaitingForPlayers = function() {
    // Do I need this? Will this be provided by the server?
  }

  this.displayMessages = function(messages) {
    messagesHtml = '<ul>';
    for (let i = 0; i < messages.length; i++) {
      messagesHtml += '<li>' + messages[i] + '</li>';
    }
    messagesHtml += '</ul>';

    $('#messages').html(messagesHtml);
  }

  this.render = function(started, state) {
    if (!started) {
      this.renderWaitingForPlayers();
    } else {
      this.displayOpponents(state.username, state.game.players);
      console.log(state.hand());
      this.displayHand(state.hand());
      this.displayTrick(state.trick());
      this.displayMessages(state.round().messages[state.username]);
    }
  }
}
