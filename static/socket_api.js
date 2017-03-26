var CHAT = 'chat';

function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function RoomSocket(api_url) {
    this.api_url = api_url;
    this.socket = io(this.api_url);
    this.socket.on(CHAT, function(data) {
        console.log('User chatted: ' + data);
    });

    this.join_room = function(room_id) {
        this.room_id = room_id;
        this.socket.emit('join', {
            room: this.room_id,
            username: 'Bill' + makeid(),
        });
    };

    this.chat = function(message) {
        console.log('Submitting chat: ' + message);
        this.socket.emit(CHAT, message);
    }
}
