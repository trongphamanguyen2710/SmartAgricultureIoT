import sys
from Adafruit_IO import MQTTClient
import time
import random
from simple_ai import *

AIO_FEED_ID = ["nutnhan1", "nutnhan2"]
AIO_USERNAME = "batrong0610"
AIO_KEY = "aio_jKkj10AwWDiNJP4Ct6KhwAkRgHnw"

def connected(client):
    print("Ket noi thanh cong ...")
    client.subscribe(AIO_FEED_ID)
    for topic in AIO_FEED_ID:
        client.subscribe(topic)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print("Nhan du lieu: " + payload + " , feed id: " + feed_id)
    if feed_id == "nutnhan1":
        if payload == "0":
            writeData("1")
        else:
            writeData("2")
    elif feed_id == "nutnhan2":
        if payload == "0":
            writeData("3")
        else:
            writeData("4")


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()
counter = 10
sensor_type = 0
counter_ai = 0
while True:
    counter = counter - 1
    if counter <= 0:
        counter = 10
        print("Random data is publishing...")
        if sensor_type == 0:
            print("Temperature...")
            temp = random.randint(10, 20)
            client.publish("cambien1", temp)
            sensor_type = 1
            print("Temperature : ", temp)
        elif sensor_type == 1:
            print("Humidity...")
            humi = random.randint(50 , 70)
            client.publish("cambien2", humi)
            print("Humidity : ", humi)
            sensor_type = 2
        elif sensor_type == 2:
            print("Light...")
            light = random.randint(100, 500)
            client.publish("cambien3", light)
            print("Light : ", light)
            sensor_type = 0
    '''counter_ai = counter_ai - 1
    if counter_ai <= 0:
        counter_ai = 5
        ai_result = image_detector()
        print("AI output: ", ai_result)
        client.publish("nhan-dang-ai", ai_result)'''
    time.sleep(1)
