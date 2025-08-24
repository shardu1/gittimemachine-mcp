from pydantic import BaseModel, Field
from typing import Optional

class FileHistoryRequest(BaseModel):
    file_path: str = Field(..., description="Path to the file relative to repo root")
    line_number: Optional[int] = Field(None, description="Specific line number to examine")
    user_question: Optional[str] = Field(None, description="The user's original question for context")

class PreviousVersionRequest(BaseModel):
    file_path: str = Field(..., description="Path to the file")
    commit_hash: str = Field(..., description="Specific commit hash to view")

class BlameRequest(BaseModel):
    file_path: str = Field(..., description="Path to the file")
    line_number: Optional[int] = Field(None, description="Specific line number")