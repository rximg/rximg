from flask_socketio import SocketIO#, emit, send
from flask import Flask, abort, request, send_file,render_template
from flask_cors import CORS

app = Flask(__name__,
static_folder='./frontend/dist',  
template_folder = "./frontend/dist",
static_url_path="") 

app.debug = True
app.config['SECRET_KEY'] = 'socket.io'
app.config['LOGIN_DISABLED'] = True
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins='*', async_mode='threading')


if __name__ == '__main__':
    # app.run(debug=True)
    # clean_tempfile(IMG_CACHE_DIR)
    socketio.run(app)

