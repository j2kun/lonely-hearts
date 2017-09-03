function RoomSocketClient(api_url) {
    this.api_url = api_url;
    this.socket = io(this.api_url);

    this.join_room = function(room_id, username) {
        return this.socket.emit('join', {
            room: this.room_id,
            username: this.username,
        });
    };

    this.pass_cards = function(cards) {
        var data = {
            cards: cards
        };
        var result = this.socket.emit('pass_cards', data);
        return result.status;
    };

    this.setup_game_update_handler(gameUpdateFn) {
        this.socket.on('game_update', function(data) {
            console.log('received game update: ');
            console.log(JSON.stringify(data, null, 2));
            gameUpdateFn(data);
        });
    }
}
