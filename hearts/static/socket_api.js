function makeid() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < 5; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function RoomSocket(api_url, state) {
    this.api_url = api_url;
    this.state = state;
    this.socket = io(this.api_url);

    this.join_room = function(room_id) {
        this.room_id = room_id;
        this.username = 'Bill ' + makeid(),
        this.socket.emit('join', {
            room: this.room_id,
            username: this.username,
        });
        this.state.username = this.username;
    };

    var that = this;
    this.socket.on('game_update', function(data) {
        console.log('received game update: ');
        console.log(JSON.stringify(data, null, 2));
        that.state.game_update(data);
        that.state.render();
    });
}
