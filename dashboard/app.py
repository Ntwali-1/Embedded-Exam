import threading
from datetime import datetime

import paho.mqtt.client as mqtt
from flask import Flask, jsonify, render_template

CANDIDATE_NAME = "Rutaganira Yanis Ntwali"
BROKER = "broker.benax.rw"
TOPIC = "sensor_rutaganira_yanis_ntwali"
MQTT_PORT = 1883
WEB_PORT = 8059

state = {
    "temperature": None,
    "updated_at": None,
    "mqtt_connected": False,
    "history": [],
}


def on_connect(client, userdata, flags, reason_code, properties=None):
    state["mqtt_connected"] = reason_code == 0
    if reason_code == 0:
        client.subscribe(TOPIC)


def on_disconnect(client, userdata, flags, reason_code, properties=None):
    state["mqtt_connected"] = False


def on_message(client, userdata, msg):
    temp = msg.payload.decode().strip()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    state["temperature"] = temp
    state["updated_at"] = now
    state["history"] = ([{"temp": temp, "time": now}] + state["history"])[:20]


def start_mqtt():
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message
    client.connect(BROKER, MQTT_PORT, 60)
    client.loop_forever()


app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        candidate_name=CANDIDATE_NAME,
        topic=TOPIC,
        broker=BROKER,
    )


@app.route("/api/data")
def api_data():
    return jsonify(
        {
            "candidate_name": CANDIDATE_NAME,
            "temperature": state["temperature"],
            "updated_at": state["updated_at"],
            "mqtt_connected": state["mqtt_connected"],
            "topic": TOPIC,
            "broker": BROKER,
            "history": state["history"],
        }
    )


if __name__ == "__main__":
    threading.Thread(target=start_mqtt, daemon=True).start()
    app.run(host="0.0.0.0", port=WEB_PORT, debug=False)
