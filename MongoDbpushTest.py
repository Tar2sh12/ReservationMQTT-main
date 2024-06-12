import random
from pymongo import MongoClient
from bson import ObjectId
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['ResturantReservation']
collection = db['reservations']
object_id = ObjectId("657bc4370c4fc677d4c1b928")
res_object_id = ObjectId("657f8285567f37ce852f605e")
# Define the document to be added to the collection
special = ["food when arrive", "I need all to be ready when arriving", "I want to sit on street view", "I want to sit in a corner", "I want a quit place to sit", "If no smoking cancel my reservation"]

for _ in range(0,20):
      new_document = {
        "customerId": object_id,
        "restaurantId": res_object_id,
        "numberOfSeats":random.randint(1, 50),
        "sepcialReq": random.choice(special),
        "reservationTime": "12:00-3:00",
        "reservationName": "MQTT"
      }
          # Insert the new document into the collection
      insert_result = collection.insert_one(new_document)

      # Check the inserted document's ID
      print(f"Inserted document ID: {insert_result.inserted_id}")
