# -*- coding: utf-8 -*-
from pymongo import MongoClient
from ConfigHelper.ConfigHelper import ConfigHelper
# from middleware.oauth import oauth
import requests, uuid
import redis

config = ConfigHelper()
client = MongoClient(host=config.ConfigSectionMapCompatiable("OP_MONGO_DB_CONFIG", "MONGO_HOST"),
                     port=int(config.ConfigSectionMapCompatiable("OP_MONGO_DB_CONFIG", "MONGO_PORT")))
db = client["op_db"]

redis_server = redis.Redis(host=config.ConfigSectionMap("REDIS_CONFIG")["SERVER"],
                           port=config.ConfigSectionMap("REDIS_CONFIG")["PORT"],
                           db=2)


def getCaptchaFromTools():
    tools_server_uri = config.ConfigSectionMapCompatiable("TOOLS_CONFIG", "TOOLS_FLASK_SERVER_URI")
    res = requests.get(tools_server_uri + "/api/image/captcha", headers={"Content-Type": "application/json"})
    rdata = res.json()
    if rdata["statusCode"] == 1:
        ticket = str(uuid.uuid4())
        redis_server.setex(ticket, 60 * 3, rdata["data"]["code"])
        rdata["data"]["ticket"] = ticket
        del rdata["data"]["code"]
        return rdata["data"]
    else:
        return None


def verifyTicketAndCode(ticket, code):
    rst=redis_server.get(ticket)
    if rst is not None:
        if rst.decode('utf-8')==str(code):
            return True
    return False

def findUserProfileByLinkID(filter):
    col = db["UserProfile"]
    item = col.find_one(filter)
    if item is not None:
        del item["_id"]
    return item

def read_userprofile_from_mongo(input_filter):
    col = db['UserProfile']
    return_result = {}
    result = []
    for item in col.find(input_filter):
        del item["_id"]
        result.append(item)
    return_result["rows"] = result

    return return_result

def insert_user_profile(content):
    col = db["UserProfile"]
    result = col.insert_one(content)
    # return Objectid
    return str(result.inserted_id)


def update_user_profile(filter, content):
    col = db["UserProfile"]
    result = col.update(filter, content, multi=False, upsert=True)
    # return Objectid
    return result


# def add_user(content):
#     result = {"statusCode": 1, "message": "ok", "data": None}
#
#     add_value = {}
#     oauth2 = oauth("", content["username"], content["password"])
#     res = oauth2.getUserInfo()
#
#     if res["success"] is False:
#         str_gender = "M"
#         if "str_gender" in content:
#             str_gender = content["gender"]
#         str_phone = ""
#         if "phone" in content:
#             str_phone = content["phone"]
#         str_email = ""
#         if "email" in content:
#             str_email = content["email"]
#         str_realname = ""
#         if "realname" in content:
#             str_realname = content["realname"]
#         add_info = oauth2.addUser(str_gender, str_phone, str_email, str_realname)
#         if add_info["success"]:
#             add_value["link_id"] = str(add_info["data"]["id"])
#             add_value["roles"] = content["roles"]
#             role_id = insert_user_profile(add_value)
#             result["data"] = add_info["data"]["id"]
#     else:
#         # 给共享用户保存权限
#         add_value["link_id"] = str(res["data"]["id"])
#         add_value["roles"] = content["roles"]
#         insert_user_profile(add_value)
#
#     return result
