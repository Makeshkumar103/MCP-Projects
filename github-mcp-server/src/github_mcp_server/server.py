import os

import httpx
from dotenv import load_dotenv
# from mcp.server.fastmcp import FastMCP
from mcp.server.mcpserver import MCPServer


load_dotenv()

mcp = MCPServer("GitHub Assistant")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
}


@mcp.tool()
async def search_repositories(query: str) -> str:
    """Search GitHub repositories."""

    url = "https://api.github.com/search/repositories"

    params = {
        "q": query,
        "per_page": 10,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=HEADERS,
            params=params,
        )

    response.raise_for_status()

    data = response.json()

    repositories = []

    for repo in data["items"]:
        repositories.append(
            {
                "name": repo["full_name"],
                "description": repo["description"],
                "stars": repo["stargazers_count"],
                "url": repo["html_url"],
            }
        )

    return str(repositories)


if __name__ == "__main__":
    mcp.run()
