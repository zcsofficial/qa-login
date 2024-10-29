from flask import Flask, request, jsonify, Blueprint
from pymongo import MongoClient
import cloudinary
import cloudinary.uploader
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# MongoDB Atlas connection
mongo_uri = "mongodb+srv://contactzcsco:Z3r0c0575k1ll%4066202@zcsproduction.zld0i.mongodb.net/?retryWrites=true&w=majority&appName=ZCSProduction"
client = MongoClient(mongo_uri)
db = client["NCCDatabase"]

# Cloudinary configuration
cloudinary.config( 
    cloud_name = "dxevrrj4j", 
    api_key = "853367529692421", 
    api_secret = "qmkkPh2MEoQCSJ2OLfHeQbaYVFk",  
    secure=True
)

# Collection references
profiles_collection = db["profiles"]
cadets_collection = db["cadets"]

# Route to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    name = data.get("name")
    email = data.get("email")
    is_admin = data.get("is_admin", False)

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Hash the password before saving
    hashed_password = generate_password_hash(password)
    
    user_profile = {
        "username": username,
        "password": hashed_password,
        "name": name,
        "email": email,
        "is_admin": is_admin
    }

    profiles_collection.insert_one(user_profile)
    return jsonify({"message": "User registered successfully!"}), 201

# Route to login a user
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = profiles_collection.find_one({"username": username})
    
    if user and check_password_hash(user["password"], password):
        return jsonify({
            "message": "Login successful",
            "is_admin": user.get("is_admin", False)
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# Route to add a new cadet profile
@app.route('/add_cadet', methods=['POST'])
def add_cadet():
    try:
        data = request.form
        name = data.get("name")
        cadet_id = data.get("cadet_id")
        rank = data.get("rank")
        year = data.get("year")
        location = data.get("location")
        achievements = data.get("achievements")
        image_file = request.files.get("profile_picture")

        if image_file:
            upload_result = cloudinary.uploader.upload(image_file)
            image_url = upload_result["secure_url"]
        else:
            return jsonify({"error": "Profile picture is required"}), 400

        cadet_profile = {
            "name": name,
            "cadet_id": cadet_id,
            "rank": rank,
            "year": year,
            "location": location,
            "achievements": achievements,
            "profile_picture": image_url
        }

        cadets_collection.insert_one(cadet_profile)
        return jsonify({"message": "Cadet profile added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to retrieve a cadet profile by cadet_id
@app.route('/get_cadet/<cadet_id>', methods=['GET'])
def get_cadet(cadet_id):
    cadet_profile = cadets_collection.find_one({"cadet_id": cadet_id})
    if cadet_profile:
        cadet_profile["_id"] = str(cadet_profile["_id"])
        return jsonify(cadet_profile), 200
    else:
        return jsonify({"error": "Cadet not found"}), 404

# Route to update permissions
@app.route('/update_permissions/<username>', methods=['PATCH'])
def update_permissions(username):
    data = request.json
    is_admin = data.get("is_admin", None)
    can_edit_blog = data.get("can_edit_blog", None)
    
    update_fields = {}
    if is_admin is not None:
        update_fields["is_admin"] = is_admin
    if can_edit_blog is not None:
        update_fields["can_edit_blog"] = can_edit_blog

    result = profiles_collection.update_one({"username": username}, {"$set": update_fields})

    if result.matched_count > 0:
        return jsonify({"message": "Permissions updated successfully!"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

# Route to enable blog editing
@app.route('/enable_blog_edit/<username>', methods=['PATCH'])
def enable_blog_edit(username):
    result = profiles_collection.update_one({"username": username}, {"$set": {"can_edit_blog": True}})

    if result.matched_count > 0:
        return jsonify({"message": "Blog editing enabled for user."}), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    print("Server is running and MongoDB connection is OK")
    app.run(host="0.0.0.0", port=5000, debug=False)
