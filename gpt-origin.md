guide me how to do it step by step [Github MCP server, file/document assistant, weather assistant, multi-tool business assistant]

ChatGPT said:
Great. I recommend doing all four in sequence, because each project teaches you something new and the final one can become your strongest portfolio project.

We'll use Python + the official MCP Python SDK. The current SDK requires Python 3.10+ and supports tools, resources, prompts, and transports such as stdio and Streamable HTTP. 
G
GitHub
+1

The roadmap
Project	What you learn	Difficulty
1. GitHub MCP Server	REST APIs, authentication, MCP tools	⭐⭐
2. File/Document Assistant	Files, search, resources, document processing	⭐⭐⭐
3. Weather Assistant	External APIs, structured data, error handling	⭐⭐
4. Multi-tool Business Assistant	Multiple APIs + tool orchestration	⭐⭐⭐⭐⭐

The goal isn't just to copy code. I'll explain why each part exists, then we'll build it.

Part 0 — Understand MCP first
Think of MCP like this:

                    ┌─────────────────┐
                    │   AI Assistant  │
                    │  Claude/Cursor  │
                    │  Your AI App    │
                    └────────┬────────┘
                             │
                          MCP
                             │
             ┌───────────────┴──────────────┐
             │                               │
       ┌─────▼─────┐                   ┌────▼─────┐
       │ MCP Server │                   │MCP Server│
       │   GitHub   │                   │  Weather │
       └─────┬─────┘                   └────┬─────┘
             │                               │
        GitHub API                       Weather API

The important idea:

Your MCP server exposes capabilities to an AI.

For example:

search_github_repositories()
get_repository()
get_issues()
get_pull_requests()

The AI doesn't need to know how the GitHub API works. Your MCP server handles that.

Part 1 — Set up your development environment
I recommend:

Python

VS Code

Git

GitHub

uv

MCP Python SDK

The official SDK currently recommends uv, although pip is also supported. 
G
GitHub

Step 1: Check Python
Open a terminal:

python --version

You want:

Python 3.10+

I'd personally use Python 3.12 or 3.13 for this project.

Step 2: Install uv
If you don't have it, install it from the official uv project.

Then check:

uv --version

Part 2 — Create our first MCP project
Let's start with GitHub.

Create a folder:

mkdir mcp-projects
cd mcp-projects

Then:

uv init github-mcp-server
cd github-mcp-server

You'll have something similar to:

github-mcp-server/
├── pyproject.toml
└── ...

Install MCP:

uv add "mcp[cli]"

This is the current official installation approach. 
G
GitHub

Part 3 — Your first MCP server
Create:

server.py

Put this inside:

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("GitHub Assistant")


@mcp.tool()
def hello(name: str) -> str:
    """Say hello to a user."""
    return f"Hello {name}!"


if __name__ == "__main__":
    mcp.run()

That's your first MCP server.

The important part is:

@mcp.tool()

This tells MCP:

"Make this Python function available as an AI tool."

So this:

def hello(name: str) -> str:

becomes something the AI can call.

Part 4 — Test your MCP server
The official SDK provides an MCP development command/Inspector workflow. 
G
GitHub

Run:

uv run mcp dev server.py

You should be able to inspect the server and see:

hello

Then test it with:

name = "John"

and get:

Hello John!

🎯 Milestone 1
At this point you've learned:

Python function
       ↓
@mcp.tool()
       ↓
MCP tool
       ↓
AI can call it

Don't move ahead until this works.

Part 5 — Project #1: GitHub MCP Server
Now we'll turn our simple server into a real project.

Our final GitHub MCP server will have:

GitHub MCP Server
│
├── search_repositories
├── get_repository
├── get_issues
├── get_pull_requests
├── get_file
├── get_user
└── search_code

For example, the user could tell an AI:

"Find popular Python repositories related to MCP."

The AI can call:

search_repositories()

Your MCP server calls:

GitHub REST API

and returns the results.

Part 6 — GitHub authentication
For anything beyond basic public API usage, authentication is important. GitHub supports personal access tokens and GitHub Apps, and recommends fine-grained tokens when using personal access tokens. 
G
GitHub Docs
+1

Create a GitHub token and store it as an environment variable.

Do not put the token directly in Python code.

Bad:

GITHUB_TOKEN = "ghp_xxxxxxxxx"

Good:

GITHUB_TOKEN=...

in an environment file.

Create:

.env

For example:

GITHUB_TOKEN=your_token_here

And add .env to .gitignore:

.env

This is extremely important because you don't want your GitHub token committed to GitHub.

Part 7 — Install HTTP library
We'll use httpx.

uv add httpx python-dotenv

Now our architecture becomes:

             AI
              │
              │ MCP
              ▼
      ┌─────────────────┐
      │ GitHub MCP      │
      │ Server          │
      │                 │
      │ @mcp.tool()     │
      └────────┬────────┘
               │
             HTTP
               │
               ▼
       ┌───────────────┐
       │ GitHub REST   │
       │ API           │
       └───────────────┘

GitHub's REST API is documented extensively, including authentication and endpoint usage. 
G
GitHub Docs
+1

Part 8 — Build search_repositories
Create:

import os

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP


load_dotenv()

mcp = FastMCP("GitHub Assistant")

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

Now you have a real MCP tool.

Part 9 — Understand what just happened
The AI sees:

search_repositories

with an input:

query: string

The AI might decide:

