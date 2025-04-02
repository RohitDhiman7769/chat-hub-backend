import db
from flask import Blueprint, request, jsonify, current_app,Flask
from datetime import datetime
from flask_jwt_extended import  create_access_token
from flask_bcrypt import Bcrypt
import re
from bson import ObjectId

bcrypt = Bcrypt()
token_password = "my_secure_password"

# fetch all users
def get_users():
    userId = request.args.get("userId") 
    users = list(db.user_collection.find(
    {"_id": {"$ne": ObjectId(userId)}},  
    {"password": 0}  
))
    for user in users:
        user["_id"] = str(user["_id"])  

    return jsonify({"message": "Data fetched successfully", "code":200, "data" : users,})  # Return JSON response


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

    db.user_collection.insert_one({ 'email' : email, 'password' : hashed_password, 'profile_img' : profile_image , 'initial_login' : 1, 'reported_count': 0})
    return jsonify({"message": "User created successfully", "auth_token": hashed_password,'code' : 200})




# def get_rooms_list():
#     user_id = request.args.get("userId") 
#     rooms = list(db.room_member_Ids_collection.find({"added_to": user_id}))
#     print('1!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!',rooms)
#     if not rooms:
#         return jsonify({"message": "No rooms exist", "code": 200, "room_list": []})
#     for room in rooms:
#          room["_id"] = str(room["_id"])
            
#     result_data = []
        
#     for room in rooms:
#         result_data.append (list(db.rooms_collection.find({"room_id": room.get('room_id')})))
        
#     print('/////////////////////////',result_data)
    
#     return jsonify({"message": "Room list fetched successfully", "code": 200, "room_list": rooms,'room_details' : result_data})

from bson import ObjectId

def get_rooms_list():
    user_id = request.args.get("userId") 
    rooms = list(db.room_member_Ids_collection.find({"added_to": user_id}))
    
    if not rooms:
        return jsonify({"message": "No rooms exist", "code": 200, "room_list": []})

    # Convert _id fields to strings
    for room in rooms:
        room["_id"] = str(room["_id"])

    # result_data = []

    for room in rooms:
        # Fetch room details
        room_details = list(db.rooms_collection.find({"room_id": room.get('room_id')}))
        
        # Convert _id in room details to strings
        for detail in room_details:
            detail["_id"] = str(detail["_id"])
        
        # result_data.append(room_details)

    return jsonify({
        "message": "Room list fetched successfully",
        "code": 200,
        "data": room_details
    })


def creat_room(data):

    userId = data.get("userId")
    roomName = data.get("roomName")
    roomType = data.get("roomType")
    roomImgIcon = data.get("roomImgIcon")
    roomMembersIds = data.get("roomMembersIds")
    now = datetime.now()
    formatted_date = now.strftime("%Y%m%d%H%M%S")


    for id in roomMembersIds:
       db.room_member_Ids_collection.insert_one({ 
        'added_by' : userId,
        'added_to' : id,
        'room_id' : formatted_date, 
        
    })
   
    db.rooms_collection.insert_one({ 
        'user_id' : userId, 
        'room_id' : formatted_date, 
        'room_name' : roomName,
        'room_type' : roomType,
        'image': roomImgIcon
        })

    # print('**********************',formatted_date)

    roomDetails = list(db.rooms_collection.find({ 'room_id' : formatted_date}))   
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!',roomDetails[0].get('room_id'))
    # Step 2: Get added_to values from room_member_Ids_collection
    room_members = list(db.room_member_Ids_collection.find({"room_id": str(roomDetails[0].get('room_id'))}))
    
    # print('""""""""""""""""""""""""""""""""""""',room_members)
    
    added_to_ids = [member.get('added_to') for member in room_members]

    # print('££££££££££££££££££££££££££',added_to_ids)

    # Step 3: Fetch user details using added_to values
    user_list = list(db.user_collection.find({"_id": {"$in": [ObjectId(user_id) for user_id in added_to_ids]}}))

    # print(user_list)
    # Convert ObjectId to string
    room_details = convert_objectid(roomDetails)
    room_members_data = convert_objectid(user_list)

    update_response_data = {
        'room_details' : room_details,
        'member_list' : room_members_data
    }
    
    return jsonify({"message": "Data successfully", 'code' : 200, 'data' :update_response_data })


def get_rooms_chats():
     roomId = request.args.get("roomId")
    #  print('roroomIdroomId' , roomId)
     return 'its workng '

def search_user_name():
    char = request.args.get("chr", "").strip()  # Get character from request, remove extra spaces
    # print("char:", char)

    if not char:
        return jsonify({"error": "Character parameter (chr) is required"}), 400

    regex_pattern = f"^{re.escape(char)}"  # Escape special characters for regex safety
    
    users = list(db.user_collection.find({"email": {"$regex": regex_pattern, "$options": "i"}}, {"password": 0}))  # Case-insensitive search

    # Convert ObjectId to string for JSON serialization
    for user in users:
        user["_id"] = str(user["_id"])

    # print("Users Found:", users)
    return jsonify({"message": "User data fetched successfully", "code":200, "data" : users,})  # Return JSON response


def creat_friends (data):
    userId = data.get("user_id")
    roomName = data.get("arrayOfAddedUsersId")
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
    db.user_collection.update_one({ "_id":ObjectId(userId)},{"$set": {"initial_login": 2 }})
    
    for friend_id in roomName:
        db.user_friends_collection.insert_one({  
            'added_by': ObjectId(userId),  
            'added_to': ObjectId(friend_id),  # Store each ID separately
            'added_status': 1,  
            'time': formatted_time  
        })  
    return jsonify({"message": "Request send successfully! Waiting for adding back", 'code' : 200})

