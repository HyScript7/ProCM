from time import time

from common.uuid import uuid

from .database import DB_POSTS
from .user import User


async def get_post_document_by_filter(flt: dict) -> dict:
    doc = DB_POSTS.find_one(flt)
    if doc is None:
        return {}
    if "id" not in doc:
        return {}
    return doc


async def get_post_document_by_id(uuid: str) -> dict:
    return await get_post_document_by_filter({"id": uuid})


async def get_post_document_by_title(title: str) -> dict:
    return await get_post_document_by_filter({"title": title})


async def get_post_many_documents_by_filter(
    flt: dict, limit: int = 20, page: int = 0
) -> list[dict]:
    docs = DB_POSTS.find(flt).sort("created", -1).skip(page * limit).limit(limit)
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


async def get_post_many_documents_by_tags(
    tags: list[str], limit_override: int = 20, page: int = 0
) -> list[dict]:
    return await get_post_many_documents_by_filter(
        {"tags": {"$in": tags}}, limit_override, page
    )


async def get_post_many_documents_by_author(
    author: str, limit_override: int = 20, page: int = 0
) -> list[dict]:
    return await get_post_many_documents_by_filter(
        {"author": author}, limit_override, page
    )


async def get_post_many_documents_by_title(
    title: str, limit_override: int = 20, page: int = 0
) -> list[dict]:
    return await get_post_many_documents_by_filter(
        {"title": {"$regex": f".*{title}.*"}}, limit_override, page
    )


class Post:
    id: str
    author_id: str
    title: str
    tags: list[str]
    content: str
    created: int

    def __init__(self, document: dict) -> None:
        self.oid = document["_id"]
        self.id: str = document["id"]
        self.author_id: str = document["author"]
        self.title: str = document["title"]
        self.tags: list[str] = document["tags"]
        self.content: str = document["content"]
        self.created: int = document["created"]

    def dump(self) -> dict:
        return {
            "_id": self.oid,
            "id": self.id,
            "author": self.author_id,
            "title": self.title,
            "tags": self.tags,
            "content": self.content,
            "created": self.created,
        }

    async def pull(self) -> None:
        doc = DB_POSTS.find_one({"_id": self.oid})
        if doc is None:
            raise LookupError(
                "The post's document has been deleted from the database, but the object wasn't destroyed"
            )
        self.__init__(doc)

    async def push(self) -> None:
        DB_POSTS.find_one_and_replace({"_id": self.oid}, self.dump())

    async def delete(self) -> None:
        DB_POSTS.find_one_and_delete({"_id": self.oid})

    @classmethod
    async def fetch(cls, uuid: str):
        user = await get_post_document_by_id(uuid)
        if user == {}:
            raise ValueError(
                f"A post with the id {uuid} was not found in the database!"
            )
        return cls(user)

    @classmethod
    async def new(cls, author: User, title: str, tags: list[str], content: str):
        now = time()
        comment = {
            "id": uuid(),
            "author": author.id,
            "title": title,
            "tags": tags,
            "content": content,
            "created": now,
        }
        oid = DB_POSTS.insert_one(comment)
        oid = oid.inserted_id
        comment["_id"] = oid
        return cls(comment)
