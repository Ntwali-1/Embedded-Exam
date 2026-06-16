import serial
import paho.mqtt.client as mqtt

SERIAL_PORT = "COM3"  # change if needed
BAUD_RATE = 9600

BROKER = "broker.benax.rw"
TOPIC = "sensor_rutaganira_yanis_ntwali"

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print("Monitoring temperature...\n")

while True:
    temp = ser.readline().decode().strip()

    if not temp:
        continue

    print("Temperature:", temp)

    client.publish(TOPIC, temp)
