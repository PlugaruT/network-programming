import paho.mqtt.client as mqtt


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("/game")
    client.publish("/game", "Online")


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    if str(msg.payload)[0] == "?":
        response = str(raw_input("Answer: "))
        client.publish("/game", response)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
