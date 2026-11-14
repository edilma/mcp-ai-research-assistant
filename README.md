# MCP Research Chatbot

A Python command-line research assistant that uses Claude to search arXiv for academic papers, save paper metadata, and summarize findings. The MCP chatbot can also retrieve information from other websites through the Fetch server. The project demonstrates Claude’s native tool calling and how a client discovers and uses tools through the Model Context Protocol (MCP).

## What’s included

| Component | What it does |
| --- | --- |
| `chatbot` | Runs the original command-line chatbot using Claude’s native tool calling for arXiv research. |
| `mcp-chatbot` | Runs the command-line chatbot as an MCP client and discovers tools from the servers in `server_config.json`. |
| Research server | Searches arXiv, saves paper metadata, and exposes saved results and a research prompt through MCP. |
| Filesystem server | Lets the MCP chatbot read and manage files within the configured `papers` folder. |
| Fetch server | Lets the MCP chatbot retrieve content from other websites. |
| Remote demo server | Exposes a `hello` tool for testing a remote MCP connection over Streamable HTTP. |

Searches save titles, authors, abstracts, dates, and PDF links in `papers/<topic>/papers.json`. PDF files stay on arXiv.

## Setup

Install [uv](https://docs.astral.sh/uv/) and use Python 3.12 or newer. Install Node.js with npm if you plan to use the Filesystem server or MCP Inspector.

Run the following from the project root in PowerShell:

```powershell
uv sync
Copy-Item .env.example .env
```

If you already have a `.env` file, keep it and add your Anthropic API key there:

```dotenv
ANTHROPIC_API_KEY=your_anthropic_api_key
```

Both command-line chatbots use the Anthropic API. The Research server can run on its own without that key. Keep `.env` out of version control.

## Run the chatbot

To use Claude’s native tool calling:

```powershell
uv run chatbot
```

To use the MCP client:

```powershell
uv run mcp-chatbot
```

Run the MCP client from the project root so it can find `server_config.json`. Try asking it to find two papers about AI interpretability and summarize their abstracts. Type `quit` to exit either chatbot.

## Configure MCP servers

The project’s `server_config.json` contains these entries:

| Server | Transport | Purpose |
| --- | --- | --- |
| `research` | STDIO | Starts `chatbot.research_server` locally for arXiv search and saved paper lookup. |
| `filesystem` | STDIO | Starts the Filesystem server through `npx` and grants access to the directory specified in its arguments. |
| `fetch` | STDIO | Starts `mcp-server-fetch` through `uvx` to retrieve web content. |
| `remote-demo` | Streamable HTTP | Connects to a hosted demo endpoint that exposes the `hello` tool. |

Before launching the client, update the Filesystem path to an existing `papers` directory on your machine. On Windows, the configuration uses `cmd /c` to launch `npx`. The client attempts to connect to every configured server at startup. If the hosted demo is unavailable or you’re testing only local servers, remove the `remote-demo` entry from your local configuration.

Grant Filesystem access only to a folder you’re comfortable having it read and modify. Review saved paper metadata before committing it or sharing it through a chat.

## Research tools and resources

| Name | Purpose |
| --- | --- |
| `search_papers(topic, max_results=5)` | Searches arXiv, saves the results locally, and returns paper IDs. |
| `extract_info(paper_id)` | Looks up metadata for a previously saved arXiv paper. |
| `papers://folders` | Lists topics with saved results. |
| `papers://{topic}` | Reads saved metadata for a topic. |
| `generate_search_prompt` | Generates instructions for searching and comparing papers on a topic. |

## Test the Research server

From the project root, launch MCP Inspector:

```powershell
npx @modelcontextprotocol/inspector uv run python -m chatbot.research_server
```

Open the Inspector URL printed in the terminal, connect using STDIO, and check that `search_papers` and `extract_info` are listed. If a tool call produces protocol errors, check for diagnostic output on stdout. STDIO MCP uses stdout for protocol messages and stderr for logs.

To connect through Claude Desktop on Windows, configure the server in `%APPDATA%\Claude\claude_desktop_config.json`. Use `uv --directory` with the absolute project path so Claude Desktop can launch the Research server from the correct directory.

## Test the HTTP demo locally

```powershell
uv run python -m chatbot.remote_server
```

Connect an MCP client to `http://localhost:8001/mcp` using Streamable HTTP and call `hello`. The demo uses port `8001` by default and accepts a different port through the `PORT` environment variable.

## Project structure

```text
chatbot/
├── src/chatbot/
│   ├── main.py              # Original chatbot entry point
│   ├── chatbot.py           # Claude native tool calling
│   ├── tools.py             # arXiv search and metadata lookup
│   ├── tool_schema.py       # Tool definitions for the original chatbot
│   ├── mcp_main.py          # MCP chatbot entry point
│   ├── mcp_chatbot.py       # MCP connections and Claude tool routing
│   ├── research_server.py   # Local STDIO research server
│   └── remote_server.py     # Streamable HTTP demo server
├── papers/                  # Local paper metadata
├── server_config.json       # MCP client server configuration
├── .env.example             # Environment variable template
├── pyproject.toml           # Project dependencies and CLI commands
└── uv.lock                  # Locked dependencies
```

## Features

- Search arXiv for academic papers by topic and summarize the findings with Claude.
- Save paper titles, authors, abstracts, publication dates, and PDF links locally. Browse saved results by topic or look up a paper by its arXiv ID.
- Retrieve content from other websites with the Fetch MCP server.
- Read and manage files in the configured `papers` folder with the Filesystem MCP server.
- Run the original Claude chatbot or the MCP chatbot from the command line.
- Test a remote MCP connection with the demo server’s `hello` tool.

## Tech Stack

- **Python 3.12+** for the chatbots and MCP servers
- **uv** for dependencies and running the project
- **Anthropic SDK** for Claude API calls
- **MCP Python SDK** for MCP clients and servers
- **arxiv** for academic paper searches
- **python-dotenv** for loading local environment variables
- **Node.js and npm** for launching the Filesystem server and MCP Inspector