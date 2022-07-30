from paho.mqtt import client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Device connected with result code: " + str(rc))

def on_disconnect(client, userdata, rc):
 print("Device disconnected with result code: " + str(rc))

def on_publish(client, userdata, mid):
    print(f"Device sent message")

def on_message(client, userdata, message):
    print("Message received: ", str(message.payload.decode("utf-8")))

client = mqtt.Client(client_id='')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_message = on_message

client.connect('test.mosquitto.org', port=1883)
client.loop_start()

while True:
    client.subscribe('test/something')