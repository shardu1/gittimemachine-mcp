#!/usr/bin/env python3
"""
GitTimeMachine MCP Server - AI-powered git history analysis for AI assistants.
"""

from fastmcp import FastMCP
from .tools.git_tools import GitTools
from .tools.llm_tools import LLMTools
from .utils.logging_setup import setup_logging
import os
import sys

# Initialize FastMCP
mcp = FastMCP("git-time-machine")

# Global variables
git_tools = None
llm_tools = LLMTools()
logger = setup_logging()

@mcp.tool()
def set_repository_path(repo_path: str) -> str:
    """
    Set the git repository path to analyze. Use this before asking about file history.
    
    Args:
        repo_path: Full path to the git repository (e.g., C:/Projects/MyRepo or /home/user/MyRepo)
    """
    global git_tools
    
    try:
        git_tools = GitTools(repo_path)
        if git_tools.repo_root:
            return f"Now analyzing repository: {git_tools.repo_root}"
        else:
            return "Not a valid git repository. Please check the path."
            
    except Exception as e:
        return f"Error setting repository: {str(e)}"
    
@mcp.tool()
def get_file_history(file_path: str, line_number: int = None, user_question: str = None) -> str:
    """Get the git commit history for a file or line number with intelligent summarization."""
    global git_tools
    
    if not git_tools or not git_tools.repo_root:
        return "❌ No repository selected. Please use set_repository_path() first to specify which git repository to analyze."
    
    # Check if file exists in the repository
    full_path = os.path.join(git_tools.repo_root, file_path)
    if not os.path.exists(full_path):
        return f"❌ File not found in repository: {file_path}\nRepository root: {git_tools.repo_root}"
    
    success, result = git_tools.get_file_history(file_path, line_number)
    if not success:
        return result
    
    # Add LLM summarization if available
    if llm_tools.is_llm_available() and len(result.split('\n')) > 3:
        summary = llm_tools.summarize_git_history(result, user_question or "What changed in this file?")
        return summary
    
    return result

@mcp.tool()
def get_previous_version(file_path: str, commit_hash: str) -> str:
    """Get what a file looked like at a previous commit."""
    global git_tools
    
    if not git_tools or not git_tools.repo_root:
        return "Not in a git repository"

    success, result = git_tools.get_previous_version(file_path, commit_hash)
    if not success:
        return result
    
    return f"File content at commit {commit_hash}:\n\n{result}"

@mcp.tool()
def get_blame_info(file_path: str, line_number: int = None) -> str:
    """See who last modified each line of a file and when."""
    global git_tools
    
    if not git_tools or not git_tools.repo_root:
        return "Not in a git repository"

    success, result = git_tools.get_blame_info(file_path, line_number)
    if not success:
        return result
    
    return result

@mcp.tool()
def get_current_repository() -> str:
    """Get the currently selected git repository path."""
    global git_tools
    if git_tools and git_tools.repo_root:
        return f"Current repository: {git_tools.repo_root}"
    return "No repository selected. Use set_repository_path() first."

@mcp.tool()
def list_repository_files() -> str:
    """List all files in the current repository."""
    global git_tools
    if not git_tools or not git_tools.repo_root:
        return "No repository selected. Use set_repository_path() first."
    
    try:
        files = []
        for root, dirs, filenames in os.walk(git_tools.repo_root):
            # Skip .git directories completely
            if '.git' in root.split(os.sep):
                continue
                
            for filename in filenames:
                # Skip hidden files and .git files
                if not filename.startswith('.'):
                    rel_path = os.path.relpath(os.path.join(root, filename), git_tools.repo_root)
                    files.append(rel_path)
        
        if files:
            # Sort alphabetically for better readability
            files.sort()
            file_list = "\n".join(files[:50])  # Show first 50 files
            if len(files) > 50:
                file_list += f"\n\n... and {len(files) - 50} more files"
            return f"Found {len(files)} files in repository:\n\n{file_list}"
        else:
            return "No files found in repository (or only hidden/git files)."
            
    except Exception as e:
        return f"Error listing files: {str(e)}"

if __name__ == "__main__":
    print("=== GTM Server Starting ===", file=sys.stderr)
    print(f"Working directory: {os.getcwd()}", file=sys.stderr)
    
    # Initialize git_tools without any specific path
    # Users will set the repository dynamically using set_repository_path()
    try:
        git_tools = GitTools()
        if git_tools.repo_root:
            print(f"Using current directory repo: {git_tools.repo_root}", file=sys.stderr)
        else:
            print("Not in a git repository - use set_repository_path() to specify one", file=sys.stderr)
            
    except Exception as e:
        print(f"Git tools error: {e}", file=sys.stderr)
    
    # Run the FastMCP server
    mcp.run()