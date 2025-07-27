# SPDX-License-Identifier: Public-Domain
#
# This file is part of the discotool project and is dedicated to the public domain.
# You may use, modify, and distribute it without restriction.
# Randall Bohn with various AI assistants

"""Utilities for registering commands with an MCP server."""

from typing import Any, List, Dict

import discotool


def register_tools(server: Any) -> None:
    """Register commands used by the MCP server.

    Parameters
    ----------
    server : mcp.server.Server
        MCP server instance used to register commands.
    """

    async def scan() -> List[Dict[str, Any]]:
        """Return the list of discovered devices.

        This calls :func:`discotool.get_identified_devices` and converts the
        resulting :class:`DeviceInfoDict` objects into plain dictionaries so
        that they can be serialised easily by the MCP server.
        """

        devices = discotool.get_identified_devices()
        return [dict(d) for d in devices]

    # Older versions of ``mcp`` expose ``command`` as a decorator while newer
    # ones offer ``register``/``add`` functions. Attempt all known names for
    # compatibility.
    if hasattr(server, "command") and callable(getattr(server, "command")):
        server.command("scan", scan)
    elif hasattr(server, "register") and callable(getattr(server, "register")):
        server.register("scan", scan)
    elif hasattr(server, "add_command") and callable(getattr(server, "add_command")):
        server.add_command("scan", scan)
    else:
        # Fallback: try attribute assignment which some simple servers use.
        setattr(server, "scan", scan)

