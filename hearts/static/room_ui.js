function RoomUI(callbacks) {

  this.cardClickCallback = callbacks['cardClick'];

  this.passButtonClickCallback = callbacks['passButtonClick'];

  this.displayCard = function(apiCard) {
    return apiCard[1] + apiCard[0];
  }

  this.apiCard = function(displayCard) {
    return displayCard[1] + displayCard[0];
  }

  this.orderedPlayerPositions = function(player, allPlayers) {
    var orderedPlayers = allPlayers.slice(allPlayers.indexOf(player), allPlayers.length)
              .concat(allPlayers.slice(0, allPlayers.indexOf(player)));
    var positions = ['bottom', 'left', 'top', 'right'];
    var playerDict = {};
    for (let i = 0; i < positions.length; i++) {
      playerDict[orderedPlayers[i]] = positions[i];
    }
    return playerDict;
  }

  this.displayOpponent = function(position, name) {
    var className = '.opponent.' + position;
    $(className + ' .name').text(name);
  }

  this.displayOpponents = function(player, allPlayers) {
    var positionDict = this.orderedPlayerPositions(player, allPlayers);

    for (let p in positionDict) {
      if (p === player) {
        continue;
      } 
      this.displayOpponent(positionDict[p], p);
    }
  }

  this.displayTrick = function(trick, player, allPlayers) {
    console.log("Rendering trick " + JSON.stringify(trick, null, 2));
    if (trick) {
      var trickToRender = '';
      var positionDict = this.orderedPlayerPositions(player, allPlayers);
      for (let p in trick) {
        trickToRender += ('<div class="card ' + positionDict[p] +
               '" id="' + this.displayCard(trick[p]["card"]) + '"></div>');
      }
      $('#trick').html(trickToRender);
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
    } else {
      console.log('disable pass button');
      this.hideActionButtons();
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

  this.hideActionButtons = function() {
      $('#pass_button').hide();
  }

  this.render = function(started, state) {
    if (!started) {
      this.renderWaitingForPlayers();
    } else {
      console.log('rendering UI');
      this.displayOpponents(state.username, state.game.players);
      this.displayHand(state.hand());
      this.displayTrick(state.trick(), state.username, state.game.players);
      this.displayMessages(state.round().messages[state.username]);
      this.hideActionButtons();
    }
  }
}
