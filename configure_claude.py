#!/usr/bin/env python3
"""
Automatically configure Claude Desktop for GitTimeMachine MCP Server.
Run with: python configure_claude.py
"""

import json
import os
import sys
import platform
from pathlib import Path

def get_claude_config_path():
    """Get the path to Claude's config file based on OS."""
    system = platform.system()
    
    if system == "Windows":
        return Path(os.environ["APPDATA"]) / "Claude" / "claude_desktop_config.json"
    elif system == "Darwin":  # macOS
        return Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"
    elif system == "Linux":
        return Path.home() / ".config" / "Claude" / "claude_desktop_config.json"
    else:
        raise OSError(f"Unsupported operating system: {system}")

def get_current_script_path():
    """Get the path to the current script's directory."""
    return Path(__file__).parent.absolute()

def create_claude_config():
    """Create or update Claude configuration."""
    claude_config_path = get_claude_config_path()
    project_path = get_current_script_path()
    
    # Configuration template
    config = {
        "mcpServers": {
            "git-time-machine": {
                "command": "python",
                "args": [
                    "-m",
                    "GTM.server"
                ],
                "cwd": str(project_path),
                "env": {
                    "PYTHONPATH": str(project_path / "src")
                }
            }
        }
    }
    
    # Create Claude config directory if it doesn't exist
    claude_config_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read existing config if it exists
    existing_config = {}
    if claude_config_path.exists():
        try:
            with open(claude_config_path, 'r') as f:
                existing_config = json.load(f)
        except json.JSONDecodeError:
            print("⚠️  Existing Claude config is invalid JSON, creating new config")
    
    # Merge with existing config (don't overwrite other servers)
    if "mcpServers" in existing_config:
        # Keep existing servers, add/update ours
        existing_config["mcpServers"]["git-time-machine"] = config["mcpServers"]["git-time-machine"]
        config = existing_config
    else:
        # No existing servers, use our config
        existing_config.update(config)
    
    # Write the config file
    with open(claude_config_path, 'w') as f:
        json.dump(existing_config, f, indent=2)
    
    return claude_config_path

def verify_installation():
    """Verify that the package is properly installed."""
    try:
        # Check if we can import the server
        import sys
        project_path = get_current_script_path()
        src_path = project_path / "src"
        
        if src_path.exists():
            sys.path.insert(0, str(src_path))
            try:
                from GTM.server import main
                print("✅ Server module imported successfully")
                return True
            except ImportError as e:
                print(f"❌ Could not import server: {e}")
                return False
        else:
            print("❌ src directory not found")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main configuration function."""
    print("🚀 Configuring Claude Desktop for GitTimeMachine...")
    print(f"📁 Project directory: {get_current_script_path()}")
    
    # Verify installation first
    if not verify_installation():
        print("\n❌ Please install the package first: pip install -e .")
        return False
    
    try:
        # Create the config
        config_path = create_claude_config()
        print(f"✅ Claude config created/updated: {config_path}")
        
        print("\n📋 Configuration summary:")
        print(f"   • MCP Server: git-time-machine")
        print(f"   • Command: python -m GTM.server")
        print(f"   • Working directory: {get_current_script_path()}")
        print(f"   • Python path: {get_current_script_path() / 'src'}")
        
        print("\n🎯 Next steps:")
        print("   1. Restart Claude Desktop completely")
        print("   2. Ask Claude: 'What's the history of my files?'")
        print("   3. Use: set_repository_path('your/repo/path') to select a repository")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        print(f"💡 Manual setup: Edit {get_claude_config_path()}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
