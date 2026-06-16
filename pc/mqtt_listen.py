import paho.mqtt.client as mqtt

BROKER = "broker.benax.rw"
TOPIC = "sensor_rutaganira_yanis_ntwali"


def on_message(client, userdata, msg):
    print(f"{msg.topic} -> {msg.payload.decode()}")


client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.subscribe(TOPIC)

print(f"Listening on {TOPIC} ...")
print("Start mqtt_client.py in another window to see messages.\n")

client.loop_forever()
