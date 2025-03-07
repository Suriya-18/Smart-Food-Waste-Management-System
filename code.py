from flask import Flask, request, jsonify
import sqlite3
import cv2
import numpy as np
from twilio.rest import Client

app = Flask(__name__)

# Twilio API Setup
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "your_twilio_phone"

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# Database Setup
def init_db():
    conn = sqlite3.connect("food_donations.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS donations 
                 (id INTEGER PRIMARY KEY, donor TEXT, food_item TEXT, expiry_date TEXT, location TEXT, receiver TEXT)''')
    conn.commit()
    conn.close()

@app.route("/donate", methods=["POST"])
def donate():
    data = request.json
    donor = data["donor"]
    food_item = data["food_item"]
    expiry_date = data["expiry_date"]
    location = data["location"]

    conn = sqlite3.connect("food_donations.db")
    c = conn.cursor()
    c.execute("INSERT INTO donations (donor, food_item, expiry_date, location, receiver) VALUES (?, ?, ?, ?, ?)", 
              (donor, food_item, expiry_date, location, None))
    conn.commit()
    conn.close()

    # Notify NGOs (replace with real phone numbers)
    message = f"New food donation available: {food_item}, expires on {expiry_date}, location: {location}."
    client.messages.create(to="+1234567890", from_=TWILIO_PHONE_NUMBER, body=message)

    return jsonify({"message": "Donation added successfully!"})

@app.route("/list_donations", methods=["GET"])
def list_donations():
    conn = sqlite3.connect("food_donations.db")
    c = conn.cursor()
    c.execute("SELECT * FROM donations WHERE receiver IS NULL")
    donations = c.fetchall()
    conn.close()
    return jsonify(donations)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
