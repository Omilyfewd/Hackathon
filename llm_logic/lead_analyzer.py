from pathlib import Path
from typing import List

import instructor
import litellm
from dotenv import load_dotenv
from pydantic import BaseModel, Field

try:
    from llm_logic.logger import log_raw_response
except ModuleNotFoundError:
    from logger import log_raw_response

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / "keys_and_tokens" / ".env")


class LeadAnalysis(BaseModel):
    scam_likelihood: int = Field(description="0-100 score. 100 is definitely a scam.")
    budget_fit: int = Field(ge=1, le=10, description="Alignment with user's ideal wage.")
    scope_clarity: int = Field(ge=1, le=10, description="How well defined the task is.")
    timeline_reasonable: bool = Field(description="Is the deadline realistic?")
    red_flags: List[str] = Field(description="Specific concerns about the client or project.")
    summary: str = Field(description="2-sentence neutral overview of the request.")
    suggested_reply_type: str = Field(description="Options: 'Reject', 'Clarify', 'Accept'")


client = instructor.from_litellm(litellm.completion)


def analyze_lead(email_content, user_preferences):
    try:
        response = client.chat.completions.create(
            model="gemini/gemini-3.1-flash-lite-preview",
            response_model=LeadAnalysis,
            max_retries=3,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional freelance lead triage agent. Use straightforward language without trivializing details.",
                },
                {
                    "role": "user",
                    "content": f"""
                    USER PREFERENCES:
                    {user_preferences}

                    EMAIL TO ANALYZE:
                    {email_content}
                """,
                },
            ],
        )

        log_raw_response(response)
        return response
    except Exception as e:
        print(f"Analysis failed: {e}")
        return None
