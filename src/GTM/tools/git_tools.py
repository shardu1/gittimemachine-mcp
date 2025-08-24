import os
from git import Repo, GitCommandError
from typing import Optional, Tuple
from ..utils.helpers import find_git_root  

class GitTools:
    def __init__(self, repo_path: str = None):
        """Initialize with optional custom repo path"""
        self.repo_root = self._find_git_root(repo_path) if repo_path else find_git_root()
        self.repo = Repo(self.repo_root) if self.repo_root else None
    
    def _find_git_root(self, start_path: str) -> Optional[str]:
        """Find git root from a specific path"""
        if not start_path:
            return None
        
        absolute_path = os.path.abspath(start_path)
        
       
        if os.path.isfile(absolute_path):
            absolute_path = os.path.dirname(absolute_path)
        
        current_path = absolute_path
        
        while True:
            if os.path.exists(os.path.join(current_path, ".git")):
                return current_path
            
            parent_path = os.path.dirname(current_path)
            if parent_path == current_path:
                return None  
            current_path = parent_path

    def get_file_history(self, file_path: str, line_number: Optional[int] = None) -> Tuple[bool, str]:
        """Get git history for a file or specific line."""
        if not self.repo_root:
            return False, "Not in a git repository"
        
        if not self.validate_file_path(file_path, self.repo_root):
            return False, f"File not found: {file_path}"
        
        try:
            if line_number:
                log_info = self.repo.git.log(
                    '-L', f'{line_number},{line_number}:{file_path}', 
                    '--pretty=format:%h - %an, %ar : %s'
                )
            else:
                log_info = self.repo.git.log('--oneline', '--', file_path)
            
            return True, log_info if log_info else "No history found"
            
        except GitCommandError as e:
            return False, f"Git command error: {str(e)}"

    def get_previous_version(self, file_path: str, commit_hash: str) -> Tuple[bool, str]:
        """Get file content at a specific commit."""
        if not self.repo_root:
            return False, "Not in a git repository"
        
        try:
            previous_content = self.repo.git.show(f'{commit_hash}:{file_path}')
            return True, previous_content
        except GitCommandError as e:
            return False, f"Error getting previous version: {str(e)}"

    def get_blame_info(self, file_path: str, line_number: Optional[int] = None) -> Tuple[bool, str]:
        """Get blame information for a file."""
        if not self.repo_root:
            return False, "Not in a git repository"
        
        try:
            blame_info = self.repo.git.blame('-w', '--line-porcelain', file_path)
            return True, blame_info
        except GitCommandError as e:
            return False, f"Error getting blame info: {str(e)}"

    def validate_file_path(self, file_path: str, repo_root: str) -> bool:
        """Check if file exists within the repository."""
        full_path = os.path.join(repo_root, file_path)

        return os.path.exists(full_path) and os.path.isfile(full_path)
