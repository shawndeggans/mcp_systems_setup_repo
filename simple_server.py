# simple_server.py
from mcp.server.fastmcp import FastMCP

# Create a minimal MCP server
mcp = FastMCP("MinimalLLMServer")

# Add a simple tool to query your LLM
@mcp.tool()
def query_llm(prompt: str) -> str:
    """Send a prompt to the local LLM and return its response"""
    from llama_cpp import Llama
    
    # Load the model (you may want to make this a global variable for better performance)
    model_path = "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
    model = Llama(
        model_path=model_path,
        n_ctx=2048,
        n_threads=4
    )
    
    # Format the prompt for TinyLlama
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