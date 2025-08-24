import os
from typing import Optional

def find_git_root(start_path: str = ".") -> Optional[str]:
    """Find the root directory of the git repository."""
    current_path = os.path.abspath(start_path)
    
    while True:
        if os.path.exists(os.path.join(current_path, ".git")):
            return current_path
        
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            return None  
        current_path = parent_path

def validate_file_path(file_path: str, repo_root: str) -> bool:
    """Check if file exists within the repository."""
    full_path = os.path.join(repo_root, file_path)

    return os.path.exists(full_path) and os.path.isfile(full_path)
