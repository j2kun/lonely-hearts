/*
 * Hearts game state maintainer
 *
 * example state:
{
  "players": [
    "BillSpsP7", "Bill Xnnqk", "Bill tC3g1", "Bill sEYQH"
  ],
  "messages": {
    "BillSpsP7": ["message1", "message2"],
    "BillXnnqk": ["message3"],
    "BilltC3g1": [],
    "BillsEyQH": []
  },
  "player_action": {
    "BillSpsP7": "play",
    "BillXnnqk": "wait",
    "BilltC3g1": "wait",
    "BillsEyQH": "wait"
  },
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

function RoomState(username) {
  this.chosenCards = [];
  this.game = null;
  this.username = username;

  this.chooseOrUnchooseCard = function(card) {
    var foundIndex = $.inArray(card, this.chosenCards);
    if (foundIndex > -1) {
      this.chosenCards.splice(foundIndex, 1);
      return true;
    } else if (this.chosenCards.length < 3) {
      this.chosenCards.push(card);
      return true;
    } else {
      return false;
    }
  }

  this.round = function() {
    let rounds = this.game.rounds();
    return rounds[rounds.length - 1];
  }

  this.hand = function() {
    return this.round().hands[this.username];
  }

  this.trick = function() {
    let round = this.round();
    return round.tricks[round.tricks.length - 1];
  }

  this.mode = function() {
    return this.game.player_action[this.username];
  }

  this.gameUpdate = function(data) {
    this.game = data;
  }
}
