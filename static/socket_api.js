var CHAT = 'chat';

function api(api_url) {
    this.api_url = api_url;
    this.socket = io(this.api_url);

    this.join_room = function(room_id) {
        this.room_id = room_id;
        this.socket.emit('join', {room: this.room_id, username: 'Bill'});
    };

    this.chat = function(message) {
        this.socket.emit('chat', message);
    }
}
