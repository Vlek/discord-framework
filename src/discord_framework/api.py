from datetime import datetime

from aiohttp import web
from discord.ext import commands, tasks


class Apiserver(commands.Cog):

    async def __init__(self, bot: commands.Bot, host: str, port: int):
        self.bot: commands.Bot = bot

        self.app: web.Application = web.Application()
        self.routes: web.RouteTableDef = web.RouteTableDef()

        self.webserver_host: str = host
        "The address the api responds to. e.g. 0.0.0.0"
        self.webserver_port: int = port
        "The port the api is listening on. e.g. 80"

        @self.routes.get("/heartbeat")
        async def heartbeat(request) -> web.Response:
            return web.Response(text=f"pong {datetime.now()}")

    @tasks.loop()
    async def run(self) -> None:
        runner = web.AppRunner(self.app)
        await runner.setup()

        site = web.TCPSite(runner, host=self.webserver_host, port=self.webserver_port)
        await site.start()

    @run.before_loop
    async def web_server_before_loop(self) -> None:
        await self.bot.wait_until_ready()
