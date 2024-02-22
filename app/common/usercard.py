from models import User
from models.database import DB_COMMENTS


class User_card:
    def __init__(self, user: User, comment_count: int) -> None:
        self.username: str = user.username
        self.pfp_url: str = "User Card Profile Picture Base64 Data"
        self.comments: int = comment_count

    @classmethod
    async def get(cls, user: User):
        comment_count: int = DB_COMMENTS.count_documents({"author": user.id})
        return cls(user, comment_count)
