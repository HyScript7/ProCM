from hashlib import sha256
from uuid import uuid1, uuid3, uuid4, uuid5

from .configuration import PASSWORD_SALT


def uuid():
    return str(uuid3(uuid1(), uuid4().hex).hex)


def complex_uuid():
    return str(uuid5(uuid3(uuid1(), uuid4().hex), uuid4().hex).hex)


def hash_password(password: str) -> str:
    return sha256(
        f"{PASSWORD_SALT}{password}{PASSWORD_SALT+password[::-1]}".encode()
    ).hexdigest()
