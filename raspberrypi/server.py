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
    code = arduino.write(message)
    return code

### webserver
@app.route("/")
def index():
    """render the control page"""
    return render_template('index.html')

@app.route("/call", methods=['POST'])
def call():
    """parse any messages and run them on the arduino"""
    ### send command to arduino
    args = ["motor", "speed", "steps", "direction", "style"]
    code = runCommand(*[request.form.get(v) for v in args])
    
    ### gather messages return from arduino
    message = ["return code: {0}".format(code),]
    while arduino.inWaiting() > 0:
        message.append(arduino.readline())
    return render_template('message.html', message=message)

if __name__ == "__main__":
    ### start the server
    app.run()