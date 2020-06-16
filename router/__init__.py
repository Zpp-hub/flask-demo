from flask import Blueprint, jsonify
from . import user_rt

bp = Blueprint('router', __name__)

def register(app):
    @app.route('/')
    def default_router():
        return jsonify({"statusCode":1,"message":"ok","data":None})

    app.register_blueprint(user_rt.routes, url_prefix='/api/user')
