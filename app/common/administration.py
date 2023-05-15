from time import time

from models.database import (DB_COMMENTS, DB_GROUPS, DB_POSTS, DB_PROJECTS,
                             DB_USERS)


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
