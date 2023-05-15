from time import time

from common.uuid import uuid

from .database import DB_PROJECTS


async def get_project_document_by_filter(flt: dict) -> dict:
    doc = DB_PROJECTS.find_one(flt)
    if doc is None:
        return {}
    if "id" not in doc:
        return {}
    return doc


async def get_project_document_by_id(uuid: str) -> dict:
    return await get_project_document_by_filter({"id": uuid})


async def get_project_many_documents_by_filter(
    flt: dict, limit: int = 20, page: int = 0
) -> list[dict]:
    docs = DB_PROJECTS.find(flt).sort("created", -1).skip(page * limit).limit(limit)
    if docs is None:
        return []
    documents: list[dict] = []
    for doc in docs:
        if doc is None:
            continue
        if "id" not in doc:
            continue
        documents.append(doc)
    return documents


class Project:
    def __init__(self, document: dict) -> None:
        self.oid = document["_id"]
        self.uuid = document["id"]
        self.created = document["created"]

    def dump(self) -> dict:
        return {"_id": self.oid, "id": self.uuid, "created": self.created}

    async def pull(self) -> None:
        doc = DB_PROJECTS.find_one({"_id": self.oid})
        if doc is None:
            raise LookupError(
                "The project's document has been deleted from the database, but the object wasn't destroyed"
            )
        self.__init__(doc)

    async def push(self) -> None:
        DB_PROJECTS.find_one_and_replace({"_id": self.oid}, self.dump())

    async def delete(self) -> None:
        DB_PROJECTS.find_one_and_delete({"_id": self.oid})

    @classmethod
    async def fetch(cls, uuid: str):
        user = await get_project_document_by_id(uuid)
        if user == {}:
            raise ValueError(
                f"A project with the id {uuid} was not found in the database!"
            )
        return cls(user)

    @classmethod
    async def new(cls):
        now = time()
        project_doc = {"id": uuid(), "created": now}
        oid = DB_PROJECTS.insert_one(project_doc)
        oid = oid.inserted_id
        project_doc["_id"] = oid
        return cls(project_doc)
