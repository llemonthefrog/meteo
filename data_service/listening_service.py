import serial
import json
import os
from pymongo import MongoClient
from time import time
from dotenv import load_dotenv

SERIAL_PORT = "/dev/cu.usbmodem1201"
BAUDRATE = 115200

load_dotenv()

mongo = MongoClient(os.getenv("MONGO_URI"))
db = mongo.weather_db
collection = db.weather

ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

print("Listening Pico on USB...")

while True:
    line = ser.readline().decode("utf-8").strip()
    if not line:
        continue

    try:
        data = json.loads(line)
        data["timestamp"] = time()
        collection.insert_one(data)
        print("Saved:", data)
    except Exception as e:
        print("Parse error:", e, "line:", line)
