### imports
from flask import Flask, render_template, request, redirect, url_for
import serial

### flask setup
app = Flask(__name__)
app.config.from_pyfile('config.py')

### arduino connection setup
arduino = serial.Serial("/dev/ttyACM0", 9600)

def runCommand(motor, speed, steps, direction, style):
    message = "{0};".format(",".join([motor, speed, steps, direction, style]))
    print "running: {0}".format(message)
    arduino.write(message)

### webserver
@app.route("/")
def index():
    message = []
    while arduino.inWaiting() > 0:
        message.append(arduino.readline())
    return render_template('index.html', message=message)

@app.route("/call", methods=['POST'])
def call():
    ### send to arduino
    args = ["motor", "speed", "steps", "direction", "style"]
    runCommand(*[request.form.get(v) for v in args])
    return redirect(url_for("index"))

if __name__ == "__main__":
    ### start the server
    app.run()