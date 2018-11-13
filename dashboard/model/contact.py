from dashboard.model import db
from bson.objectid import ObjectId


def search_by_contactname(user):
    query = {'name': user['name']}
    matching_user = db['users'].find(query)
    if matching_user.count() > 0:
        return matching_user.next()
    else:
        return None


def add_contact(user):
    existing_user = search_by_contactname(user)
    if existing_user is not None:
        return False
    else:
        db['contacts'].insert_one(user)
    return True

