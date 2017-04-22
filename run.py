from hearts import create_app
from hearts import socketio

app = create_app()
socketio.run(
    app,
    host=app.config['HOST'],
    port=app.config['PORT'],
    debug=app.config['DEBUG']
)
