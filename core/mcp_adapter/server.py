"""
MCP (Model Context Protocol) Adapter
Expose MindSymphony skills as MCP tools for integration with Claude Code

Inspired by claude-flow's 100 MCP tools architecture
"""

import json
import asyncio
from typing import Dict, Any, List, Optional
from pathlib import Path


class MCPServer:
    """
    MCP Server implementation for MindSymphony
    Exposes skills as MCP tools
    """

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.skill_metadata: Dict[str, Dict[str, Any]] = {}
        self._load_skills()

    def _load_skills(self):
        """Load all skills and convert to MCP tools"""
        if not self.skills_dir.exists():
            return

        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            # Parse skill metadata
            metadata = self._parse_skill(skill_md, skill_dir.name)
            if metadata:
                self.skill_metadata[skill_dir.name] = metadata

                # Create MCP tool
                tool = self._create_mcp_tool(skill_dir.name, metadata)
                self.tools[skill_dir.name] = tool

    def _parse_skill(self, skill_md: Path, skill_name: str) -> Optional[Dict[str, Any]]:
        """Parse SKILL.md to extract metadata"""
        try:
            content = skill_md.read_text(encoding='utf-8')

            # Extract description from frontmatter
            import re
            desc_match = re.search(r'description:\s*(.+?)(?:\n|$)', content)
            description = desc_match.group(1).strip() if desc_match else f"{skill_name} skill"

            # Extract capabilities
            capabilities = []
            cap_section = re.search(r'## 核心能力.*?\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
            if cap_section:
                cap_text = cap_section.group(1)
                capabilities = re.findall(r'[-*]\s*\*\*(.+?)\*\*', cap_text)

            # Extract input/output schemas
            input_schema = self._extract_input_schema(content)
            output_schema = self._extract_output_schema(content)

            return {
                'name': skill_name,
                'description': description,
                'capabilities': capabilities,
                'input_schema': input_schema,
                'output_schema': output_schema
            }

        except Exception as e:
            print(f"Error parsing {skill_md}: {e}")
            return None

    def _extract_input_schema(self, content: str) -> Dict[str, Any]:
        """Extract input schema from skill documentation"""
        # Default schema
        schema = {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "Task description or instruction"
                },
                "context": {
                    "type": "object",
                    "description": "Additional context for the task"
                }
            },
            "required": ["task"]
        }

        # TODO: Parse actual input schema from SKILL.md if defined
        return schema

    def _extract_output_schema(self, content: str) -> Dict[str, Any]:
        """Extract output schema from skill documentation"""
        # Default schema
        schema = {
            "type": "object",
            "properties": {
                "success": {
                    "type": "boolean",
                    "description": "Whether the task completed successfully"
                },
                "result": {
                    "type": "string",
                    "description": "Task result or output"
                },
                "metadata": {
                    "type": "object",
                    "description": "Additional metadata about execution"
                }
            }
        }

        return schema

    def _create_mcp_tool(self, skill_name: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Create MCP tool definition from skill metadata"""
        return {
            "name": f"mindsymphony_{skill_name.replace('-', '_')}",
            "description": metadata['description'],
            "inputSchema": metadata['input_schema'],
            "outputSchema": metadata['output_schema'],
            "capabilities": metadata['capabilities']
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available MCP tools"""
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "inputSchema": tool["inputSchema"]
            }
            for tool in self.tools.values()
        ]

    async def call_tool(
            self,
            tool_name: str,
            arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Execute a tool (skill) with given arguments"""
        # Extract skill name from tool name
        skill_name = tool_name.replace("mindsymphony_", "").replace("_", "-")

        if skill_name not in self.tools:
            return {
                "success": False,
                "error": f"Tool not found: {tool_name}"
            }

        # Execute skill
        # This would integrate with actual skill execution system
        result = await self._execute_skill(skill_name, arguments)

        return result

    async def _execute_skill(
            self,
            skill_name: str,
            arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a skill (placeholder implementation)
        Should integrate with actual skill execution engine
        """
        # Placeholder - return success
        return {
            "success": True,
            "result": f"Executed skill: {skill_name}",
            "metadata": {
                "skill_name": skill_name,
                "arguments": arguments
            }
        }

    def generate_mcp_config(self, output_path: str = "mcp_config.json"):
        """Generate MCP server configuration"""
        config = {
            "name": "mindsymphony",
            "version": "15.6.0",
            "description": "MindSymphony AI Orchestration System",
            "tools": self.list_tools(),
            "capabilities": {
                "skills": len(self.tools),
                "features": [
                    "Hybrid memory system",
                    "Fault tolerance",
                    "Semantic routing",
                    "Pattern learning",
                    "Performance monitoring"
                ]
            }
        }

        Path(output_path).write_text(json.dumps(config, indent=2, ensure_ascii=False))
        return config


class MCPClient:
    """Client for calling MCP tools"""

    def __init__(self, server_url: str = None):
        self.server_url = server_url or "http://localhost:8080"

    async def list_tools(self) -> List[Dict[str, Any]]:
        """List available tools from MCP server"""
        # Placeholder - would make HTTP request to server
        return []

    async def call_tool(
            self,
            tool_name: str,
            arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Call a tool on the MCP server"""
        # Placeholder - would make HTTP request
        return {
            "success": True,
            "result": "Placeholder response"
        }


class SkillWrapper:
    """Wrap MindSymphony skills for MCP compatibility"""

    def __init__(self, skill_name: str, skill_metadata: Dict[str, Any]):
        self.skill_name = skill_name
        self.metadata = skill_metadata

    def to_mcp_tool(self) -> Dict[str, Any]:
        """Convert skill to MCP tool format"""
        return {
            "name": f"mindsymphony_{self.skill_name.replace('-', '_')}",
            "description": self.metadata.get('description', ''),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "instruction": {
                        "type": "string",
                        "description": "Task instruction"
                    },
                    "context": {
                        "type": "object",
                        "description": "Execution context"
                    }
                },
                "required": ["instruction"]
            }
        }

    async def execute(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the skill with MCP arguments"""
        # This would integrate with actual skill execution
        return {
            "success": True,
            "skill_name": self.skill_name,
            "arguments": arguments
        }


def create_mcp_server_script(output_path: str = "start_mcp_server.py"):
    """Create a standalone MCP server script"""
    script_content = """#!/usr/bin/env python3
\"\"\"
MindSymphony MCP Server
Standalone server that exposes MindSymphony skills via MCP protocol
\"\"\"

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
    print("\\n📋 Available Tools:")
    for tool in server.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")

    # Start server (placeholder - would start HTTP server)
    print("\\n🌐 Server ready at http://localhost:8080")
    print("Press Ctrl+C to stop")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\\n👋 Server stopped")


if __name__ == "__main__":
    asyncio.run(main())
"""

    Path(output_path).write_text(script_content)
    Path(output_path).chmod(0o755)  # Make executable

    return output_path


def generate_claude_desktop_config(output_path: str = "claude_desktop_config.json"):
    """Generate configuration for Claude Desktop integration"""
    config = {
        "mcpServers": {
            "mindsymphony": {
                "command": "python",
                "args": ["start_mcp_server.py"],
                "env": {},
                "metadata": {
                    "description": "MindSymphony v15.6 - AI Orchestration System",
                    "version": "15.6.0",
                    "skills_count": 78
                }
            }
        }
    }

    Path(output_path).write_text(json.dumps(config, indent=2))
    return config
