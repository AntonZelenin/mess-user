from collections import defaultdict

from fastapi import FastAPI, status, Header, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
from result import Ok, Err

from mess_user import repository, helpers
from mess_user.helpers import auth
from mess_user.models.user import User
from mess_user.schemas import UserRegisterData

app = FastAPI()


async def get_current_active_user(x_user_id: str = Header(None)) -> User:
    if x_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    user = repository.get_user(x_user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return user


@app.exception_handler(RequestValidationError)
async def custom_form_validation_error(_, exc):
    reformatted_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)  # nested fields with dot-notation
        reformatted_message[field_string].append(msg)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"errors": reformatted_message}
        ),
    )


@app.post("/api/v1/users")
async def register(user_data: UserRegisterData):
    if repository.username_exists(user_data.username):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'errors': {'username': 'This username is already taken'}},
        )

    user = repository.create_user(user_data.username)

    match helpers.auth.create_user_in_auth(user.id, user.username, user_data.password):
        case Ok(_):
            return {}
        case Err(message):
            repository.delete_user(user.id)
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=message,
            )


@app.get("/api/v1/users/")
async def find_users(username: str, _: User = Depends(get_current_active_user)):
    users = repository.search_users(username)
    return [user.username for user in users]
