
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
        chosenCards: [],
        game: null,
        username: 'Jeremy',
        mode: 'play',  // or 'passing'
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

    this.handCardClick = function(event) {
        var card = apiCard(this.id);
        console.log('clicked ' + card);
        if (this.state.mode === 'passing') {
            if (this.chooseOrUnchooseCard(card)) {
                $(this).toggleClass('chosen_to_pass');
            } // if 3, display button
        } else if (this.state.mode === 'play') {
            var success = true; // playCard(card);  // call the API
            if (success) {
                var index = this.state.hand.indexOf(card);
                this.state.hand.splice(index, 1);
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
        $('#hand .card').click(this.handCardClick.bind(this));
    }

    this.renderWaitingForPlayers = function() {
        
    }

    this.render = function() {
        if (this.state.game === null) {
            // game hasn't started yet
            this.renderWaitingForPlayers();
        } else {
            displayOpponents(this.state.username, this.state.game.players);

            var currentRound = this.state.game.rounds[this.state.game.rounds.length - 1];
            var myHand = currentRound.hands[this.state.username];
            this.displayHand(myHand);

            if (currentRound.tricks.length > 0) {
                var currentTrick = currentRound.tricks[currentRound.tricks.length - 1];
                displayTrick(currentTrick);
            } else {
                displayTrick([]);
            }
        }
    }

    this.gameUpdate = function(data) {
        this.state.game = data;
    }

    this.setUsername = function(username) {
        this.state.username = username;
        // Re-render username information
    }
}
