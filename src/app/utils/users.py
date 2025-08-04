import bcrypt
from bson import json_util
from flask.wrappers import Response
import os
from src.app import mongo_client
from src.app.config import app_config

def register_user_db(user_body):
    try:
        is_email_already_created = mongo_client.users.find_one({"email": user_body["email"]})
        is_username_already_created = mongo_client.users.find_one({"username": user_body["username"]})

        if is_email_already_created or is_username_already_created:
            return Response(
                response=json_util.dumps({"error": "User already exists in the database."}),
                status=409,
                mimetype="application/json"
            )

        user_body["password"] = bcrypt.hashpw(
            password=user_body["password"].encode("utf-8"),
            salt=bcrypt.gensalt(10)
        )

        mongo_client.users.insert_one(user_body)
        user_body.pop("password")

        return Response(
            response=json_util.dumps({"records": user_body}),
            status=200,
            mimetype="application/json"
        )

    except Exception as e:
        return Response(
            response=json_util.dumps({"error": f"{e}"}),
            status=400,
            mimetype="application/json"
        )

def check_password_user(user_body): pass

def login_user(user_body): pass

def validate_token_user(token): pass
