import paho.mqtt.client as mqtt
import settings
import RPI.GPIO as GPIO

# Interact with the hardware
def go_forward():
    print("Going forward...")
    GPIO.output(settings.HB_PIN_2, False)
    GPIO.output(settings.HB_PIN_4, False)
    GPIO.output(settings.HB_PIN_1, True)
    GPIO.output(settings.HB_PIN_3, True)

def go_backward():
    print("Going backwards...")
    # Turn PIN_MOTOR_RIGHT ON and PIN_MOTOR_LEFT ON,
    # but reverse...
    GPIO.output(settings.HB_PIN_1, False)
    GPIO.output(settings.HB_PIN_3, False)
    GPIO.output(settings.HB_PIN_2, True)
    GPIO.output(settings.HB_PIN_4, True)


def go_left():
    print("Going left...")
    # Turn PIN_MOTOR_RIGHT ON
    GPIO.output(settings.HB_PIN_1, True)
    GPIO.output(settings.HB_PIN_3, False)
    GPIO.output(settings.HB_PIN_2, False)
    GPIO.output(settings.HB_PIN_4, False)


def go_right():
    print("Going right...")
    # Turn PIN_MOTOR_LEFT ON
    GPIO.output(settings.HB_PIN_1, False)
    GPIO.output(settings.HB_PIN_3, True)
    GPIO.output(settings.HB_PIN_2, False)
    GPIO.output(settings.HB_PIN_4, False)


def brake():
    GPIO.output(settings.HB_PIN_1, False)
    GPIO.output(settings.HB_PIN_3, False)
    GPIO.output(settings.HB_PIN_2, False)
    GPIO.output(settings.HB_PIN_4, False)


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
    else:
        brake()

GPIO.setmode(GPIO.BCM)
GPIO.setup(settings.HB_PIN_1, GPIO.OUT)
GPIO.setup(settings.HB_PIN_2, GPIO.OUT)
GPIO.setup(settings.HB_PIN_3, GPIO.OUT)
GPIO.setup(settings.HB_PIN_4, GPIO.OUT)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(settings.MQTT_SERVER, 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()