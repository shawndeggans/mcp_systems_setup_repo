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