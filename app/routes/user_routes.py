from flask import Blueprint, jsonify, request
from app.services.user_service import login,creat_room, create_user, get_users,get_rooms_list,search_user_name,get_rooms_chats
user_bp = Blueprint('user_bp', __name__)

# GET all users
@user_bp.route('/', methods=['GET'])
def get_all_users():
    return jsonify(get_users())


# get rooms data on particular id


# GET a single user by ID
# @user_bp.route('/<int:user_id>', methods=['GET'])
# def get_single_user(user_id):
#     return jsonify(get_user(user_id))

# Sign-up POST API
@user_bp.route('/sign-up', methods=['POST'])
def add_user():
    data = request.json
    return create_user(data)

# Login Post API
@user_bp.route('/log-in', methods=['POST'])
def login_user():
    data = request.json
    return login(data)

# Get room on specific user id
@user_bp.route('/room-list', methods=['GET'])
def get_room_data():
    return get_rooms_list()

#get specific room chat
@user_bp.route('/get-room-chat', methods=['GET'])
def get_room_chat():
    return get_rooms_chats()

#creat user room
@user_bp.route('/creat-room', methods=['POST'])
def creat_new_room():
    data = request.json
    return creat_room(data)

#get specific room chat
@user_bp.route('/search-user', methods=['GET'])
def search_user():
    return search_user_name()
# Login Post API
# @user_bp.route('/log-in', methods=['POST'])
# def forget_email():
#     data = request.json
#     return forgetEmail(data)

# PUT (Update) a user
# @user_bp.route('/<int:user_id>', methods=['PUT'])
# def modify_user(user_id):
#     data = request.json
#     return jsonify(update_user(user_id, data))

# DELETE a user
# @user_bp.route('/<int:user_id>', methods=['DELETE'])
# def remove_user(user_id):
#     return jsonify(delete_user(user_id))
