import jwt
import os
from datetime import datetime, timedelta, timezone

def create_token(payload):
    payload.update({
        "exp": datetime.now(timezone.utc) + timedelta(hours=4)
    })

    token_user = jwt.encode(payload,
                            os.getenv("SECRET_KEY"),
                            algorithm="HS256"
    )

    return token_user