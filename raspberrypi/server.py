### imports
from flask import Flask, render_template, request, redirect, url_for
import serial

### flask setup
app = Flask(__name__)
app.config.from_pyfile('config.py')

### arduino connection setup
arduino = serial.Serial("/dev/ttyACM0", 9600)

def runCommand(motor, speed, steps, direction, style):
    """send the message to the arduino and return the execution code"""
    message = "{0};".format(",".join([motor, speed, steps, direction, style]))
    print "running: {0}".format(message)
    code = arduino.write(message)
    print "code: {0}".format(code)
    return code

### webserver
@app.route("/")
def index():
    """render the control page"""
    message = []
    while arduino.inWaiting() > 0:
        message.append(arduino.readline())
    return render_template('index.html', message=message)

@app.route("/call", methods=['POST'])
def call():
    """parse any messages and run them on the arduino"""
    ### send to arduino
    args = ["motor", "speed", "steps", "direction", "style"]
    runCommand(*[request.form.get(v) for v in args])
    return redirect(url_for("index"))

if __name__ == "__main__":
    ### start the server
    app.run()