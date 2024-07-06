import asyncio
from src.core.bot import Tether
from src.core.secrets import Env
tether = Tether()
env = Env()
asyncio.run(tether.run(env.token))  