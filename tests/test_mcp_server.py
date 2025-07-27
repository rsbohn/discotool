# tests/test_mcp_tools.py
# SPDX-License-Identifier: Public-Domain
#
# This file is part of the discotool project and is dedicated to the public domain.
# You may use, modify, and distribute it without restriction.
# Randall Bohn with various AI assistants

from discotool.mcp.tools import register_tools
from mcp.server import Server
import pytest
from unittest.mock import patch, MagicMock
import asyncio


class MockServer:
    """Mock MCP server for testing tool registration."""
    def __init__(self):
        self.commands = {}
    
    def command(self, name, func):
        self.commands[name] = func


@pytest.mark.asyncio
async def test_scan_tool():
    """Test that the scan tool returns device data in the correct format."""
    # Mock the discotool.get_identified_devices function
    mock_device_data = [
        {'name': 'Test Device 1', 'vendor_id': 0x239a, 'product_id': 0x1234},
        {'name': 'Test Device 2', 'vendor_id': 0x239a, 'product_id': 0x5678}
    ]
    
    with patch('discotool.mcp.tools.discotool.get_identified_devices') as mock_get_devices:
        mock_get_devices.return_value = mock_device_data
        
        # Create mock server and register tools
        server = MockServer()
        register_tools(server)
        
        # Test that scan command was registered
        assert 'scan' in server.commands
        
        # Call the scan function
        scan_func = server.commands['scan']
        result = await scan_func()
        
        # Verify the result
        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]['name'] == 'Test Device 1'
        assert result[1]['name'] == 'Test Device 2'
        
        # Verify that get_identified_devices was called
        mock_get_devices.assert_called_once()

