# -*- coding: utf-8 -*-
import traceback, json, re
from flask import Blueprint, request, jsonify, g
from middleware.oauth import oauth
from middleware.routerDecorator import auth_middlware
import controller.userProfileController as upc
import pydash as _

routes = Blueprint("user", __name__)

@routes.route("/info", methods=["GET"])
@auth_middlware
def get_user():
    result = {"statusCode": 1, "message": "ok", "data": None}
    try:
        if g.user is not None:
            result["data"] = g.user
        else:
            result["code"] = -1
            result["message"] = "token failed"
    except Exception as e:
        traceback.print_exc()
        result["code"] = -1
        result["message"] = str(e)
    return jsonify(result)



#
#
# @routes.route("/logout", methods=["POST"])
# def get_logout():
#     result = {"message": "", "code": 0, "data": None, "success": False}
#     try:
#         if "Authorization" in request.headers and request.headers["Authorization"]:
#             oauth2 = oauth(request.headers["Authorization"], "", "")
#             result = oauth2.logout()
#
#     except Exception as e:
#         traceback.print_exc()
#         result["code"] = -1
#         result["message"] = "internal error"
#
#     return jsonify(result)
#
#
# @routes.route("/list", methods=["GET"])
# def get_user_list():
#     result = {"message": "", "statusCode": 0, "data": None, "success": False}
#     try:
#         offset = 0
#         if "offset" in request.args:
#             offset = int(request.args["offset"])
#         limit = 10
#         if "limit" in request.args:
#             limit = int(request.args["limit"])
#         query = ""
#         if 'query' in request.args.keys():
#             query = request.args.get('query')
#         oauth2 = oauth("", "", "")
#         res = oauth2.getUserList(offset, limit)
#
#         # tp_data = res['data']
#         # re_query = re.compile(query)
#         # if query:
#         #     tp_data['rows'] = _.collections.filter_(tp_data['rows'], lambda x: re_query.match(x['username']))
#         #     tp_data['total'] = len(tp_data['rows'])
#         result["success"] = res["success"]
#         result["data"] = res["data"]
#         result["message"] = res["message"]
#         result["statusCode"] = res["code"]
#
#     except Exception as e:
#         traceback.print_exc()
#         result["statusCode"] = -1
#         result["message"] = e.message
#
#     return jsonify(result)
#
#
# @routes.route("/add", methods=["POST"])
# @auth_middlware
# def add_user():
#     result = {"statusCode": 1, "message": "ok", "data": None}
#
#     try:
#         content = request.json
#         result = upc.add_user(content)
#
#     except Exception as e:
#         traceback.print_exc()
#         result["statusCode"] = -1
#         result["message"] = "internal error"
#
#     return jsonify(result)
#
#
# """
# {
#     "data": {
#         "avatar": null,
#         "createTime": "2019-08-29T13:55:42.000+0800",
#         "email": "",
#         "gender": "M",
#         "id": 100139,
#         "lastLoginIp": "",
#         "nickName": null,
#         "phone": "13221122344",
#         "realName": "",
#         "roles": [
#             "admin"
#         ],
#         "status": 1,
#         "statusJson": null,
#         "systemCode": 32,
#         "updateTime": "2019-08-29T14:58:20.000+0800",
#         "username": "test123",
#         "version": 11
#     },
#     "message": "ok",
#     "statusCode": 1
# }
#
# """
#
#
# @routes.route("/info/<id>", methods=["GET"])
# @auth_middlware
# def get_user_info_by_id(id):
#     result = {"statusCode": 1, "message": "ok", "data": None}
#
#     try:
#         if "id" in request.args.keys():
#             id = request.args.get["id"]
#         oauth2 = oauth("", "", "")
#         ret = oauth2.getUserInfoById(id)
#         if ret["success"]:
#             tp_user = ret["data"]
#             user_profile = upc.findUserProfileByLinkID({"link_id": str(tp_user["id"])})
#             if user_profile is not None:
#                 tp_user = _.assign(tp_user, user_profile)
#             else:
#                 tp_user["roles"] = []
#             result["data"] = tp_user
#
#     except Exception as e:
#         traceback.print_exc()
#         result["statusCode"] = -1
#         result["message"] = "internal error"
#
#     return jsonify(result)
#
#
# @routes.route("/update", methods=["PUT", "POST"])
# @auth_middlware
# def update_user():
#     result = {"statusCode": 1, "message": "ok", "data": None}
#     try:
#         content = request.json
#
#         strgender = "M"
#         if "gender" in content:
#             strgender = content["gender"]
#         strphone = ""
#         if "phone" in content:
#             strphone = content["phone"]
#         stremail = ""
#         if "email" in content:
#             stremail = content["email"]
#         strrealname = ""
#         if "realName" in content:
#             strrealname = content["realName"]
#
#         oauth2 = oauth("", content["username"], "")
#         tp_content = oauth2.updateUser(strgender, strphone, stremail, strrealname, content["id"])
#         if tp_content["success"]:
#             ret_roles = upc.update_user_profile({"link_id": str(tp_content["data"]["id"])},
#                                                 {"$set": {"roles": content["roles"]}})
#         result["message"] = tp_content["message"]
#         result["data"] = tp_content["data"]
#
#     except Exception as e:
#         traceback.print_exc()
#         result["statusCode"] = -1
#         result["message"] = "internal error"
#
#     return jsonify(result)
#
# @routes.route("/captcha", methods=["GET"])
# def get_captcha():
#     result = {"statusCode": 1, "message": "ok", "data": None}
#     try:
#         result['data']=upc.getCaptchaFromTools()
#     except Exception as ex:
#         traceback.print_exc()
#         result["statusCode"] = -1
#         result["message"] = "internal error"
#     return jsonify(result)
