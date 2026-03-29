from flask import Flask, jsonify, render_template
import serial
import threading
import time
from typing import Optional

app = Flask(__name__)

ser = serial.Serial('COM5', 9600)  
data = {"temp": 0, "moist": 0, "last_watered": None}

THRESHOLD = 300

prev_moist = THRESHOLD
#unix timestamp of when last watered
last_watered: Optional[float] = None

def read_serial():
    global data
    global prev_moist, last_watered
    while True:
        line = ser.readline().decode().strip()

        if "MOIST" in line:
            parts = line.split(",")
            temp = float(parts[0].split(":")[1])
            moist = int(parts[1].split(":")[1])

            #dry to wet
            if moist >= THRESHOLD and prev_moist < THRESHOLD:
                last_watered = time.time()

            prev_moist = moist

            data = {"temp": temp, "moist": moist, "last_watered": int(last_watered) if last_watered else None}

threading.Thread(target=read_serial, daemon=True).start()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)