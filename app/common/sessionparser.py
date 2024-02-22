from models import User


async def get_session(session):
    try:
        user = await User.from_token(session.get("token", ""))
    except ValueError:
        return False
    return (True, user)
