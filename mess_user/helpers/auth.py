import requests
from result import Result, Ok, Err

from mess_user import constants


def create_user_in_auth(user_id: str, username: str, password: str) -> Result[bool, dict]:
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
        if e.response.status_code == 400:
            return Err(e.response.json())
        return Err({
            'errors': {
                'auth_error': [e.response],
            },
        })
    except Exception as e:
        return Err({
            'errors': {
                'exception': [str(e)],
            },
        })
