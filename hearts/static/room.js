
function displayCard(apiCard) {
    return apiCard[1] + apiCard[0];
}

function apiCard(displayCard) {
    return displayCard[1] + displayCard[0];
}

// API returns data of the form
/*
{
    'players': [str],
    'max_points': int,
    'rounds': [
        {
            'players': str,
            'direction': str,
            'turn': int,
            'hands': {str: [str]},
            'tricks': [[str]],
            'hearts': self.hearts_broken,
            'current_scores': {str: int},
            'final_scores': {str: int},
            'is_over': boolean,
        }, ...
    ],
    'round_number': int,
    'scores': {str: int},
    'total_scores': {str: int},
    'is_over': boolean,
}
*/
var state = {
    chosenCards: [],
    game: null,
    me: 'Jeremy',
    mode: 'play',  // or 'passing'
};

function chooseOrUnchooseCard(card) {
    var foundIndex = $.inArray(card, state.chosenCards);
    if (foundIndex > -1) {
        state.chosenCards.splice(foundIndex, 1);
        return true;
    } else if (state.chosenCards.length < 3) {
        state.chosenCards.push(card);
        return true;
    } else {
        return false;
    }
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

function displayHand(hand) {
    var handToRender = '';
    for (var i = 0; i < hand.length; i++) {
        handToRender += '<li class="card" id="' + displayCard(hand[i]) + '"></li>'
    }
    $('#hand #cards_list').html(handToRender);
    $('#hand .card').click(handCardClick);
}

function handCardClick(event) {
    var card = apiCard(this.id);
    console.log('clicked ' + card);
    if (state.mode === 'passing') {
        if (chooseOrUnchooseCard(card)) {
            $(this).toggleClass('chosen_to_pass');
        }
    } else if (state.mode === 'play') {
        var success = true; // playCard(card);  // call the API
        if (success) {
            var index = state.hand.indexOf(card);
            state.hand.splice(index, 1);
            state.trick.push(card);
            render(state);
        }
    }
    // socket.emit('chat message', $('#m').val());
}

function displayTrick(trick) {
    var trickToRender = '';
    var orderedPositions = ['bottom', 'left', 'top', 'right'];
    for (var i = 0; i < trick.length; i++) {
        trickToRender += ('<div class="card ' + orderedPositions[i] + 
                           '" id="' + displayCard(trick[i]) + '"></div>');
    }
    $('#trick').html(trickToRender);
}

function renderWaitingForPlayers() {
    
}

function render(state) {
    if (state.game === null) {
        // game hasn't started yet
        renderWaitingForPlayers();
    } else {
        var currentRound = state.game.rounds[state.game.rounds.length - 1];
        var myHand = currentRound.hands[state.me];
        var currentTrick = currentRound.tricks[currentRound.tricks.length - 1];
        displayHand(myHand);
        displayTrick(currentTrick);
        displayOpponents(state.me, state.game.players);
    }
}

function setup() {
    $("body").removeClass("preload");
    render(state);
}


$(window).load(setup);
