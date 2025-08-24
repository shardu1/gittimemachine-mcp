#!/usr/bin/env python3
"""
One-click installation and configuration script with colored output.
"""

import subprocess
import sys
import os
from pathlib import Path

# Install colorama if not available
try:
    from colorama import init, Fore, Style
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_header(text):
    """Print a header with colored formatting."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}🎯 {text}")
    print(f"{Fore.CYAN}{'=' * 60}")

def print_success(text):
    """Print success message."""
    print(f"{Fore.GREEN}✅ {text}")

def print_warning(text):
    """Print warning message."""
    print(f"{Fore.YELLOW}⚠️  {text}")

def print_error(text):
    """Print error message."""
    print(f"{Fore.RED}❌ {text}")

def print_info(text):
    """Print info message."""
    print(f"{Fore.BLUE}ℹ️  {text}")

def print_step(text):
    """Print step message."""
    print(f"{Fore.MAGENTA}🔧 {text}")

def run_command(command, description):
    """Run a shell command with error handling."""
    print_step(f"{description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print_error(f"Failed: {result.stderr.strip() or 'Unknown error'}")
            return False
        print_success("Completed successfully")
        return True
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def check_prerequisites():
    """Check if Python and pip are available."""
    print_header("Checking Prerequisites")
    
    # Check Python version
    try:
        python_version = sys.version.split()[0]
        print_info(f"Python version: {python_version}")
        if tuple(map(int, python_version.split('.'))) < (3, 8):
            print_error("Python 3.8 or higher is required")
            return False
    except Exception:
        print_error("Could not determine Python version")
        return False
    
    # Check pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      capture_output=True, check=True)
        print_success("pip is available")
    except subprocess.CalledProcessError:
        print_error("pip is not available")
        return False
    
    return True

def main():
    """Main installation function."""
    print_header("GitTimeMachine One-Click Installation")
    print_info("This script will install and configure GitTimeMachine MCP Server")
    
    # Check prerequisites
    if not check_prerequisites():
        print_error("Prerequisite check failed")
        return False
    
    # Step 1: Install package
    print_header("Step 1: Installing Package")
    if not run_command(f"{sys.executable} -m pip install -e .", "Installing package"):
        print_error("Package installation failed")
        return False
    
    # Step 2: Configure Claude
    print_header("Step 2: Configuring Claude Desktop")
    configure_script = Path(__file__).parent / "configure_claude.py"
    
    if configure_script.exists():
        if not run_command(f"{sys.executable} configure_claude.py", "Configuring Claude"):
            print_warning("Claude configuration failed, but package is installed")
            print_info("You can manually run: python configure_claude.py")
    else:
        print_warning("configure_claude.py not found - skipping configuration")
        print_info("You'll need to configure Claude manually")
    
    # Success message
    print_header("Installation Complete!")
    print_success("GitTimeMachine has been successfully installed!")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}🎯 Next steps:")
    print(f"{Fore.WHITE}   1. {Fore.YELLOW}Restart Claude Desktop{Fore.WHITE} completely")
    print(f"{Fore.WHITE}   2. {Fore.YELLOW}Set your repository{Fore.WHITE}: set_repository_path('your/repo/path')")
    print(f"{Fore.WHITE}   3. {Fore.YELLOW}Ask about history{Fore.WHITE}: 'What's the history of myfile.py?'")
    print(f"{Fore.WHITE}   4. {Fore.YELLOW}Explore files{Fore.WHITE}: list_repository_files()")
    
    print(f"\n{Fore.GREEN}💡 Pro tip: Use {Fore.YELLOW}gittm-configure{Fore.GREEN} to reconfigure anytime!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}🎉 All done! Happy coding! 🚀")
        else:
            print(f"\n{Fore.RED}{Style.BRIGHT}💥 Installation failed. Please check the errors above.")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Fore.RED}🚫 Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Fore.RED}💥 Unexpected error: {e}")
        sys.exit(1)
