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