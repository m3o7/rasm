### imports
from flask import Flask, render_template, request, redirect, url_for
from canvas import Canvas

### flask setup
app = Flask(__name__)
app.config.from_pyfile('config.py')

### setup canvas
canvas = Canvas()

### webserver
@app.route("/")
def index():
    """render the control page"""
    return render_template('index.html', canvas=canvas)

@app.route("/call", methods=['POST'])
def call():
    """parse any messages and run them on the arduino"""
    ### send command to arduino
    args = ["motor", "speed", "steps", "direction", "style"]
    code = canvas.runCommand(*[request.form.get(v) for v in args])
    
    ### gather messages return from arduino
    message = [ "position: {0}".format(canvas.position),
                "l/r: ({0}: {1})".format(canvas.left, canvas.right),
                "return code: {0}".format(code),]
    while canvas.arduino.inWaiting() > 0:
        message.append(canvas.arduino.readline())
    return render_template('message.html', message=message)

@app.route("/setup", methods=['POST'])
def setup():
    """setup the geometry for the canvas"""
    left = request.form.get("left")
    right = request.form.get("right")
    motors_apart = request.form.get("motors_apart")
    canvas.updateGeometry(left=left, right=right, motors_apart=motors_apart)
    return redirect(url_for("index"))

@app.route("/move", methods=['POST'])
def move():
    x = request.form.get("x")
    y = request.form.get("y")
    canvas.moveTo(x, y)
    return redirect(url_for("index"))

if __name__ == "__main__":
    ### start the server
    app.run()