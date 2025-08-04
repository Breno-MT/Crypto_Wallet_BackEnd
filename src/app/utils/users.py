import bcrypt
from bson import json_util
from flask.wrappers import Response
import os
from src.app import mongo_client
from src.app.utils.token_jwt import create_token 

def register_user_db(user_body):
    try:
        is_user_existent = get_user_by_email_or_username(user_body)

        if is_user_existent:
            return Response(
                response=json_util.dumps({"error": "User already exists in the database."}),
                status=409,
                mimetype="application/json"
            )

        user_body["password"] = encrypt_user_password(user_body["password"])

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

def login_user(user_body): 
    is_user_valid = validate_user_login(user_body)

    if not is_user_valid:
        return Response(
            response=json_util.dumps({"error": "Invalid credentials."}),
            status=401,
            mimetype="application/json"
        )

    del user_body["password"]

    return Response(
        response=json_util.dumps({"token": create_token(user_body)}),
        status=200,
        mimetype="application/json"
    )

def validate_user_login(user_body):
    get_user = mongo_client.users.find_one({"email": user_body["email"]})

    if not get_user:
        return False

    is_user_valid = bcrypt.checkpw(user_body["password"].encode("utf-8"), get_user.get("password"))

    return is_user_valid

def validate_token_user(token): pass

def encrypt_user_password(password):
    return bcrypt.hashpw(
                password=password,
                salt=bcrypt.gensalt(10)
            )

def get_user_by_email_or_username(user_body):
    is_email_created = mongo_client.users.find_one({"email": user_body["email"]})
    is_username_created = mongo_client.users.find_one({"username": user_body["username"]})

    if is_email_created or is_username_created:
        return is_email_created or is_username_created
    
    return None
