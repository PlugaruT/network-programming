import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")
mqttc.connect("139.59.161.37", 1883)
mqttc.publish("test", "alalalala")
mqttc.loop(2)

print("alalalala")
