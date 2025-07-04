from bson import json_util
from flask import Blueprint, request
from flask.wrappers import Response
from src.app import mongo_client

user = Blueprint("user", __name__, url_prefix="/user")

@user.route("/", methods=["GET"])
def get_users():
    try:
        all_users = mongo_client.users.find()

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
def create_user():
    """
    This URL expects "email, password" in order to create the user.
    """
    try:
        new_user = request.get_json()

        mongo_client.users.insert_one(new_user)

        return Response(
            response=json_util.dumps({"records": new_user}),
            status=201,
            mimetype="application/json"
        )

    except Exception as _:
        
        return Response(
            response=json_util.dumps({"error": f"Something happened! Check your json body!"}),
            status=403,
            mimetype="application/json"
        )
