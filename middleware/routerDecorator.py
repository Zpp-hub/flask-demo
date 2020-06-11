# -*- coding: utf-8 -*-
from functools import wraps
from flask import Flask, request, g
from middleware.oauth import oauth
import controller.userProfileController as user
import pydash as _

def auth_middlware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # print('--------auth------------')
        # print(request.headers['Authorization'])
        result = {'message': 'token not exists', 'statusCode': -1, 'data': None}
        if 'Authorization' in request.headers and request.headers['Authorization']:
            tp_tokens=request.headers['Authorization'].split(' ')

            if len(tp_tokens)!=2 and tp_tokens[0] !="Bearer":
                return result,401
            token=tp_tokens[1]
            oauth2 = oauth(token, '', '')
            ret = oauth2.checkToken()
            if ret is not None:
                # 检查当前用户是否为该实验的负责人或者被分享用户
                tp_profile = user.findUserProfileByLinkID({"link_id": str(ret['id'])})
                tp_user = _.assign(ret, tp_profile)
                g.user = tp_user
                result = func(*args, **kwargs)
                return result
            else:
                return result, 401
        else:
            return result, 401

    return wrapper
