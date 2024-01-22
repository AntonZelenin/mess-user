import requests
from result import Result, Ok, Err

from mess_users import constants


def create_user_in_auth(user_id: str, username: str, password: str) -> Result[bool, str]:
    try:
        res = requests.post(
            f"{constants.AUTH_URL}/api/v1/users",
            json={
                "user_id": user_id,
                "username": username,
                "password": password,
            },
        )
        res.raise_for_status()

        return Ok(True)
    except requests.HTTPError as e:
        return Err(e.response.text)
    except Exception as e:
        return Err(str(e))
