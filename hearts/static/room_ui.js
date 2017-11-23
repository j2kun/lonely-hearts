function RoomUI(callbacks) {

  this.cardClickCallback = callbacks['card_click'];

  this.displayCard = function(apiCard) {
    return apiCard[1] + apiCard[0];
  }

  this.apiCard = function(displayCard) {
    return displayCard[1] + displayCard[0];
  }

  this.displayOpponent = function(position, name) {
    var class_name = '.opponent.' + position;
    $(class_name + ' .name').text(name);
  }

  this.displayOpponents = function(player, all_players) {
    var ordered_players = all_players.slice(all_players.indexOf(player), all_players.length)
              .concat(all_players.slice(0, all_players.indexOf(player)));
    var opponents = ordered_players.slice(1, ordered_players.length);
    var positions = ['left', 'top', 'right'];

    for (var i = 0; i < positions.length; i++) {
      this.displayOpponent(positions[i], opponents[i]);
    }
  }

  this.displayTrick = function(trick) {
    // Need to rewrite this
    var trickToRender = '';
    var orderedPositions = ['bottom', 'left', 'top', 'right'];
    for (var i = 0; i < trick.length; i++) {
      trickToRender += ('<div class="card ' + orderedPositions[i] +
               '" id="' + this.displayCard(trick[i]) + '"></div>');
    }
    $('#trick').html(trickToRender);
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
    }
    $('#status').html(buttonHtml);
  }

  this.renderWaitingForPlayers = function() {
    // Do I need this? Will this be provided by the server?
  }

  this.displayMessages = function(messages) {
    messages_html = '<ul>';
    for (let i = 0; i < messages.length; i++) {
      messages_html += '<li>' + messages[i] + '</li>';
    }
    messages_html += '</ul>';

    $('#messages').html(messages_html);
  }

  this.render = function(started, state) {
    if (!started) {
      this.renderWaitingForPlayers();
    } else {
      this.displayOpponents(state.username, state.game.players);
      this.displayHand(state.hand);
      this.displayTrick(state.trick);
      this.displayMessages(state.messages[state.username]);
    }
  }
}