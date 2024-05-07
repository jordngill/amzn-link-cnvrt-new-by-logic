# (c) @AmznUser | Jordan Gill

import datetime
from pymongo import MongoClient

class Database:
    def __init__(self, uri, database_name):
        self._client = MongoClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, user_id: int):
        return {
            "id": int(user_id),
            "join_date": datetime.date.today().isoformat(),
            "notif": True,
            "usertype": "",
            "footer_channel_username": None,
            "ban_status": {
                "is_banned": False,
                "ban_duration": 0,
                "banned_on": datetime.date.max.isoformat(),
                "ban_reason": "",
            },
            "channel_id": [],
            "amazon_tag": [],
            "session_string": []
        }

    def add_user(self, user_id: int):
        user = self.new_user(user_id)
        self.col.insert_one(user)

    def is_user_exist(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return True if user else False

    def total_users_count(self):
        count = self.col.count_documents({})
        return count

    def get_user(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user

    def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    def delete_user(self, user_id: int):
        self.col.delete_many({"id": int(user_id)})

    def remove_ban(self, user_id: int):
        ban_status = {
            "is_banned": False,
            "ban_duration": 0,
            "banned_on": datetime.date.max.isoformat(),
            "ban_reason": "",
        }
        self.col.update_one({"id": int(user_id)}, {"$set": {"ban_status": ban_status}})

    def ban_user(self, user_id: int, ban_duration, ban_reason):
        ban_status = {
            "is_banned": True,
            "ban_duration": ban_duration,
            "banned_on": datetime.date.today().isoformat(),
            "ban_reason": ban_reason,
        }
        self.col.update_one({"id": int(user_id)}, {"$set": {"ban_status": ban_status}})

    def get_ban_status(self, user_id: int):
        default = {
            "is_banned": False,
            "ban_duration": 0,
            "banned_on": datetime.date.max.isoformat(),
            "ban_reason": "",
        }
        user = self.col.find_one({"id": int(user_id)})
        return user.get("ban_status", default)

    def get_all_banned_users(self):
        banned_users = self.col.find({"ban_status.is_banned": True})
        return banned_users

    def set_notif(self, user_id: int, notif):
        self.col.update_one({"id": int(user_id)}, {"$set": {"notif": notif}})

    def get_notif(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("notif", False)

    def get_all_notif_user(self):
        notif_users = self.col.find({"notif": True})
        return notif_users

    def total_notif_users_count(self):
        count = self.col.count_documents({"notif": True})
        return count

    def add_string_session(self, user_id: int, str_session):
        self.col.update_one({"id": int(user_id)}, {"$push": {"session_string": str_session}})

    def get_string_session(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("session_string")[-1] if len(user.get("session_string", [])) > 0 else None

    def remove_string_session(self, user_id: int, str_session):
        self.col.update_one({"id": int(user_id)}, {"$pull": {"session_string": str_session}})

    def add_forward_channel(self, user_id: int, channel):
        self.col.update_one({"id": int(user_id)}, {"$push": {"channel_id": channel}})

    def get_forward_channel(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("channel_id")[-1] if len(user.get("channel_id", [])) > 0 else None

    def get_all_forward_channel(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("channel_id", [])

    def remove_forward_channel(self, user_id: int, channel):
        self.col.update_one({"id": int(user_id)}, {"$pull": {"channel_id": channel}})

    def add_copy_channel(self, user_id: int, channel):
        self.col.update_one({"id": int(user_id)}, {"$push": {"copy_channel": channel}})

    def get_copy_channel(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("copy_channel")[-1] if len(user.get("copy_channel", [])) > 0 else None

    def remove_copy_channel(self, user_id: int, channel):
        self.col.update_one({"id": int(user_id)}, {"$pull": {"copy_channel": channel}})
    def reset_all(self, user_id: int):
        work = self.col.find_one_and_delete({"id": int(user_id)})
        if work:
            return True
        else:
            return False

    def get_all_copy_channel(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("copy_channel", [])

    def add_amazon_tag(self, user_id: int, amazon_tag):
        self.col.update_one({"id": int(user_id)}, {"$push": {"amazon_tag": amazon_tag}})

    def get_amazon_tag(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("amazon_tag")[-1] if len(user.get("amazon_tag", [])) > 0 else None
    
    def remove_amazon_tag(self, user_id: int, channel):
        self.col.update_one({"id": int(user_id)}, {"$pull": {"amazon_tag": channel}})

    def get_all_logined_users(self):
        query = {
            "$and": [
                {"session_string.0": {"$exists": True}},
                {"copy_channel.0": {"$exists": True}},
            ]
        }
        users = self.col.find(query)
        return users
    
    def set_tagauthuser(self, user_id: int):
        self.col.update_one({"id": int(user_id)}, {"$set": {"tagauth": "authorised"}})

    def get_tagauthuser(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("tagauth", "")

    def remove_tagauthuser(self, user_id: int):
        self.col.update_one({"id": int(user_id)}, {"$set": {"tagauth": ""}})

    def set_forwardauthuser(self, user_id: int):
        self.col.update_one({"id": int(user_id)}, {"$set": {"forwardauth": "authorised"}})

    def get_forwardauthuser(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("forwardauth", "")

    def remove_forwardauthuser(self, user_id: int):
        self.col.update_one({"id": int(user_id)}, {"$set": {"forwardauth": ""}})

    def add_custom_footer_channel(self, user_id: int, username):
        self.col.update_one({"id": int(user_id)}, {"$set": {"footer_channel_username": username}})

    def get_custom_footer_channel(self, user_id: int):
        user = self.col.find_one({"id": int(user_id)})
        return user.get("footer_channel_username", None)

    def remove_custom_footer_channel(self, user_id: int):
        self.col.update_one({"id": int(user_id)}, {"$set": {"footer_channel_username": None}})
