from flask import Blueprint, jsonify, request
from app.services.user_service import report_user_id,login,creat_room,fetch_added_users,profile, fetch_user_profile,  update_initial_popup_status,confirm_pending_req, create_user,creat_friends,get_users,get_rooms_list,search_user_name,get_rooms_chats
user_bp = Blueprint('user_bp', __name__)

# GET all users
@user_bp.route('/fetch-all-users', methods=['GET'])
def get_all_users():
    return get_users()


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

#get specific room chat
@user_bp.route('/profile', methods=['GET'])
def get_profile():
    return profile()

#Get selected initial users id for adding as a friend
@user_bp.route('/add-friend', methods=['POST'])
def creat_new_friends():
    data = request.json
    return creat_friends(data)

# confirm pending request
@user_bp.route('/confirm-request', methods=['POST'])
def confirm_request():
    data = request.json
    return confirm_pending_req(data)

#fetch added friend list
@user_bp.route('/added-users-list', methods=['GET'])
def get_added_users_list():
    return fetch_added_users()

# update initial login status
@user_bp.route('/update-initial-status', methods=['GET'])
def update_initial_status():
    return update_initial_popup_status()


#fetch particular user data 
@user_bp.route('/get-single-user-profile-data', methods=['GET'])
def get_profile_data():
    return fetch_user_profile()

#report user id 
@user_bp.route('/report-user', methods=['GET'])
def report_user():
    return report_user_id()