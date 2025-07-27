# discotool/mcp/server.py
# SPDX-License-Identifier: Public-Domain
#
# This file is part of the discotool project and is dedicated to the public domain.
# You may use, modify, and distribute it without restriction.
# Randall Bohn with various AI assistants

import asyncio
import mcp.server.stdio
from mcp.server import Server
from discotool.mcp.tools import register_tools

server = Server("discotool")

register_tools(server)

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    asyncio.run(main())
