import sys
from llama_cpp import Llama

# Load the TinyLlama model
model_path = "models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
print(f"Loading model from {model_path}...")

# Initialize the model with basic parameters
model = Llama(
    model_path=model_path,
    n_ctx=2048,      # Context window size
    n_threads=4      # Number of CPU threads to use
)
print("Model loaded successfully")

# Simple prompt formatter for TinyLlama's chat format
def format_prompt(messages):
    prompt = ""
    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")
        
        if role == "system":
            prompt += f"<|system|>\n{content}</s>\n"
        elif role == "user":
            prompt += f"<|user|>\n{content}</s>\n"
        elif role == "assistant":
            prompt += f"<|assistant|>\n{content}</s>\n"
    
    # Add final assistant prefix for the model to continue
    prompt += "<|assistant|>\n"
    return prompt

# Start with a system message
messages = [
    {"role": "system", "content": "You are a helpful, friendly AI assistant."}
]

# Simple chat loop
print("\nChat with TinyLlama (type 'exit' to quit):")
while True:
    # Get user input
    user_input = input("\nYou: ")
    
    # Check for exit command
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    
    # Add user message to history
    messages.append({"role": "user", "content": user_input})
    
    # Format prompt and generate response
    prompt = format_prompt(messages)
    
    print("Generating response...")
    
    # Generate completion
    output = model.create_completion(
        prompt=prompt,
        max_tokens=512,
        temperature=0.7,
        stop=["<|user|>", "</s>"]
    )
    
    # Extract and display the response
    response = output['choices'][0]['text']
    print(f"\nTinyLlama: {response}")
    
    # Add assistant response to message history
    messages.append({"role": "assistant", "content": response})