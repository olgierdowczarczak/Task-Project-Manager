from typing import Any
from auth.auth import get_hashed_password # for demo


# fake db users
static_users: list[dict[Any, Any]] = [
    {
        "id": 1,
        "name": "tester1",
        "password": get_hashed_password(plain_password="testpwd"),
        "is_admin": 1
    },
    {
        "id": 2,
        "name": "tester2",
        "password": get_hashed_password(plain_password="testpwd"),
        "is_admin": 0
    }
]