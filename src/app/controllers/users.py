from bson import json_util
from flask import Blueprint, request
from flask.wrappers import Response
from src.app import mongo_client
from src.app.utils.users import create_user_db, login_user, validate_token_user

user = Blueprint("user", __name__, url_prefix="/user")

@user.route("/", methods=["GET"])
def get_users_endpoint():
    try:
        all_users = mongo_client.users.find({}, {"password": False})

        return Response(
            response=json_util.dumps({"records": all_users}),
            status=200,
            mimetype="application/json"
        )
    
    except Exception as e:
        return Response(
            response=json_util.dumps({"error": f"Something happened! More info: {e}"}),
            status=404,
            mimetype="application/json"
        )

@user.route("/create_user", methods=["POST"])
def create_user_endpoint():
    # TODO: transform create_user into register_user
    """
    This URL expects "username, email, password" in order to create the user.
    """
    try:
        response = create_user_db(request.get_json())
        return response

    except Exception as e:
        return Response(
            response=json_util.dumps({"error": f"Something happened! Check your json body! {e}"}),
            status=403,
            mimetype="application/json"
        )

@user.route("/login", methods=["POST"])
def login_user_endpoint():
    """
    The user has to login using username/email and password
    """
    try:
        response = login_user(request.get_json())
        return response

    except Exception as e:
        return Response(
            response=json_util.dumps({"error": f"Oops! Something happened! {e}"}),
            status=403,
            mimetype="application/json"
        )

@user.route("/validate_token", methods=["GET"])
def validate_token_endpoint():
    validate_token_user()
    return Response(
        response=json_util.dumps({"message": "Token is valid (W.I.P)"}),
        status=200,
        mimetype="application/json"
    )
