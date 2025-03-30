import subprocess
import os
import sys
from pathlib import Path

def main():
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    
    # Check for the virtual environment
    venv_path = script_dir / ".venv"
    if not venv_path.exists():
        print("Virtual environment not found. Creating one...")
        subprocess.run(["uv", "venv"], cwd=script_dir, check=True)
    
    # Print usage instructions
    print("\nTinyLlama MCP Demo")
    print("=================")
    print("1. First download the model:   python download_model.py")
    print("2. Start the server:           python server.py")
    print("3. In another terminal, run:   python client.py")
    print("\nAlternatively:")
    print("- Run with inspector:          uv run mcp dev server.py")
    print("- Install in Claude:           uv run mcp install server.py\n")
    
    # Ask user what they want to run
    choice = input("What would you like to run? (download/server/client/inspector/install): ").strip().lower()
    
    if choice == "download":
        subprocess.run(["python", "download_model.py"], cwd=script_dir)
    elif choice == "server":
        subprocess.run(["python", "server.py"], cwd=script_dir)
    elif choice == "client":
        subprocess.run(["python", "client.py"], cwd=script_dir)
    elif choice == "inspector":
        subprocess.run(["uv", "run", "mcp", "dev", "server.py"], cwd=script_dir)
    elif choice == "install":
        subprocess.run(["uv", "run", "mcp", "install", "server.py"], cwd=script_dir)
    else:
        print(f"Unknown option: {choice}")

if __name__ == "__main__":
    main()