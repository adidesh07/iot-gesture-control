from hand_tracker import handDetector
import cv2
import time
# import serial
from paho.mqtt import client as mqtt


"""
Detect tip of index finger, tip of thumb, calculate real-time distance between them.
Send toggle signal every time distance crosses a threshold value.

Landmark indices:
Tip of thumb = 4
Tip of index finger = 8
"""

def on_connect(client, userdata, flags, rc):
    print("Device connected with result code: " + str(rc))

def on_disconnect(client, userdata, rc):
 print("Device disconnected with result code: " + str(rc))

def on_publish(client, userdata, mid):
    print(f"Device sent message")

def on_message(client, userdata, message):
    print("Message received: ", str(message.payload.decode("utf-8")))


curTime = 0
prevTime = 0
capture = cv2.VideoCapture(0)
detector = handDetector()

client = mqtt.Client(client_id='')
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_message = on_message

# boardComm = serial.Serial(
#     'COM9', # Active port connected to USB for serial communication with controller
#     115200, # Baud rate for contrller
# )

# if not boardComm.is_open:
#     boardComm.open()

client.connect('test.mosquitto.org', port=1883)

# Check flag to ensure toggle operations occurs only once for each condition
check = 0

client.loop_start()

while True:
    success, image = capture.read()
    image = detector.findHands(image)

    # List of landmark indices, their x, y positions
    # [ind, xpos, ypos]
    landmarkList = detector.findPos(image)
    
    if len(landmarkList) > 0:
        xThumb, yThumb = landmarkList[4][1::]
        xIndex, yIndex = landmarkList[8][1::]

        # Calculate distance from points
        xLen = abs(xThumb - xIndex)
        yLen = abs(yThumb - yIndex)
        distance = (xLen ** 2 + yLen ** 2) ** 0.5
        
        if distance < 50 and check:
            check = 0
            client.publish('test/something', 'OFF')
            print('OFF')
        elif distance >= 50 and not check:
            check = 1
            client.publish('test/something', 'ON')
            print('ON')

    curTime = time.time()
    fps = 1 / (curTime - prevTime)
    prevTime = curTime

    cv2.putText(image, str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN,
                2, (255, 0, 0), 2)
    cv2.imshow('Motion Detection', image)
    cv2.waitKey(1)

