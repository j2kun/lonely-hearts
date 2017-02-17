
function displayCard(apiCard) {
    return apiCard[1] + apiCard[0];
}

function apiCard(displayCard) {
    return displayCard[1] + displayCard[0];
}

var state = {
    passing: true,
    hand: [],
    trick: [],
    players: [],
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
    var hand_to_render = '';
    for (var i = 0; i < hand.length; i++) {
        hand_to_render += '<li class="card" id="' + displayCard(hand[i]) + '"></li>'
    }
    $('#hand #cards_list').html(hand_to_render);
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

function setup() {
    $("body").removeClass("preload");
    // var socket = io.connect('http://127.0.0.1:5000/chat');

    $('#hand .card').click(handCardClick);

    //socket.on('chat message', function(msg){
    //    $('#messages').append($('<li>').text(msg));
    //});
}


$(window).load(setup);
