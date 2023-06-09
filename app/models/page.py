from base64 import b64decode, b64encode
from time import time
from common.uuid import uuid
from common.xss_checker import safe_xss
from common.default_content import c_about, c_index, c_terms, c_privacy
from .database import DB_PAGES


async def get_page_document_by_filter(flt: dict) -> dict:
    doc = DB_PAGES.find_one(flt)
    if doc is None:
        return {}
    if "id" not in doc:
        return {}
    return doc


async def get_page_document_by_route(route: str) -> dict:
    return await get_page_document_by_filter({"route": route})


class Page:
    id: str
    created: int
    route: str
    can_be_deleted: bool
    content: str

    def __init__(self, document: dict) -> None:
        self.oid = document["_id"]
        self.id: str = document["id"]
        self.route: str = document["route"]
        self.can_be_deleted: bool = document["deletable"]
        self.content: str = safe_xss(
            b64decode(document["content"].encode("utf-8")).decode("utf-8")
        )
        self.created: int = document["created"]

    def dump(self) -> dict:
        return {
            "_id": self.oid,
            "id": self.id,
            "route": self.route,
            "deletable": self.can_be_deleted,
            "content": b64encode(self.content.encode("utf-8")).decode("utf-8"),
            "created": self.created,
        }

    async def pull(self) -> None:
        doc = DB_PAGES.find_one({"_id": self.oid})
        if doc is None:
            raise LookupError(
                "The page's document has been deleted from the database, but the object wasn't destroyed"
            )
        self.__init__(doc)

    async def push(self) -> None:
        DB_PAGES.find_one_and_replace({"_id": self.oid}, self.dump())

    async def delete(self) -> None:
        if self.can_be_deleted:
            DB_PAGES.find_one_and_delete({"_id": self.oid})
            return
        raise TypeError("Cannot delete a protected page!")

    @classmethod
    async def fetch(cls, route):
        page = await get_page_document_by_route(route)
        if page == {}:
            raise ValueError(
                f"Page at the route {route} was not found in the database!"
            )
        return cls(page)

    @classmethod
    async def new(cls, route: str, content: str, deletable: bool = True):
        route_check = await get_page_document_by_route(route)
        if route_check != {}:
            raise ValueError("The provided route is already registered!")
        now = time()
        pagedata = {
            "id": uuid(),
            "route": route,
            "deletable": deletable,
            "content": b64encode(safe_xss(content).encode("utf-8")).decode("utf-8"),
            "created": now,
        }
        oid = DB_PAGES.insert_one(pagedata)
        oid = oid.inserted_id
        pagedata["_id"] = oid
        return cls(pagedata)


async def get_all_pages(only_user_defined: bool = False):
    mod = {}
    if only_user_defined:
        mod["deletable"] = True
    pages = []
    for page in DB_PAGES.find({"id": {"$exists": True}, **mod}):
        pages.append(Page(page))
    return pages


async def create_default_pages():
    pages = {"index": c_index, "about": c_about, "terms": c_terms, "privacy": c_privacy}
    for route, content in pages.items():
        if (await get_page_document_by_route(route)) != {}:
            continue
        await Page.new(route, b64decode(content.encode("utf-8")).decode("utf-8"), False)
