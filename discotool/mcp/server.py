# discotool/mcp/server.py
# SPDX-License-Identifier: Public-Domain
#
# This file is part of the discotool project and is dedicated to the public domain.
# You may use, modify, and distribute it without restriction.
# Randall Bohn with various AI assistants

import argparse
import asyncio
import logging
import os
import sys
import mcp.server.stdio
from mcp.server import Server
from discotool.mcp.tools import register_tools

server = Server("discotool")

register_tools(server)

async def timeout_shutdown():
    """Wait 5 seconds then exit the program."""
    await asyncio.sleep(5)
    print("Timeout reached, shutting down server...")
    print("Press ENTER to exit.")
    exit(0)

async def main():
    # Configure logging to stderr
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        stream=sys.stderr
    )
    logger = logging.getLogger(__name__)
    
    # Print startup banner
    script_path = os.path.abspath(__file__)
    cwd = os.getcwd()
    logger.info(f"Starting discotool MCP server")
    logger.info(f"Script: {script_path}")
    logger.info(f"CWD: {cwd}")
    
    parser = argparse.ArgumentParser(description="MCP server for discotool")
    parser.add_argument("-t", "--timeout", action="store_true", 
                       help="Enable 15 second timeout before shutdown")
    args = parser.parse_args()
    
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        if args.timeout:
            # Start timeout task
            timeout_task = asyncio.create_task(timeout_shutdown())
            server_task = asyncio.create_task(server.run(read_stream, write_stream, {}))
            
            # Wait for either the server to finish or timeout to occur
            done, pending = await asyncio.wait(
                [server_task, timeout_task], 
                return_when=asyncio.FIRST_COMPLETED
            )
            
            # Cancel any remaining tasks
            for task in pending:
                task.cancel()
        else:
            await server.run(read_stream, write_stream, {})

if __name__ == "__main__":
    asyncio.run(main())
