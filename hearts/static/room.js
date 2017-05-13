
/*
 * Rendering functions
 */

function displayCard(apiCard) {
    return apiCard[1] + apiCard[0];
}

function apiCard(displayCard) {
    return displayCard[1] + displayCard[0];
}

function displayOpponent(position, name) {
    var class_name = '.opponent.' + position;
    $(class_name + ' .name').text(name);
}

function displayOpponents(player, all_players) {
    var ordered_players = all_players.slice(all_players.indexOf(player), all_players.length)
                          .concat(all_players.slice(0, all_players.indexOf(player)));
    var opponents = ordered_players.slice(1, ordered_players.length);
    var positions = ['left', 'top', 'right'];

    for (var i = 0; i < positions.length; i++) {
        displayOpponent(positions[i], opponents[i]);
    }
}

function displayTrick(trick) {
    // Need to rewrite this
    var trickToRender = '';
    var orderedPositions = ['bottom', 'left', 'top', 'right'];
    for (var i = 0; i < trick.length; i++) {
        trickToRender += ('<div class="card ' + orderedPositions[i] +
                           '" id="' + displayCard(trick[i]) + '"></div>');
    }
    $('#trick').html(trickToRender);
}


/*
 * Hearts state maintainer
 *
 * example state:
{
  "players": [
    "BillSpsP7", "Bill Xnnqk", "Bill tC3g1", "Bill sEYQH"
  ],
  "rounds": [
    {
      "hands": {
        "Bill sEYQH": [ "4c", "8c", "Ac", "4d", "6d", "2h", "3h",
                        "5h", "9h", "Jh", "3s", "7s", "Js" ]
      },
      "players": [
        "BillSpsP7", "Bill Xnnqk", "Bill tC3g1", "Bill sEYQH"
      ],
      "is_over": false,
      "current_scores": {
        "Bill tC3g1": 0, "BillSpsP7": 0, "Bill Xnnqk": 0, "Bill sEYQH": 0
      },
      "hearts": false,
      "turn": 1,
      "direction": "left",
      "tricks": [],
      "final_scores": {
        "Bill tC3g1": 0, "BillSpsP7": 0, "Bill Xnnqk": 0, "Bill sEYQH": 0
      }
    }
  ],
  "total_scores": {
    "Bill tC3g1": 0, "BillSpsP7": 0, "Bill Xnnqk": 0, "Bill sEYQH": 0
  },
  "max_points": 100,
  "is_over": false,
  "round_number": 0,
  "scores": [
    {
      "Bill tC3g1": 0, "BillSpsP7": 0, "Bill Xnnqk": 0, "Bill sEYQH": 0
    }
  ]
}
 */

function HeartsClient() {

    this.state = {
        username: '',
        chosenCards: [],
        mode: 'passing',  // 'play' or 'passing' or 'waiting'

        // game, round, hand, trick are updated by incoming
        // socket events
        game: null,
        round: null,
        hand: null,
        trick: null,
    };

    this.chooseOrUnchooseCard = function(card) {
        var foundIndex = $.inArray(card, this.state.chosenCards);
        if (foundIndex > -1) {
            this.state.chosenCards.splice(foundIndex, 1);
            return true;
        } else if (this.state.chosenCards.length < 3) {
            this.state.chosenCards.push(card);
            return true;
        } else {
            return false;
        }
    }

    this.removeCard = function(card) {
        var index = this.state.hand.indexOf(card);
        this.state.hand.splice(index, 1);
        return card;
    }

    this.cardClick = function(card, div) {
        console.log('clicked ' + card);
        if (this.state.mode === 'passing') {
            if (this.chooseOrUnchooseCard(card)) {
                div.toggleClass('chosen_to_pass');
            } // if 3, display button
        } else if (this.state.mode === 'play') {
            var success = true; // playCard(card);  // call the API
            if (success) {
                this.removeCard(card);
                this.state.trick.push(card);
                this.render();
            }
        }
    }

    this.displayHand = function(hand) {
        var handToRender = '';
        for (var i = 0; i < hand.length; i++) {
            handToRender += '<li class="card" id="' + displayCard(hand[i]) + '"></li>'
        }
        $('#hand #cards_list').html(handToRender);
        $('#hand .card').click({heartsClient: this},
            function(event) {
                var card = apiCard(this.id);
                var heartsClient = event.data.heartsClient;
                heartsClient.cardClick(card, $(this));
            }
        );
    }

    this.renderWaitingForPlayers = function() {

    }

    this.resetPassing = function() {
        this.state.chosenCards = [];
        this.render();
    }

    this.donePassing = function() {
        for (var i = 0; i < this.state.chosenCards.length; i++) {
            this.removeCard(this.state.chosenCards[i]);
        }
        this.resetPassing();
        this.state.mode = 'waiting';
    }

    this.message = function(messageStr) {
        alert(messageStr);  // this is temporary
    }

    this.render = function() {
        if (this.state.game === null) {
            // game hasn't started yet
            this.renderWaitingForPlayers();
        } else {
            displayOpponents(this.state.username, this.state.game.players);
            this.displayHand(this.state.hand);
            displayTrick(this.state.trick);
        }
    }

    this.gameUpdate = function(data) {
        // Update the local copy of the game state with the server data
        var state = this.state;
        state.game = data;
        state.round = state.game.rounds[state.game.rounds.length - 1];
        state.hand = state.round.hands[state.username];
        if (state.round.tricks.length > 0) {
            state.trick = state.round.tricks[state.round.tricks.length - 1];
        } else {
            state.trick = [];
        }
    }

    this.setUsername = function(username) {
        this.state.username = username;
        this.render();
    }
}
