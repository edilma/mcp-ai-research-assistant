import os
from mcp.server.mcpserver import MCPServer

# Public demonstration server
mcp = MCPServer("research-demo")


@mcp.tool()
def hello(name: str = "World") -> str:
    """Test the connection to the remote MCP server."""
    return f"Hello, {name}! Your remote MCP server works."


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8001")),
        stateless_http=True,
        json_response=True,
    )
