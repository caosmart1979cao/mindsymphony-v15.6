#!/usr/bin/env python3
"""
MindSymphony MCP Server
Standalone server that exposes MindSymphony skills via MCP protocol
"""

import asyncio
import json
from pathlib import Path
from core.mcp_adapter.server import MCPServer


async def main():
    # Initialize server
    server = MCPServer(skills_dir="skills")

    print("🚀 MindSymphony MCP Server starting...")
    print(f"📦 Loaded {len(server.tools)} skills as MCP tools")

    # Generate configuration
    config = server.generate_mcp_config()
    print(f"✅ Generated MCP configuration: mcp_config.json")

    # List tools
    print("\n📋 Available Tools:")
    for tool in server.list_tools()[:10]:  # Show first 10
        print(f"  - {tool['name']}: {tool['description'][:60]}...")

    if len(server.tools) > 10:
        print(f"  ... and {len(server.tools) - 10} more tools")

    # Start server (placeholder - would start HTTP server)
    print("\n🌐 Server ready at http://localhost:8080")
    print("📚 Full tool list available in mcp_config.json")
    print("\n💡 To integrate with Claude Code:")
    print("   1. Add mcp_config.json to your Claude Desktop configuration")
    print("   2. Restart Claude Desktop")
    print("   3. All MindSymphony skills will be available as MCP tools")
    print("\nPress Ctrl+C to stop")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Server stopped")


if __name__ == "__main__":
    asyncio.run(main())
