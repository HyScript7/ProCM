from base64 import b64decode, b64encode

from common.dateparser import parse_date
from models import Post
from models.user import User, get_user_document_by_id


def html_to_markdown(content: str, add_a_hrefs: bool = False):
    content: list[str] = ">\n<".join(content.split("><")).split("\n")
    for i, v in enumerate(content):
        if is_title(v):
            if add_a_hrefs:
                content[
                    i
                ] = f"<a id=\"{b64encode(title_html_to_md(v).encode('utf-8')).decode('utf-8')}\"></a>{v}"
                continue
            content[i] = title_html_to_md(v)
    return content


def is_title(html: str):
    try:
        if (
            html.lower().startswith("<h")
            and int(html[2]) in [1, 2, 3, 4, 5, 6]
            and html.lower()[len(html) - 5 : len(html) - 2] == "</h"
            and html.endswith(">")
        ):
            return True
    except ValueError:
        pass
    return False


def title_html_to_md(html: str):
    title_text = ""
    append = False
    skipping = False
    for i, v in enumerate(html):
        if skipping and html[i - 1] != ">":
            continue
        skipping = False
        if append and v == "<" and html[i + 1] == "/":
            break
        if append:
            title_text += v
            continue
        if html[i - 5 : i] == "<span" or (v == ">" and not "<span" in html):
            skipping = True
            append = True
    level = int(html.replace(" ", "")[2])
    return level * "#" + " " + title_text


class ContentTable:
    def __init__(self, content: list):
        self.table = self.parse(content)
        self.simple = self.simpleParse(self.table)

    def parse(self, content: list) -> dict:
        """Returns the titles as a dict system

        Args:
            content (list): The Markdown content

        Returns:
            dict: {"# Heading 1": {"## Heading 2": {}, "## Another Heading 2": {"### Heading 3": {}}}}
        """
        titles = {}
        path = []
        for i in content:
            if not (i.startswith("#") and i.replace("#", "").startswith(" ")):
                continue
            # Modify path if necessary
            level = i.split(" ")[0].count("#")
            indentLevel = len(path)
            if indentLevel >= level:
                path = path[0 : level - 1]
                path.append(i)
            elif indentLevel < level:
                path.append(i)
            # Add path to corresponding title
            current = titles
            lp = path[0 : len(path) - 1]
            for y in lp:
                current = current[y]
            current[i] = {}
        return titles

    def simpleParse(self, table, prefix="") -> list:
        """Returns the titles as a list (in order)

        This is a recursive function

        Args:
            table (_type_): The dict system content table
            prefix (str, optional): What should every single titles be prefixed with? Defaults to "".

        Returns:
            list: The titles in order
        """
        titles = []
        for i, n in enumerate(table):
            p = f"{prefix}{i+1}"
            titles.append(
                [
                    p,
                    "#" + b64encode(n.encode("utf-8")).decode("utf-8"),
                    n.replace("#", "").replace(" ", "", 1),
                ]
            )
            if len(table[n]):
                titles += self.simpleParse(table[n], prefix=(p + "."))
        return titles


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
        self.table = ContentTable(html_to_markdown(self.content)).simple
        self.content = html_to_markdown(self.content, True)
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
