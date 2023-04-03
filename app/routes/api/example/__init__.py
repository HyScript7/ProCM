from .. import api

@api.route("/")
async def root():
    return "OK!"
