import logging
from datetime import datetime

from aiohttp import web
from discord.ext import commands, tasks


class Apiserver(commands.Cog):

    def __init__(self, host: str, port: int) -> None:
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
        """Starts the api event loop. Only run during or after on_ready."""
        self.app.add_routes(self.routes)
        runner = web.AppRunner(self.app)
        await runner.setup()

        site = web.TCPSite(runner, host=self.webserver_host, port=self.webserver_port)
        await site.start()
        logging.warning(
            f"Discord API started on {self.webserver_host}:{self.webserver_port}"
        )
