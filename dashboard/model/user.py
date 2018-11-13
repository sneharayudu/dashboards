from dashboard.model import db
from bson.objectid import ObjectId


def search_by_username(username):

    query = {'username': username}
    matching_user = db['users'].find(query)
    if matching_user.count() > 0:
        return matching_user.next()
    else:
        return None

def search_by_user_id(user_id):
    query = {'_id': ObjectId(user_id)}
    matching_user = db['users'].find(query)
    if matching_user.count() > 0:
        return matching_user.next()
    else:
        return None



def signup_user(name, username, password):
    existing_user = search_by_username(username)
    if existing_user is not None:
        return False
    else:
        user = {
         'name': name,
         'username': username,
         'password': password,

    }
    db['users'].insert_one(user)
    return True


def authenticate(username, password):
    user = search_by_username(username)

    if user is None:

        return False

    if user['password'] == password:

        return True
    else:

        return False