from models import Group, get_default_group_id, get_admin_group_id
from models.user import User, get_user_document_by_id


class Editor:
    user: User

    def __init__(self, user: User) -> None:
        self.group_selector = {}
        self.user = user

    async def fetch_groups(self) -> None:
        self.group_selector["Admin"] = await get_admin_group_id()
        self.group_selector["Default"] = await get_default_group_id()

    @classmethod
    async def edit(cls, uuid):
        e = cls(User(await get_user_document_by_id(uuid)))
        await e.fetch_groups()
        return e
