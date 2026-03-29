from flask import Flask, jsonify, render_template
import serial
import threading

app = Flask(__name__)

ser = serial.Serial('COM3', 9600)  # CHANGE THIS
data = {"temp": 0, "moist": 0}

THRESHOLD = 300

def read_serial():
    global data
    while True:
        line = ser.readline().decode().strip()

        if "MOIST" in line:
            parts = line.split(",")
            temp = float(parts[0].split(":")[1])
            moist = int(parts[1].split(":")[1])

            data = {"temp": temp, "moist": moist}

threading.Thread(target=read_serial, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)