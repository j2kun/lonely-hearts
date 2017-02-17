
function displayCard(apiCard) {
    return apiCard[1] + apiCard[0];
}

function apiCard(displayCard) {
    return displayCard[1] + displayCard[0];
}

// Will remove dummy data once we pull state from the API
var state = {
    passing: true,
    hand: ['2h', '5s', '6c', 'Jc', 'Kd', 'As'],
    trick: [],
    players: ['Jeremy', 'Erin', 'Daniel', 'Lauren'],
    turn: 'Jeremy',
    mode: 'play',  // or 'passing'
    chosenCards: []
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
    if (state.passing) {
        if (chooseOrUnchooseCard(card)) {
            $(this).toggleClass('chosen_to_pass');
        }
    }
    // socket.emit('chat message', $('#m').val());
}

function displayTrick(trick) {
    var trickToRender = '';
    var orderedPositions = ['trick_bottom', 'trick_left', 'trick_top', 'trick_right'];
    for (var i = 0; i < trick.length; i++) {
        trickToRender += ('<div class="card ' + orderedPositions[i] + 
                           '" id="' + displayCard(trick[i]) + '"></div>');
    }
    $('#trick').html(trickToRender);
}

function render(state) {
    displayHand(state.hand);
    displayTrick(state.trick);
}

function setup() {
    $("body").removeClass("preload");
    // var socket = io.connect('http://127.0.0.1:5000/chat');
    //socket.on('chat message', function(msg){
    //    $('#messages').append($('<li>').text(msg));
    //});
    render(state);
}


$(window).load(setup);
