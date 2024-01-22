from fastapi import FastAPI, HTTPException, status
from result import Ok, Err

from mess_users import repository, helpers
from mess_users.helpers import auth
from mess_users.schemas import UserRegisterData

app = FastAPI()


@app.post("/api/v1/users")
async def register(user_data: UserRegisterData):
    if repository.username_exists(user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken",
        )
    user = repository.create_user(user_data.username)

    match helpers.auth.create_user_in_auth(user.id, user.username, user_data.password):
        case Ok(_):
            return {"success": "true"}
        case Err(message):
            repository.delete_user(user.id)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=message,
            )
