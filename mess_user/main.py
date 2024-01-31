from collections import defaultdict
from typing import Annotated

from fastapi import FastAPI, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from result import Ok, Err
from sqlalchemy.ext.asyncio import AsyncSession

from mess_user import repository, helpers
from mess_user.db import get_db_session
from mess_user.helpers import user
from mess_user.models.user import User
from mess_user.schemas import UserRegisterData

app = FastAPI()

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]


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


@app.post("/api/user/v1/users")
async def register(user_data: UserRegisterData, session: DBSessionDep):
    if await repository.username_exists(session, user_data.username):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={'errors': {'username': 'This username is already taken'}},
        )

    user_ = await repository.create_user(session, user_data.username)

    try:
        match helpers.user.create_user_in_auth(user_.id, user_.username, user_data.password):
            case Ok(_):
                return {}
            case Err(message):
                # todo it always returns 400, even if auth is down and it should be 500
                await repository.delete_user(session, user_.id)
                return JSONResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    content=message,
                )
    except Exception as e:
        await repository.delete_user(session, user_.id)
        raise e


@app.get("/api/user/v1/users")
async def find_users(username: str, session: DBSessionDep, _: User = Depends(helpers.user.get_current_active_user)):
    users = await repository.search_users(session, username)
    return [u.username for u in users]
