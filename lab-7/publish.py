import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")
mqttc.connect("localhost", 1883)
mqttc.publish("/game", "?Hello, World! from me")
mqttc.loop(2)
