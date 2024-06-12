import json

from paho.mqtt import client as mqtt_client
import random
import time
from pymongo import MongoClient
from bson import ObjectId
broker = 'broker.emqx.io'
port = 1883
topic = "python/mqtt"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# mongo  connection
mongoClient = MongoClient('mongodb://localhost:27017/')
db = mongoClient['ResturantReservation']
collection = db['reservations']
# data to send from

# Define the document to be added to the collection
special = ["food when arrive", "I need all to be ready when arriving", "I want to sit on street view", "I want to sit in a corner", "I want a quit place to sit", "If no smoking cancel my reservation"]


def data_to_send():
    return {
        "customerId": '657f98829e21ccac6a55508c',
        "restaurantId": '657f8285567f37ce852f605e',
        "numberOfSeats":random.randint(1, 50),
        "sepcialReq": random.choice(special),
        "reservationTime": "12:00-3:00",
        "reservationName": "MQTT"
    }


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
         time.sleep(2)
         data = data_to_send()
         result = client.publish(topic, json.dumps(data))
         # result: [0, 1]
         status = result[0]
         if status == 0:
             print(f"Send reservation from `{data['reservationName']}` to topic `{topic}`")
         else:
             print(f"Failed to send message to topic {topic}")

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode('utf-8'))
        data['customerId'] = ObjectId(data['customerId'])
        data['restaurantId'] = ObjectId(data['restaurantId'])
        print(f"Received reservation by `{data['reservationName']}` from `{msg.topic}` topic")
        collection.insert_one(data)
    client.subscribe(topic)
    client.on_message = on_message


client = connect_mqtt()
client.loop_start()
subscribe(client)
publish(client)
client.loop_forever()
