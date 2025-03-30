# MCP Systems Setup Repo

This repository demonstrates how to set up and use the Model Composition Protocol (MCP) with TinyLlama in VS Code.

## Overview

The Model Composition Protocol (MCP) enables AI systems to expose capabilities to other systems in a standardized way. This project shows how to:

- Set up a local MCP server using TinyLlama
- Create and use MCP clients
- Accelerate MCP development using LLMs
- Integrate MCP with VS Code

## Prerequisites

- Python 3.13+
- [devbox](https://www.jetpack.io/devbox/) for development environment management
- Git

## Getting Started

1. Clone this repository
2. Initialize the development environment:
   ```bash
   devbox shell
   ```
3. Install dependencies using `uv` (automatically handled by devbox)

## Running the Server

Start the basic MCP server with:

```bash
python simple_server.py
```

Or try the Rick knowledge base server:

```bash
python rick_server.py
```

This will initialize the TinyLlama model and expose it through an MCP server running on localhost.

## Testing with a Client

Connect to the basic server using:

```bash
python simple_client.py
```

Or connect to the Rick knowledge base server:

```bash
python rick_client.py
```

These demonstrate basic interactions with the MCP server, including tool calls and resource utilization.

## Simple Llama Chat

For a direct interface with the TinyLlama model without MCP:

```bash
python simple_llama_chat.py
```

## MCP Inspector

For debugging and exploring the MCP server capabilities, use the MCP Inspector:

```bash
uv run mcp dev simple_server.py
```

Or for the Rick server:

```bash
uv run mcp dev rick_server.py
```

## Integration with Claude

To install your MCP server capabilities in Claude:

```bash
uv run mcp install simple_server.py
```

## Guides and Tutorials

- [Building MCP with LLMs](building_mcp_with_llms.md) - Detailed instructions on using Claude and other frontier LLMs to accelerate your MCP development
- [MCP Tutorial](mcp-tutorial.md) - Step-by-step tutorial for getting started with MCP

## Project Structure

- `simple_server.py` - Basic MCP server implementation with TinyLlama
- `simple_client.py` - Basic MCP client for testing
- `rick_server.py` - MCP server with Rick and Morty knowledge base
- `rick_client.py` - Client for the Rick knowledge base server
- `Ricks_KB.txt` - Knowledge base text file for the Rick server
- `simple_llama_chat.py` - Direct interface to TinyLlama without MCP
- `building_mcp_with_llms.md` - Guide for MCP development with LLMs
- `mcp-tutorial.md` - Step-by-step MCP tutorial
- `devbox.json` - Development environment configuration
- `devbox.lock` - Locked dependencies for devbox
- `pyproject.toml` - Python project configuration
- `uv.lock` - Locked dependencies for uv package manager
- `models/` - Directory for downloaded model files (gitignored)
- `test/` - Test files for the project
- `__pycache__/` - Python bytecode cache (gitignored)

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [TinyLlama on Hugging Face](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0)