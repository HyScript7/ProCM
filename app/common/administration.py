from base64 import b64decode, b64encode
from time import time

from common.xss_checker import safe_xss
from models.database import DB_COMMENTS, DB_GROUPS, DB_POSTS, DB_PROJECTS, DB_USERS
from models.post import Post


class DashboardData:
    user_count: int
    post_count: int
    comment_count: int
    project_count: int
    updated: float

    def __init__(self) -> None:
        self.user_count = DB_USERS.count_documents({"id": {"$exists": True}})
        self.post_count = DB_POSTS.count_documents({"id": {"$exists": True}})
        self.comment_count = DB_COMMENTS.count_documents({"id": {"$exists": True}})
        self.project_count = DB_PROJECTS.count_documents({"id": {"$exists": True}})
        self.updated = time()


class PostEditor(Post):
    def __init__(self, document: dict, is_new: bool = False) -> None:
        super().__init__(document)
        self.content = safe_xss(b64decode(self.content.encode("utf-8")).decode("utf-8"))
        self.is_new = is_new

    @classmethod
    async def blank(cls):
        return cls(
            {
                "_id": 0,
                "id": 0,
                "title": "Untitled",
                "tags": ["Example Tag", "Another Tag"],
                "author": 0,
                "content": b64encode(
                    "<h1>Hello World!</h1><p>This is placeholder post content! Change it using the Admin editor</p>".encode(
                        "utf-8"
                    )
                ).decode("utf-8"),
                "created": 0,
            },
            True,
        )
