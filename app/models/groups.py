from time import time

from common.uuid import uuid

from .database import DB_GROUPS


async def get_group_document_by_filter(flt: dict) -> dict:
    doc = DB_GROUPS.find_one(flt)
    if doc is None:
        return {}
    if "id" not in doc:
        return {}
    return doc


async def get_group_document_by_id(id: str) -> dict:
    return await get_group_document_by_filter({"id": id})


async def get_group_document_by_name(name: str) -> dict:
    return await get_group_document_by_filter({"name": name})


class Permissions:
    permissions: dict[dict]

    def __init__(self, document: dict) -> None:
        self.permissions = document

    def action(self, action: str) -> list[bool]:
        if action not in self.permissions:
            raise NameError("Unknown action requested of the Permission Wrapper")
        return self.permissions[action]

    def get(self, action: str, resource: str) -> bool:
        action: dict = self.action(action)
        if resource not in action:
            raise NameError("Unknown resource requested of the Permission Wrapper")
        return action[resource]

    def set(self, action: str, resource: str, value: bool) -> None:
        if resource not in self.action(action):
            raise NameError("Unknown resource requested of the Permission Wrapper")
        self.permissions[action][resource] = value

    def dump(self) -> dict:
        return self.permissions

    @classmethod
    def default(cls):
        default_resources = {
            "comment": False,
            "comment.own": True,  # This is used to distinct comment admin from own comment management
            "post": False,
            "page": False,
            "project": False,
            "admin": False,
        }
        return cls(
            {
                "create": {**default_resources, "comment": True},
                "delete": default_resources,
                "manage": default_resources,
                "view": {
                    **default_resources,
                    "comment": True,
                    "post": True,
                    "project": True,
                    "page": True,
                },
            }
        )


class Group:
    id: str
    name: str
    permissions: Permissions
    created: int

    def __init__(self, document: dict) -> None:
        self.oid = document["_id"]
        self.id: str = document["id"]
        self.name: str = document["name"]
        self.permissions: Permissions = Permissions(document["permissions"])
        self.created: int = document["created"]

    def dump(self) -> dict:
        return {
            "_id": self.oid,
            "id": self.id,
            "name": self.name,
            "permissions": self.permissions.dump(),
            "created": self.created,
        }

    async def pull(self) -> None:
        doc = DB_GROUPS.find_one({"_id": self.oid})
        if doc is None:
            raise LookupError(
                "The group's document has been deleted from the database, but the object wasn't destroyed"
            )
        self.__init__(doc)

    async def push(self) -> None:
        DB_GROUPS.find_one_and_replace({"_id": self.oid}, self.dump())

    async def delete(self) -> None:
        DB_GROUPS.find_one_and_delete({"_id": self.oid})

    @classmethod
    async def from_id(cls, id: str):
        group = await get_group_document_by_id(id)
        if group == {}:
            raise ValueError(f"A group with the ID {id} does not exist!")
        return cls(group)

    @classmethod
    async def from_name(cls, name: str):
        group = await get_group_document_by_name(name)
        if group == {}:
            raise ValueError(f"A group with the name {name} does not exist!")
        return cls(group)

    @classmethod
    async def create(cls, name: str, overrides: dict):
        name_check = await get_group_document_by_name(name)
        if name_check != {}:
            raise ValueError(f"The provided name '{name}' is already used by a group!")
        now = time()
        group: dict = {
            "id": uuid(),
            "name": name,
            "permissions": {**Permissions.default().dump(), **overrides},
            "created": now,
        }
        oid = DB_GROUPS.insert_one(group)
        oid = oid.inserted_id
        group["_id"] = oid
        return cls(group)


async def get_default_group_id() -> str:
    try:
        g = await Group.from_name("default")
        return g.id
    except ValueError:
        g = await Group.create("default", {})
    return g.id


async def get_admin_group_id() -> str:
    try:
        g = await Group.from_name("admin")
        return g.id
    except ValueError:
        default_resources = {
            "comment": True,
            "comment.own": True,
            "post": True,
            "page": True,
            "project": True,
            "admin": True,
        }
        resources = {
            "create": default_resources,
            "delete": default_resources,
            "manage": default_resources,
            "view": default_resources,
        }
        g = await Group.create("admin", resources)
    return g.id
