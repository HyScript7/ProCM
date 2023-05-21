from time import time

from common.projects import GITHUB_USERNAME, get_repository_data
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


async def get_project_document_by_name(name: str) -> dict:
    return await get_project_document_by_filter({"name": name})


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
    uuid: str
    created: float
    url: str
    name: str
    description: str
    license: str
    stars: int
    forks: int

    def __init__(self, document: dict) -> None:
        self.oid = document["_id"]
        self.uuid = document["id"]
        self.created = document["created"]
        self.url = document["url"]
        self.name = document["name"]
        self.description = document["description"]
        self.license = document["license"]
        self.stars = document["stars"]
        self.forks = document["forks"]

    def dump(self) -> dict:
        return {
            "_id": self.oid,
            "id": self.uuid,
            "created": self.created,
            "url": self.url,
            "name": self.name,
            "description": self.description,
            "license": self.license,
            "stars": self.stars,
            "forks": self.forks,
        }

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

    async def update(self) -> None:
        repo = await get_repository_data(self.url.split("/")[-1])
        updated = {
            "name": repo[0],
            "description": repo[1],
            "license": repo[2],
            "stars": repo[3],
            "forks": repo[4],
        }
        self.__init__({**self.dump(), **updated})
        await self.push()

    @classmethod
    async def fetch(cls, name: str):
        proj = await get_project_document_by_name(name)
        if proj == {}:
            raise ValueError(
                f"A project with the name {name} was not found in the database!"
            )
        return cls(proj)

    @classmethod
    async def new(cls, repo_name: str):
        if await get_project_document_by_name(repo_name) != {}:
            raise ValueError("A project with this name is already registered!")
        repo = await get_repository_data(repo_name)
        now = time()
        project_doc = {
            "id": uuid(),
            "created": now,
            "url": f"https://github.com/{GITHUB_USERNAME}/{repo_name}",
            "name": repo[0],
            "description": repo[1],
            "license": repo[2],
            "stars": repo[3],
            "forks": repo[4],
        }
        oid = DB_PROJECTS.insert_one(project_doc)
        oid = oid.inserted_id
        project_doc["_id"] = oid
        return cls(project_doc)
