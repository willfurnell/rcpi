import paho.mqtt.client as mqtt
import settings


# Interact with the hardware
def go_forward():
    print("Going forward...")


def go_backward():
    print("Going backwards...")


def go_left():
    print("Going left...")


def go_right():
    print("Going right...")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("Connected with result code " + str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(settings.TOPIC)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = msg.payload.decode('utf-8')
    if message == "w":
        go_forward()
    elif message == "s":
        go_backward()
    elif message == "a":
        go_left()
    elif message == "d":
        go_right()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(settings.MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()