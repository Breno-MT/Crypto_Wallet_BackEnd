def create_collection_user(mongo_client):
    user_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "title": "User Object Validation",
            "required": [ "_id", "email", "username", "password" ],
            "properties":{
                "_id": {
                    "bsonType": "objectId",
                    "description": "Key defined by collection"
                },
                "email": {
                    "bsonType": "string",
                    "description": "Email must be greater than 6 and less than 127 characters",
                    "minLength": 6,
                    "maxLength": 127,
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
                },
                "username": {
                    "bsonType": "string",
                    "description": "Username must be greater than 4 and less than 24 characters",
                    "minLength": 4,
                    "maxLength": 24
                },
                "password": {
                    "bsonType": "string",
                    "description": "Password must be greater than 12 and less than 64 characters",
                    "minLength": 12,
                    "maxLength": 64
                }
            }
        }
    }

    try:
        mongo_client.create_collection("users")
        print("Collection Users created successfully!")
    
    except Exception as e:
        print(f"Something went wrong! {e}")

    mongo_client.command("collMod", "users", validator=user_validator)