def profile():
    user_id = request.args.get("user_id")  # Get user ID from query params
    # print("Received user_id:", user_id)

    if not user_id:
        return jsonify({"error": "User ID not provided, please refresh the page"}), 400

    try:
        # Convert user_id to ObjectId
        user = db.user_collection.find_one({"_id": ObjectId(user_id)}, {"password": 0})  # Exclude password
       
        addFriendRequest = db.user_friends_collection.find(
       {"added_to": user_id, "added_status": 1},
       {"_id": 0, "added_by": 1} )

        # Extracting the results
        added_by_list = [doc["added_by"] for doc in addFriendRequest]

        added_by_object_ids = [ObjectId(uid) for uid in added_by_list]

        # Query to get user details excluding passwords
        users = db.user_collection.find({"_id": {"$in": added_by_object_ids}},{"password": 0} )

        # Convert cursor to list of user details
        user_list = list(users)

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Convert ObjectId to string
        user["_id"] = str(user["_id"])

        # val = {
        #     'profileData' : user,
        #     'addingRequest' : user_list
        # }
        response_data = {
        "message": "Profile data fetched successfully",
        "code": 200,
        "data":  convert_objectid({
            "profileData": user,
            "addingRequest": user_list
        })
    }
    
        return jsonify(response_data)

    except Exception as e:
        # print("Error fetching user:", str(e))
        return jsonify({"error": "Invalid User ID"}), 400  # Handle invalid ObjectId

def confirm_pending_req(data):
    userId = data.get("user_id")
    request_id = data.get("confirm_user_request_id")

    db.user_friends_collection.update_one(
    { "added_to": userId, "added_by": request_id },  # Filter condition
    { "$set": { "added_status": 2 } }  )
    
    user = db.user_collection.find_one({"_id": ObjectId(request_id)})
    user["_id"] = str(user["_id"])
    return jsonify({"message": "Added Successfully", 'code' : 200, 'data' :user})



def fetch_added_users():
    userId = request.args.get("userId")  # Get userId from request
    if not userId:
        return {"error": "userId is required"}, 400  # Handle missing userId
    try:
        userId = ObjectId(userId)  # Ensure userId is an ObjectId if needed
    except:
        return {"error": "Invalid userId"}, 400  # Handle invalid ObjectId
    # Query to find where userId is either added_by or added_to
    addFriendRequest = db.user_friends_collection.find(
        {
            "added_status": 2,
            "$or": [
                {"added_by":  str(userId)},
                {"added_to":  str(userId)}
            ]
        },
        {"_id": 0, "added_by": 1, "added_to": 1}  # Retrieve both fields
    )
    userIds = list(addFriendRequest)

    # Extract the opposite user IDs
    result_ids = []
    for record in userIds:
        if record["added_by"] ==  str(userId):
            result_ids.append(str(record["added_to"]))  # Get added_to if userId is in added_by
        else:
            result_ids.append(str(record["added_by"]))  # Get added_by if userId is in added_to
        
        
        
    # Convert string IDs to ObjectId
    object_ids = [ObjectId(friend_id) for friend_id in result_ids]
    
    # Fetch all matching documents in a single query
    friends = db.user_collection.find({"_id": {"$in": object_ids}}, {'password': 0,'reported_count' : 0,'initial_login':0 })

    # Convert cursor to a list of dictionaries and handle ObjectId serialization
    friends_list = []
    for friend in list(friends):
        friend["_id"] = str(friend["_id"])  # Convert ObjectId to string
        # print('111111111',friend)
        friends_list.append(friend)
        
    # print('2222222222222222222222',friends_list)

    return jsonify({"message": "Fetched Successfully", 'code': 200, 'data': friends_list})





def update_initial_popup_status():
    userId = request.args.get("userId")  # Get userId from request
    db.user_collection.update_one({ "_id":ObjectId(userId)},{"$set": {"initial_login": 2 }})
    return jsonify({"message": "Update Successfully", 'code' : 200})
    
    
    
    
def fetch_user_profile():
    userId = request.args.get("userId")  # Get userId from request 
    user = db.user_collection.find_one({"_id": ObjectId(userId)},{'password' : 0,'initial_login': 0})
    user["_id"] = str(user["_id"])
    
    return jsonify({"message": "Update Successfully", 'code' : 200, 'data' : user})
    
    
def report_user_id():
    userId = request.args.get("userId")  # Get userId from request
    # print('User ID:', userId)

    # Fetch the user and ensure reported_count is handled properly
    user = db.user_collection.find_one({"_id": ObjectId(userId)}, {'reported_count': 1})

    if not user:
        return jsonify({"message": "User not found", "code": 404})

    reported_count = int(user.get("reported_count", 0))  # Use .get() to handle missing field
    # print('Current reported count:', reported_count)

    # Update the reported count
    db.user_collection.update_one(
        {'_id': ObjectId(userId)},
        {'$set': {'reported_count': reported_count + 1}}
    )
    return jsonify({"message": 'User Reported successfully', 'code' : 200, })
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
def convert_objectid(obj):
    """Recursively convert ObjectId to string in nested dictionaries or lists."""
    if isinstance(obj, ObjectId):  
        return str(obj)  # Convert ObjectId to string
    elif isinstance(obj, list):  
        return [convert_objectid(item) for item in obj]  # Convert items in a list
    elif isinstance(obj, dict):  
        return {key: convert_objectid(value) for key, value in obj.items()}  # Convert values in a dictionary
    return obj  # Return the object if no conversion is needed

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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




























