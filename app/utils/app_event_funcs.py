from application import database
from application import ps


async def startup():
    await database.connect()
    await ps.setup()


async def shutdown():
    await database.disconnect()
