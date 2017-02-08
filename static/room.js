
function displayCard(apiCard) {
    return apiCard[1] + apiCard[0];
}

function apiCard(displayCard) {
    return displayCard[1] + displayCard[0];
}


$(window).load(function() {
  $("body").removeClass("preload");
  // var socket = io.connect('http://127.0.0.1:5000/chat');

  $('.card').click(function(event) {
    var card = apiCard(this.id);
    console.log('played ' + card);
    // socket.emit('chat message', $('#m').val());
  });

  //socket.on('chat message', function(msg){
  //  $('#messages').append($('<li>').text(msg));
  //});
});
