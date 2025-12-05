from flask import Flask, request, jsonify
from pymongo import MongoClient
import os

app = Flask(__name__)

mongo_url = os.getenv("MONGO_URI")

if not mongo_url:
    print("⚠ MONGO_URI not found. Using LOCAL MongoDB.")
    mongo_url = "mongodb://localhost:27017/"

# Connect to MongoDB
client = MongoClient(mongo_url)
 
# Database & Collection
db = client["Resturant"]        
collection = db["registration"] 

@app.route("/")
def home():
    return "Hello from MongoDB API!"

@app.route("/registration", methods=['POST'])
def registration():
    data = request.get_json()
    user_name = data.get("username")
    email = data.get("email")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    new_user = {
        "username": user_name,
        "email": email,
        "password": password,
        "confirm_password": confirm_password
    }
    collection.insert_one(new_user)

    return jsonify({"message": f"{user_name} inserted successfully"})

@app.route("/login", methods=['POST'])
def login():
    data = request.get_json(force=True, silent=True)

    email = data.get("email")
    password = data.get("password")

    user= collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "User not found"}), 404
    
    if user["password"] != password:
        return jsonify({"error": "Incorrect password"}), 401

    return jsonify({"message": "Login successfull!"})


if __name__ == "__main__":
    app.run(debug=True)
