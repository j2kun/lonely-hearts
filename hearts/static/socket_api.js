function RoomSocket(api_url, heartsClient) {
    this.api_url = api_url;
    this.heartsClient = heartsClient;
    this.socket = io(this.api_url);

    this.join_room = function(room_id) {
        this.room_id = room_id;
        this.username = prompt('Enter your name: ');
        this.socket.emit('join', {
            room: this.room_id,
            username: this.username,
        });
        this.heartsClient.setUsername(this.username);
    };

    this.pass_cards = function(cards) {
        var data = {
            cards: cards
        };
        var result = this.socket.emit('pass_cards', data);
        if (result.status == 'failure') {
            this.heartsClient.resetPassing();
        } else {
            this.heartsClient.donePassing();
        }
    };

    var that = this;
    this.socket.on('game_update', function(data) {
        console.log('received game update: ');
        console.log(JSON.stringify(data, null, 2));
        that.heartsClient.gameUpdate(data);
        that.heartsClient.render();
    });
}
