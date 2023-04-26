from time import time

from common.uuid import uuid

from . import Post, User
from .database import DB_COMMENTS


async def get_comment_document_by_filter(flt: dict) -> dict:
    doc = DB_COMMENTS.find_one(flt)
    if doc is None:
        return {}
    if "id" not in doc:
        return {}
    return doc


async def get_comment_document_by_id(uuid: str) -> dict:
    return await get_comment_document_by_filter({"id": uuid})


async def get_comment_document_by_author(author_id: str) -> dict:
    return await get_comment_document_by_filter({"author": author_id})


async def get_comment_document_by_parent(parent_id: str) -> dict:
    return await get_comment_document_by_filter({"for": parent_id})


async def get_comment_many_documents_by_filter(flt: dict) -> dict:
    docs = DB_COMMENTS.find(flt)
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


async def get_comment_many_documents_by_id(uuid: str) -> list[dict]:
    return await get_comment_many_documents_by_filter({"id": uuid})


async def get_comment_many_documents_by_author(author_id: str) -> list[dict]:
    return await get_comment_many_documents_by_filter({"author": author_id})


async def get_comment_many_documents_by_parent(parent_id: str) -> list[dict]:
    return await get_comment_many_documents_by_filter({"for": parent_id})


class Comment:
    id: str
    parent_id: str
    author_id: str
    content: str
    created: int

    def __init__(self, document: dict) -> None:
        self.oid = document["_id"]
        self.id: str = document["id"]
        self.parent_id: str = document["for"]
        self.author_id: str = document["author"]
        self.content: str = document["content"]
        self.created: int = document["created"]

    def dump(self) -> dict:
        return {
            "_id": self.oid,
            "id": self.id,
            "for": self.parent_id,
            "author": self.author_id,
            "content": self.content,
            "created": self.created,
        }

    async def pull(self) -> None:
        doc = DB_COMMENTS.find_one({"_id": self.oid})
        if doc is None:
            raise LookupError(
                "The comment's document has been deleted from the database, but the object wasn't destroyed"
            )
        self.__init__(doc)

    async def push(self) -> None:
        DB_COMMENTS.find_one_and_replace({"_id": self.oid}, self.dump())

    async def delete(self) -> None:
        DB_COMMENTS.find_one_and_delete({"_id": self.oid})

    @classmethod
    async def fetch(cls, uuid: str):
        user = await get_comment_document_by_id(uuid)
        if user == {}:
            raise ValueError(
                f"Comment with the id {uuid} was not found in the database!"
            )
        return cls(user)

    @classmethod
    async def new(cls, parent: Post, author: User, content: str):
        now = time()
        comment = {
            "id": uuid(),
            "for": parent.id,
            "author": author.id,
            "content": content,
            "created": now,
        }
        oid = DB_COMMENTS.insert_one(comment)
        oid = oid.inserted_id
        comment["_id"] = oid
        return cls(comment)
