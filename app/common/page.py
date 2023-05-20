from models import Page


class blankPage:
    def __init__(self) -> None:
        self.id = 0
        self.content = "<h1>Hello World!</h1>"
        self.route = "example"
        self.can_be_deleted = True


class pageEditor:
    is_new: bool
    id: str
    route: str
    can_be_deleted: bool
    content: str

    def __init__(self, page: Page | blankPage, is_new: bool = False) -> None:
        self.id = page.id
        self.route = page.route
        self.content = page.content
        self.is_new = is_new
        self.can_be_deleted = page.can_be_deleted

    @classmethod
    def new_file(cls):
        return cls(blankPage(), is_new=True)

    @classmethod
    async def fetch(cls, route: str):
        page = await Page.fetch(route)
        return cls(page)
