import dataHandler

from flask import *
from flask_socketio import SocketIO


# Create flask app, SocketIO object, and global pi 'thing' object.
app = Flask(__name__)
socketio = SocketIO(app)
dataHandler = dataHandler.dataHandler()


# Define app routes.
# Index route renders the main HTML page.
@app.route("/")
def index():
    # Read the current switch state to pass to the template.
#    switch = pi_thing.read_switch()
    # Render index.html template.
    return render_template('index.html')

# Listen for SocketIO event that will change the LED.
#@socketio.on('change_led')
#def change_led(led):
#    if led == 'on':
#        pi_thing.set_led(True)
#    elif led == 'off':
#        pi_thing.set_led(False)

# Internal callback that will be called when the switch changes state.
#def switch_change(switch):
    # Broadcast a switch change event.
#   socketio.emit('switch_change', { 'switch': switch })

# Internal callback that will be called when a new temperature & humidity reading is ready.
#def temp_humidity_change(temperature, humidity):
    # Broadcast a temp & humidity change event.
#   socketio.emit('temp_humidity_change', { 'temperature': temperature, 'humidity': humidity })

def data_change(data, count):
    socketio.emit('data_change', {'data': data, 'count': count})

@app.route("/test")
def test_page():
	return render_template('test.html')

def data_change(data, count):
    socketio.emit('data_change', {'data': data, 'count': count})

if __name__ == "__main__":
    # Register callbacks for switch and temp/humidity event changes.
#   pi_thing.on_switch_change(switch_change)
#   pi_thing.on_temp_humidity_change(temp_humidity_change)
    dataHandler.on_data_change(data_change)
    # Run the flask development web server with SocketIO.
    socketio.run(app, host='0.0.0.0', debug=True)
