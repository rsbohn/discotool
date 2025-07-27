# tests/test_mcp_tools.py
# SPDX-License-Identifier: Public-Domain
#
# This file is part of the discotool project and is dedicated to the public domain.
# You may use, modify, and distribute it without restriction.
# Randall Bohn with various AI assistants

from discotool.mcp.tools import register_tools
from mcp.server import Server
import pytest

@pytest.mark.asyncio
async def test_disco_scan_tool():
    server = Server("test")
    register_tools(server)
    
    call_fn = server._tool_call_callbacks["disco-scan"]
    response = await call_fn("disco-scan", {"text": "Stayin' Alive"})
    
    assert isinstance(response, list)
    assert any("Alive" in r.text for r in response)
