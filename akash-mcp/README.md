# Dev.to Blog Publisher MCP Server

This project provides an MCP (Model Context Protocol) server tool for publishing blog posts directly to Dev.to. It exposes a tool (publish_blog_to_devto) that can be called from an MCP-compatible client

## Refer this video on how to use this MCP server: `https://www.youtube.com/watch?v=cMulGPMnbUA`

## Prerequisites

- In this project I have used `uv` to install python dependencies.
- `Node.js` & npm (for npx to run filesystem MCP server)

## Environment Variables

Create a .env file in the project root with the following:
`DEVTO_API_KEY=your_devto_api_key_here`

### Install uv (Python package manager):

`curl -LsSf https://astral.sh/uv/install.sh | sh`

### Verify the installation:

`uv --version`

## Environment Setup

### Create a Virual Environment

`uv venv`

#### Activate the environment

`source ./venv/bin/activate`

#### Install Dependencies

`uv sync`

## Note: Modify your path in the claude-desktop-config.json as shown in the example config.json
