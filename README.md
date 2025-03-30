# MCP Systems Setup Repo

A demonstration of setting up VS Code for MCP (Model Composition Protocol) server use with TinyLlama.

## Overview

This repository demonstrates how to set up and run a local MCP server with TinyLlama, a lightweight LLM that can run on consumer hardware. It showcases:

- Setting up a Python environment with `uv`
- Downloading and running a TinyLlama model
- Using MCP server and client implementations
- Integration with VS Code

## Prerequisites

- Python 3.13+
- [devbox](https://www.jetpack.io/devbox/) for development environment management
- Git

## Quick Start

1. Clone this repository
2. Initialize the development environment:
   ```bash
   devbox shell
   ```
3. Run the main script to see available options:
   ```bash
   python main.py
   ```

## Available Commands

The main script provides several options:

- **Download Model**: `python download_model.py` - Downloads the TinyLlama model from Hugging Face
- **Start Server**: `python server.py` - Runs the MCP server with the TinyLlama model
- **Run Client**: `python client.py` - Connects to the server and demonstrates tool calls
- **Run with Inspector**: `uv run mcp dev server.py` - Runs the server with the MCP inspector
- **Install in Claude**: `uv run mcp install server.py` - Installs the server capabilities in Claude

## Project Structure

- `main.py` - Main entry point with options menu
- `mcp_server.py` - MCP server implementation with tools, resources, and prompts
- `mcp_client.py` - MCP client implementation demonstrating interaction with the server
- `models/` - Directory for downloaded model files (gitignored)

## Development

This project uses:
- `uv` for Python package management
- `devbox` for development environment setup
- TinyLlama 1.1B chat model
- MCP for AI system composition

## License

See the LICENSE file for details.