User:
"Find MCP projects on GitHub"

↓

AI
↓
search_repositories(
    query="model context protocol"
)

↓

MCP Server
↓
GitHub API

↓

GitHub results

↓

MCP Server
↓
AI

↓

AI:
"I found these repositories..."

That's the core concept you need to understand.

Part 10 — Add more GitHub tools
Once search_repositories() works, we'll add:

get_repository
get_repository("owner/repository")

Returns:

name
description
stars
forks
language
open issues
URL

get_issues
get_issues("owner/repository")

Returns:

issue number
title
author
state
URL

get_pull_requests
get_pull_requests("owner/repository")

Returns:

PR number
title
author
state
URL

get_file
get_file(
    repository="owner/repository",
    path="README.md"
)

Returns the contents of a GitHub file.

get_user
get_user("username")

Returns GitHub profile information.

Part 11 — Project #2: File/Document Assistant
Once GitHub works, start a new project:

cd ..
uv init document-mcp-server
cd document-mcp-server
uv add "mcp[cli]"

The concept:

                  AI
                   │
                   │ MCP
                   ▼
          ┌──────────────────┐
          │ Document MCP     │
          │ Server            │
          └────────┬─────────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
     TXT         PDF          DOCX

Tools:

list_files()
read_file()
search_files()
get_document()

For example:

"Find all documents containing the word Kubernetes."

AI:

search_files("Kubernetes")

Your MCP server:

scan documents
      ↓
search text
      ↓
return matches

Part 12 — Make the document project better
Don't stop at simple file reading.

Add:

list_documents()
read_document()
search_documents()
summarize_document()
extract_metadata()

Then your project becomes:

             Document Assistant
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
        PDF        DOCX        TXT
          │          │          │
          └──────────┼──────────┘
                     ▼
              MCP Server
                     │
                     ▼
                    AI

This is already a very good portfolio project.

Part 13 — Project #3: Weather MCP Server
Next:

cd ..
uv init weather-mcp-server
cd weather-mcp-server
uv add "mcp[cli]" httpx

Tools:

get_current_weather(city)
get_forecast(city)
get_weather_alerts(city)

Example:

"What's the weather in Chennai?"

AI calls:

get_current_weather("Chennai")

Your MCP server:

MCP
 ↓
Weather API
 ↓
JSON
 ↓
MCP
 ↓
AI

The important thing you'll learn here is external API integration.

Part 14 — Project #4: Multi-tool Business Assistant
This is the project I'd ultimately put on your resume.

Instead of having one API, combine several MCP capabilities.

Imagine:

                 Business AI
                      │
                      ▼
              MCP Business Server
                      │
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
     GitHub        Weather         Documents
        │             │              │
        ▼             ▼              ▼
    GitHub API    Weather API      Local files

Then add business functionality.

For example:

search_company()
get_company_repositories()
get_company_documents()
get_weather()
search_news()
generate_report()

A realistic example
Imagine someone asks:

"Analyze Microsoft's developer activity this week and prepare a short report."

Your MCP server could potentially perform:

1. Find Microsoft repositories
          ↓
2. Get recent commits
          ↓
3. Get recent pull requests
          ↓
4. Get issues
          ↓
5. Search company documents
          ↓
6. Get relevant external information
          ↓
7. Generate structured result

The AI orchestrates the tools.

That's much more impressive than:

"I made a chatbot."

Recommended final architecture
Eventually I'd structure the project like this:

mcp-business-assistant/
│
├── server.py
│
├── tools/
│   ├── github.py
│   ├── weather.py
│   ├── documents.py
│   └── business.py
│
├── services/
│   ├── github_service.py
│   ├── weather_service.py
│   └── document_service.py
│
├── models/
│   └── schemas.py
│
├── tests/
│   ├── test_github.py
│   ├── test_weather.py
│   └── test_documents.py
│
├── .env
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock

That gives you a proper software project rather than one giant Python file.

Your learning sequence
I strongly recommend not building all four simultaneously.

Follow this:

WEEK 1
│
├── MCP fundamentals
├── Python MCP SDK
├── Tools
├── Resources
├── MCP Inspector
└── GitHub MCP
        │
        ▼
WEEK 2
│
├── REST APIs
├── Authentication
├── Error handling
├── File handling
└── Document MCP
        │
        ▼
WEEK 3
│
├── External APIs
├── Async Python
├── Structured responses
└── Weather MCP
        │
        ▼
WEEK 4+
│
├── Multiple MCP tools
├── Database
├── Search
├── Security
├── Testing
├── Deployment
└── Business AI Assistant

What I'd have you build first
Don't start with the huge business assistant.

Start with:

GitHub MCP Server

and get these 5 tools working:

1. search_repositories()
2. get_repository()
3. get_issues()
4. get_pull_requests()
5. get_file()

Then we'll connect it to an MCP client and make sure you can actually ask an AI things like:

"Find Python MCP repositories."

"Show me the open issues in this repository."

"Read the README of this project."

"Which repository has more stars?"

After that, we'll move to the Document Assistant, then Weather, and finally combine everything.

For reference, the official MCP Python SDK is here: MCP Python SDK, and the official GitHub REST API documentation is here: GitHub REST API documentation. 
G
GitHub
+1

Next step: build the GitHub MCP server with me from zero, one command/file at a time. We can start with Step 1: installing Python + uv and creating the project, and I’ll wait for the result of each step before giving you the next one.