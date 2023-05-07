import asyncio
from time import time
from base64 import b64encode, b64decode

from common.uuid import complex_uuid, uuid

from .database import DB_USERS
from .groups import Group, get_default_group_id


async def get_user_document_by_filter(flt: dict) -> dict:
    doc = DB_USERS.find_one(flt)
    if doc is None:
        return {}
    if "id" not in doc:
        return {}
    return doc


async def get_user_document_by_username(username: str) -> dict:
    return await get_user_document_by_filter({"username": username})


async def get_user_document_by_email(email: str) -> dict:
    return await get_user_document_by_filter({"email": email})


async def get_user_document_by_id(id: str) -> dict:
    return await get_user_document_by_filter({"id": id})


async def get_user_document_by_token(token: str) -> dict:
    return await get_user_document_by_filter({"tokens": {"$in": [token]}})


class User:
    id: str
    username: str
    password: str
    email: str
    tokens: list[str]
    group: Group
    created: int
    bio: list[str]

    def __init__(self, document: dict) -> None:
        self.oid = document["_id"]
        self.id: str = document["id"]
        self.username: str = document["username"]
        self.password: str = document["password"]
        self.email: str = document["email"]
        self.tokens: list[str] = document["tokens"]
        self.group: str = document["group"]
        self.created: int = document["created"]
        self.bio: list[str] = ">\n<".join(b64decode(document["bio"].encode("utf-8")).decode("utf-8").split("><")).split("\n")

    def dump(self) -> dict:
        return {
            "_id": self.oid,
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "tokens": self.tokens,
            "group": self.group,
            "created": self.created,
            "bio": b64encode("".join(self.bio).encode("utf-8")).decode("utf-8")
        }

    async def pull(self) -> None:
        doc = DB_USERS.find_one({"_id": self.oid})
        if doc is None:
            raise LookupError(
                "The user's document has been deleted from the database, but the object wasn't destroyed"
            )
        self.__init__(doc)

    async def push(self) -> None:
        DB_USERS.find_one_and_replace({"_id": self.oid}, self.dump())

    async def delete(self) -> None:
        DB_USERS.find_one_and_delete({"_id": self.oid})

    async def check_password(self, password: str) -> bool:
        return password == self.password

    async def create_token(self) -> str:
        token = complex_uuid()
        self.tokens.append(token)
        await self.push()
        return token

    async def kill_sessions(self) -> None:
        self.tokens = []
        await self.push()

    @staticmethod
    async def change_password(token, password, new_password) -> None:
        user = await get_user_document_by_token(token)
        if user == {}:
            raise ValueError("Invalid token!")
        user = User(user)
        if not user.check_password(password):
            raise ValueError(
                f"Incorrect password for user by the username {user.username}!"
            )
        user.password = new_password
        user.tokens = []
        await user.push()

    @staticmethod
    async def delete_token(token: str) -> None:
        user = await get_user_document_by_token(token)
        if user == {}:
            raise ValueError("Invalid token!")
        user = User(user)
        user.tokens.remove(token)
        await user.push()

    @classmethod
    async def from_token(cls, token: str):
        user = await get_user_document_by_token(token)
        if user == {}:
            raise ValueError("Invalid token!")
        return cls(user)

    @classmethod
    async def login(cls, username, password):
        user = await get_user_document_by_username(username)
        if user == {}:
            raise ValueError(
                f"User by the username {username} was not found in the database!"
            )
        if password == user["password"]:
            return cls(user)
        raise ValueError(f"Incorrect password for user by the username {username}!")

    @classmethod
    async def register(cls, username: str, password: str, email: str):
        email_check = await get_user_document_by_email(email)
        username_check = await get_user_document_by_username(username)
        if email_check != {} or username_check != {}:
            raise ValueError("The provided username or email is already registered!")
        now = time()
        account = {
            "id": uuid(),
            "username": username,
            "password": password,
            "email": email,
            "tokens": [],
            "group": await get_default_group_id(),
            "created": now,
            "bio": b64encode("".join(f"<h1>Hello There!</h1><p>I am {username}, welcome to my profile!</p><p class='text-muted'>You can change your profile's bio when you're signed in by simply modifying it in the editor and clicking save.</p>").encode("utf-8")).decode("utf-8")
        }
        oid = DB_USERS.insert_one(account)
        oid = oid.inserted_id
        account["_id"] = oid
        return cls(account)
