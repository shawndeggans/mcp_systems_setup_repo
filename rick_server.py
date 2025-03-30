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