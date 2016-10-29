import paho.mqtt.client as mqtt
import settings

client = mqtt.Client()
client.connect(settings.MQTT_SERVER,1883,60)


def p(message):
    client.publish(settings.TOPIC, message)


while True:
    try:
        message = input("Enter direction >> ")
        p(message)
    except KeyboardInterrupt:
        client.disconnect()
        print("Disconnected from " + settings.MQTT_SERVER + " Shutting down...")
        exit()
