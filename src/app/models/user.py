def create_collection_user(mongo_client):
    user_validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": [ 
            "_id",
            "username",
            "password",
        ],
        }
    }

    try:
        mongo_client.create_collection("user")
        print("Collection Users created successfully!")
    
    except Exception as e:
        print(f"Something went wrong! {e}")

    mongo_client.command("collMod", "user", validator=user_validator)
