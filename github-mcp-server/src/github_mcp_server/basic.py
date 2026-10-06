# from mcp.server.fastmcp import FastMCP
from mcp.server.mcpserver import MCPServer
# from mcp import Server, tool



# mcp = FastMCP("GitHub Assistant")
mcp = MCPServer("GitHub Assistant")

@mcp.tool()
def hello(name: str) -> str:
    """Say hello to a user."""
    return f"Hello {name}!"


if __name__ == "__main__":
    mcp.run()
