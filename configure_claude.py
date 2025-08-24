import json
import os
import sys
import platform
from pathlib import Path

# Install colorama if not available
try:
    from colorama import init, Fore, Style
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_success(text):
    print(f"{Fore.GREEN}✅ {text}")

def print_warning(text):
    print(f"{Fore.YELLOW}⚠️  {text}")

def print_error(text):
    print(f"{Fore.RED}❌ {text}")

def print_info(text):
    print(f"{Fore.BLUE}ℹ️  {text}")

def print_header(text):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}🎯 {text}")
    print(f"{Fore.CYAN}{'=' * 50}")

# ... rest of configure_claude.py functions with colored prints ...

def main():
    print_header("Configuring Claude Desktop for GitTimeMachine")
    
    try:
        claude_config_path = get_claude_config_path()
        print_info(f"Claude config path: {claude_config_path}")
        
        if not verify_installation():
            print_error("Package not properly installed. Run: pip install -e .")
            return False
        
        config_path = create_claude_config()
        print_success(f"Claude config created/updated: {config_path}")
        
        print_header("Configuration Summary")
        print_info("MCP Server: git-time-machine")
        print_info("Command: python -m GTM.server")
        print_info("Working directory: {get_current_script_path()}")
        
        print_header("Next Steps")
        print_info("1. Restart Claude Desktop completely")
        print_info("2. Use: set_repository_path('your/repo/path')")
        print_info("3. Ask: 'What's the history of myfile.py?'")
        
        return True
        
    except Exception as e:
        print_error(f"Configuration failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
