from hearts import create_app
from hearts import socketio

app = create_app()
socketio.run(app, host='0.0.0.0', port=5000)
