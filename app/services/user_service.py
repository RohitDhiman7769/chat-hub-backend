import db
from flask import Blueprint, request, jsonify, current_app,Flask
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token,get_jwt_identity,jwt_required
from flask_bcrypt import Bcrypt
import re


bcrypt = Bcrypt()
token_password = "my_secure_password"
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
]

def get_users():
    return users

def login(data):
    email = data.get("email")
    password = data.get("password")

    #Check email is exist or not 
    user = db.user_collection.find_one({"email": email})
    if not user: 
        return {"error": "Email not registered"}, 400
    
    #hash password 
    hashed_password = user.get("password")

    if bcrypt.check_password_hash(hashed_password, password):
         access_token = create_access_token(identity=email)
         user["_id"] = str(user["_id"])

        # Remove sensitive data (e.g., password)
         del user["password"]

         return jsonify({
            "code": 200,
            "message": "Login successful",
            "user_data": user,
            "access_token": access_token
        })
    else:
        return {"error": "Invalid password"}, 401



def forgetEmail(data):
    email = data.get("email")
    password = data.get("password")

    #Check email is exist or not 
    user = db.user_collection.find_one({"email": email})
    if not user: 
        return {"error": "Email not registered"}, 400
    


def create_user(data):

    email = data.get("email")
    password = data.get("password")
    profile_image = data.get("profileImage")

    if  not email or not password:
        return jsonify({"error": "Missing required fields"}), 401

  
    user = db.user_collection.find_one({"email": email})
    if user:
        return  {"error": "Email already registered"}, 400
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    db.user_collection.insert_one({ 'email' : email, 'password' : hashed_password, 'profile_img' : profile_image })
    return jsonify({"message": "User created successfully", "auth_token": hashed_password,'code' : 200})




def get_rooms_list():
    # user_id = request.args.get('userId')

    # # print('>>>>',user_id)
    # #Check email is exist or not 
    # user = db.rooms_collection.find_one({"user_id": user_id})
    # if not user: 
    #     return jsonify({"message": "No room exist",'code' : 200, 'room_list' : []})  
    # else:
    #     return {"message": "Room list fetched successfully",'code' : 200, 'room_list' : user}  
     user_id = request.args.get("userId")  # Ensure frontend sends 'userId' correctly
    
    #  if not user_id:
    #     return jsonify({"message": "User ID is required", "code": 400, "room_list": []})

    # Fetch all rooms where user_id matches
     rooms = list(db.rooms_collection.find({"user_id": user_id}))

     if not rooms:
        return jsonify({"message": "No rooms exist", "code": 200, "room_list": []})

    # Convert ObjectId to string for JSON serialization
     for room in rooms:
        room["_id"] = str(room["_id"])

     return jsonify({"message": "Room list fetched successfully", "code": 200, "room_list": rooms})


def creat_room(data):

    userId = data.get("userId")
    roomName = data.get("roomName")
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d%H%M%S")

    db.rooms_collection.insert_one({ 'user_id' : userId, 'room_id' : formatted_date, 'room_name' : roomName })
    return jsonify({"message": "Room has been created successfully", 'code' : 200})



def get_rooms_chats():
     roomId = request.args.get("roomId")
     print('roroomIdroomId' , roomId)
     return 'its workng '

def search_user_name():
    char = request.args.get("chr", "").strip()  # Get character from request, remove extra spaces
    print("char:", char)

    if not char:
        return jsonify({"error": "Character parameter (chr) is required"}), 400

    regex_pattern = f"^{re.escape(char)}"  # Escape special characters for regex safety
    
    users = list(db.user_collection.find({"email": {"$regex": regex_pattern, "$options": "i"}}, {"password": 0}))  # Case-insensitive search

    # Convert ObjectId to string for JSON serialization
    for user in users:
        user["_id"] = str(user["_id"])

    print("Users Found:", users)
    return jsonify(users)






# def update_user(user_id, data):
#     for user in users:
#         if user["id"] == user_id:
#             user.update(data)
#             return {"message": "User updated successfully", "user": user}
#     return {"error": "User not found"}

# def delete_user(user_id):
#     global users
#     users = [user for user in users if user["id"] != user_id]
#     return {"message": "User deleted successfully"}





# class UserService:
#     def __init__(self, mongo):
#         self.users_collection = mongo.db.users

#     def create_user(self, name, email, password):
#         user_data = {
#             "name": name,
#             "email": email,
#             "password": password,
#             "created_at": datetime.utcnow()
#         }
#         self.users_collection.insert_one(user_data)

#     def get_user_by_email(self, email):
#         return self.users_collection.find_one({"email": email})
