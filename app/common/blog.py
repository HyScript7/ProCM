from base64 import b64decode

from common.dateparser import parse_date
from models import Post
from models.user import User, get_user_document_by_id


class ContentTable:
    data: dict

    def __init__(self, article_content: str) -> None:
        # Look through the article content to find headings
        # Store found headings in self.data in the format of {"Level 1 Heading": {"level 2 Heading": {...}}}
        pass


class parsedPost:
    def __init__(
        self,
        id: str,
        title: str,
        content: str,
        tags: list[str],
        author: dict,
        created: float,
    ):
        self.id: str = id
        self.title: str = title
        try:
            self.content: str = b64decode(content.encode("utf-8")).decode("utf-8")
        except UnicodeDecodeError:
            self.content: str = content
        self.tags: str = ", ".join(tags)
        self.author: User = author.get("username", "???")
        self.created: str = parse_date(created, show_time=True, time_sep_symbol="@")

    @classmethod
    async def parse(cls, post: dict):
        post: Post = Post(post)
        return cls(
            post.id,
            post.title,
            post.content,
            post.tags,
            await get_user_document_by_id(post.author_id),
            post.created,
        )
