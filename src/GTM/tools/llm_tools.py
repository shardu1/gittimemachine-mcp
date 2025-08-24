import litellm
from litellm import completion
from typing import Optional
import logging

logger = logging.getLogger("gittimemachine")

class LLMTools:
    def __init__(self, model: str = "ollama/phi3:mini"):
        self.model = model
        self.api_base = "http://localhost:11434"
    
    def summarize_git_history(self, git_history: str, user_question: str) -> str:
        """Use LLM to summarize git history intelligently."""
        try:
            prompt = f"""
            Please analyze this git history and answer the user's question concisely.

            USER'S QUESTION: {user_question}

            GIT HISTORY:
            {git_history}

            Please provide a clear, concise summary focusing on the most relevant changes.
            If there are multiple commits, highlight the most significant ones.
            Explain the evolution of the code and the reasons for changes.
            """
            
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                api_base=self.api_base,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"LLM summarization failed: {e}")
            return f"Could not generate summary. Error: {str(e)}"
    
    def is_llm_available(self) -> bool:
        """Check if the LLM service is available."""
        try:
            # Simple test call
            completion(
                model=self.model,
                messages=[{"role": "user", "content": "test"}],
                api_base=self.api_base,
                max_tokens=5
            )
            return True
        except:
            return False