# MCP Tutorial: Building LLM-Integrated Knowledge Systems

This tutorial will introduce you to the Model Context Protocol (MCP) through hands-on examples. We'll create two progressively more complex systems that integrate with a local LLM, demonstrating key MCP concepts along the way.

## Introduction to MCP

The Model Context Protocol (MCP) is a standardized way for applications to provide context to Large Language Models (LLMs). It enables:

- Secure access to data and tools
- Standardized interfaces for LLM interactions
- Separation of context provision from the actual LLM interactions
- Extensible architecture for building AI-powered applications

MCP consists of two main components:

1. **MCP Servers**: Expose data and functionality
2. **MCP Clients**: Connect to servers and facilitate LLM interactions

## Prerequisites

- Python 3.10 or higher
- The MCP SDK: `pip install "mcp[cli]"`
- [llama-cpp-python](https://github.com/abetlen/llama-cpp-python): `pip install llama-cpp-python`
- A local LLM model (we're using TinyLlama in these examples)

## Example 1: Minimal MCP Implementation

Let's start with the simplest possible MCP system: a server that exposes a single tool to query a local LLM, and a client that connects to this server.

### Minimal Server Implementation

```python
# simple_server.py
from mcp.server.fastmcp import FastMCP

# Create a minimal MCP server
mcp = FastMCP("MinimalLLMServer")

# Add a simple tool to query your LLM
@mcp.tool()
def query_llm(prompt: str) -> str:
    """Send a prompt to the local LLM and return its response"""
    from llama_cpp import Llama
    
    # Load the model
    model_path = "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    model = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=4
    )
    
    # Format the prompt for TinyLlama's chat format
    formatted_prompt = f"<|system|>\nYou are a helpful, friendly AI assistant.</s>\n<|user|>\n{prompt}</s>\n<|assistant|>\n"
    
    # Generate completion
    output = model.create_completion(
        prompt=formatted_prompt,
        max_tokens=512,
        temperature=0.7,
        stop=["<|user|>", "</s>"]
    )
    
    # Return the generated text
    return output['choices'][0]['text']

# Run the server when the script is executed directly
if __name__ == "__main__":
    mcp.run()
```

### Minimal Client Implementation

```python
# simple_client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["simple_server.py"],
    )
    
    # Connect to the server
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools_result = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools_result.tools]}")
            
            # Simple interaction loop
            while True:
                # Get user input
                user_input = input("\nEnter a prompt (or 'exit' to quit): ")
                
                if user_input.lower() == 'exit':
                    break
                
                print("Calling LLM through MCP...")
                
                # Call the tool with the user's input
                result = await session.call_tool("query_llm", {"prompt": user_input})
                
                # Print the result
                print("\nResponse:", result.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
```

### Key Concepts in Example 1

- **FastMCP Server**: Provides a high-level interface for creating MCP servers
- **Tool Registration**: Using Python decorators to register functions as MCP tools
- **Standard I/O Transport**: Communication via stdio for a simple process-based setup
- **ClientSession**: Managing the connection and protocol communication
- **Tool Discovery**: Listing available tools on the server
- **Tool Execution**: Calling a tool and processing its result

## Example 2: Knowledge Base Management System

Now let's build a more complex system that manages a text-based knowledge base with multiple features.

### Knowledge Base Server

```python
# rick_server.py
import os
from mcp.server.fastmcp import FastMCP, Context

# Create the server
mcp = FastMCP("RickKnowledgeBase")

# Path to Rick's knowledge base
KB_PATH = "Ricks_KB.txt"

# Helper functions
def read_kb():
    """Read the knowledge base file"""
    if not os.path.exists(KB_PATH):
        return "Knowledge base not found"
    with open(KB_PATH, 'r') as f:
        return f.read()

def write_kb(content):
    """Write to the knowledge base file"""
    with open(KB_PATH, 'w') as f:
        f.write(content)
    return "Knowledge base updated successfully"

# Resource to access the knowledge base
@mcp.resource("rickskb://main")
def get_kb() -> str:
    """Get Rick's entire knowledge base"""
    return read_kb()

@mcp.resource("rickskb://section/{section_number}")
def get_kb_section(section_number: str) -> str:
    """Get a specific section from Rick's knowledge base"""
    kb_content = read_kb()
    
    # Find the section
    try:
        section_num = int(section_number)
        section_header = f"{section_num}. "
        
        # Split by sections and find the requested one
        sections = kb_content.split("\n\n")
        for i, section in enumerate(sections):
            if section.strip().startswith(section_header):
                # Return this section and its content until the next section
                if i < len(sections) - 1:
                    return section
                else:
                    return section
                    
        return f"Section {section_number} not found"
    except ValueError:
        return f"Invalid section number: {section_number}"

# Tools to interact with the knowledge base
@mcp.tool()
def query_kb(query: str) -> str:
    """Query Rick's knowledge base using the local LLM"""
    from llama_cpp import Llama
    
    kb_content = read_kb()
    
    # Load the model
    model_path = "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    model = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=4
    )
    
    # Format the prompt for TinyLlama
    formatted_prompt = f"""<|system|>
You are Rick Sanchez's AI assistant. You have access to his knowledge base.
Use the knowledge base to answer questions accurately in Rick's characteristic tone.
Knowledge base:
{kb_content}</s>
<|user|>
{query}</s>
<|assistant|>
"""
    
    # Generate completion
    output = model.create_completion(
        prompt=formatted_prompt,
        max_tokens=512,
        temperature=0.7,
        stop=["<|user|>", "</s>"]
    )
    
    # Return the generated text
    return output['choices'][0]['text']

@mcp.tool()
def add_to_kb(section: int, entry: str) -> str:
    """Add a new entry to a section in Rick's knowledge base"""
    kb_content = read_kb()
    lines = kb_content.split('\n')
    
    # Find the section
    section_header = f"{section}. "
    section_found = False
    section_end = None
    
    for i, line in enumerate(lines):
        if line.strip().startswith(section_header):
            section_found = True
            
        # Check if we've found the section and are now at the next section or the end
        elif section_found and (line.strip().startswith(f"{section+1}. ") or i == len(lines)-1):
            section_end = i
            break
    
    if not section_found:
        return f"Section {section} not found"
    
    if section_end:
        # Insert the new entry before the next section
        lines.insert(section_end, f"- {entry}")
    else:
        # Add to the end of the file
        lines.append(f"- {entry}")
    
    # Write back to the file
    write_kb('\n'.join(lines))
    return f"Added entry to section {section}: {entry}"

@mcp.tool()
def create_section(title: str) -> str:
    """Create a new section in Rick's knowledge base"""
    kb_content = read_kb()
    
    # Count existing sections to determine the new section number
    section_count = 0
    for line in kb_content.split('\n'):
        if line.strip() and line[0].isdigit() and '. ' in line:
            section_count += 1
    
    # Create new section
    new_section = f"\n\n{section_count + 1}. {title.upper()}"
    
    # Append to knowledge base
    write_kb(kb_content + new_section)
    return f"Created new section: {section_count + 1}. {title.upper()}"

# Run the server
if __name__ == "__main__":
    mcp.run()
```

### Knowledge Base Client

```python
# rick_client.py
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Create server parameters for stdio connection
    server_params = StdioServerParameters(
        command="python",
        args=["rick_server.py"],
    )
    
    # Connect to the server
    print("Connecting to Rick's Knowledge Base server...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            
            # List available tools
            tools_result = await session.list_tools()
            tool_names = [tool.name for tool in tools_result.tools]
            print(f"Available tools: {tool_names}")
            
            # List available resources
            resources_result = await session.list_resources()
            resource_names = [resource.uri for resource in resources_result.resources]
            print(f"Available resources: {resource_names}")
            
            # Main interaction loop
            while True:
                print("\n--- RICK'S KNOWLEDGE BASE INTERFACE ---")
                print("1. View entire knowledge base")
                print("2. View a specific section")
                print("3. Query the knowledge base with LLM")
                print("4. Add entry to a section")
                print("5. Create a new section")
                print("6. Exit")
                
                choice = input("\nEnter your choice (1-6): ")
                
                if choice == '1':
                    # Read the entire knowledge base
                    print("\nReading full knowledge base...")
                    resource_result = await session.read_resource("rickskb://main")
                    # Extract the text content from the first content item
                    kb_content = resource_result.contents[0].text
                    print("\n" + kb_content)
                    
                elif choice == '2':
                    # Read a specific section
                    section = input("Enter section number: ")
                    print(f"\nReading section {section}...")
                    resource_result = await session.read_resource(f"rickskb://section/{section}")
                    # Extract the text content from the first content item
                    section_content = resource_result.contents[0].text
                    print("\n" + section_content)
                    
                elif choice == '3':
                    # Query the knowledge base
                    query = input("Enter your query for Rick's knowledge base: ")
                    print("\nProcessing query with LLM...")
                    result = await session.call_tool("query_kb", {"query": query})
                    print("\nRick's AI says:", result.content[0].text)
                    
                elif choice == '4':
                    # Add entry to a section
                    section = input("Enter section number: ")
                    entry = input("Enter new entry: ")
                    print("\nAdding entry...")
                    result = await session.call_tool("add_to_kb", {"section": int(section), "entry": entry})
                    print("\nResult:", result.content[0].text)
                    
                elif choice == '5':
                    # Create a new section
                    title = input("Enter new section title: ")
                    print("\nCreating section...")
                    result = await session.call_tool("create_section", {"title": title})
                    print("\nResult:", result.content[0].text)
                    
                elif choice == '6':
                    print("Exiting Rick's Knowledge Base Interface...")
                    break
                    
                else:
                    print("Invalid choice, please try again")
                
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    asyncio.run(main())
```

### Key Concepts in Example 2

- **Resources**: Data sources exposed through URI templates
- **Parameterized Resources**: Using URI parameters to access specific parts of data
- **Multiple Tools**: Implementing several different tools with distinct purposes
- **File I/O**: Reading from and writing to files through MCP
- **Complex Context Management**: Using the LLM with context from a knowledge base
- **Response Handling**: Properly extracting and processing different response types

## Core MCP Concepts Explained

### 1. MCP Servers

MCP servers expose functionality to clients through three main primitives:

| Primitive | Control               | Description                                         | Example Use                  |
|-----------|-----------------------|-----------------------------------------------------|------------------------------|
| Prompts   | User-controlled       | Interactive templates invoked by user choice        | Slash commands, menu options |
| Resources | Application-controlled| Contextual data managed by the client application   | File contents, API responses |
| Tools     | Model-controlled      | Functions exposed to the LLM to take actions        | API calls, data updates      |

In our examples, we've used the `FastMCP` class to create servers, which simplifies the process of creating and running an MCP server.

### 2. Transport Layers

MCP supports different transport mechanisms:

- **Standard I/O (stdio)**: Process-based communication
- **Server-Sent Events (SSE)**: HTTP-based streaming
- **WebSocket**: Bidirectional communication

Our examples use stdio transport, which is simple and effective for local development.

### 3. Resources

Resources represent data that can be accessed by clients. They are:

- Identified by URIs
- Can be static or dynamic
- Can accept parameters in their URIs
- Return data in a standardized format
- Read-only (they don't modify state)

In our knowledge base example, we defined two resources:
- `rickskb://main`: Returns the entire knowledge base
- `rickskb://section/{section_number}`: Returns a specific section

### 4. Tools

Tools are functions that can be executed by clients. They:

- Have names and descriptions
- Accept structured input parameters
- Can perform arbitrary computations
- Can modify state
- Return results in a standardized format

Our knowledge base example has three tools:
- `query_kb`: Uses the LLM to answer questions about the knowledge base
- `add_to_kb`: Adds a new entry to a section
- `create_section`: Creates a new section

### 5. MCP Clients

MCP clients connect to servers and interact with their exposed functionality. They:

- Establish and maintain connections
- Discover available resources and tools
- Access resources and execute tools
- Process and present results

Our client examples demonstrate:
- Connection establishment with error handling
- Resource and tool discovery
- Resource access
- Tool execution
- User interface integration

## Common Patterns and Best Practices

### Code Organization

1. **Separation of concerns**: Keep transport, server logic, and business logic separate
2. **Helper functions**: Extract common functionality into helper functions
3. **Error handling**: Implement comprehensive error handling
4. **Documentation**: Document tools and resources thoroughly
5. **Resource naming**: Use clear, consistent URI patterns

### Resource Design

1. **URI templates**: Use parameterized URIs for flexible resource access
2. **Resource granularity**: Balance between fine-grained and coarse-grained resources
3. **MIME types**: Specify correct MIME types for resources
4. **Error responses**: Return clear error messages when resources cannot be accessed

### Tool Design

1. **Input validation**: Validate tool parameters before execution
2. **Error handling**: Handle and report errors gracefully
3. **Statelessness**: Design tools to be as stateless as possible
4. **Idempotence**: Make tools idempotent when possible
5. **Documentation**: Provide clear descriptions and parameter documentation

## Running MCP Servers

You can run MCP servers in several ways:

### Direct Execution

```bash
python my_server.py
```

### Using the MCP CLI

```bash
# Run in development mode with the inspector
mcp dev my_server.py

# Install in Claude Desktop
mcp install my_server.py --name "My Server"
```

### Mounting to an Existing ASGI Server

```python
from starlette.applications import Starlette
from starlette.routing import Mount
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My App")

# Mount the SSE server to the existing ASGI server
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)
```

## Conclusion

MCP provides a powerful framework for integrating LLMs with various data sources and tools. By standardizing the interaction patterns, it enables secure, flexible, and extensible AI applications.

The examples in this tutorial demonstrate how to:

1. Create simple and complex MCP servers
2. Implement resources and tools
3. Connect clients to servers
4. Integrate with local LLMs
5. Build interactive applications

As you continue exploring MCP, consider these advanced topics:

- Resource subscriptions for real-time updates
- Prompt templates for standardized interactions
- Transport security for remote connections
- Authentication and authorization
- Versioning and compatibility

## Further Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP Specification](https://spec.modelcontextprotocol.io)
- [Python SDK Repository](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Server Examples](https://github.com/modelcontextprotocol/servers)
