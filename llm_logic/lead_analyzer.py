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
    # --- Existing Fields ---
    scam_likelihood: int = Field(description="0-100 score. 100 is definitely a scam.")
    budget_fit: int = Field(ge=1, le=10, description="Alignment with user's ideal wage.")
    scope_clarity: int = Field(ge=1, le=10, description="How well defined the task is.")
    timeline_reasonable: bool = Field(description="Is the deadline realistic?")
    red_flags: List[str] = Field(description="Specific concerns about the client or project.")
    summary: str = Field(description="2-sentence neutral overview of the request.")
    suggested_reply_type: Literal["Reject", "Clarify", "Accept"] = Field(description="The chosen workflow path.")

    # --- NEW: Information Extraction Fields ---
    client_name: str = Field(default="there", description="The name of the sender. Use 'there' if not found.")
    company_name: Optional[str] = Field(description="The name of the client's company or project.")

    # For Acceptance/Scope Recap
    extracted_goals: List[str] = Field(description="The top 3 specific goals or features the client wants built.")
    technical_requirements: List[str] = Field(
        description="Specific tools, languages, or platforms mentioned (e.g. Python, Shopify).")

    # For Clarification
    missing_info: List[str] = Field(
        description="List specific details missing that are needed to provide a quote (e.g. 'total page count').")

    # For Personalization
    personalization_hook: str = Field(
        description="A specific phrase or detail the client mentioned to include in the reply to show we read the email.")

    # For the Streamlit Editor
    draft_reply: str = Field(
        description="A full email draft using [[brackets]] for values the freelancer must manually confirm, like price or dates.")




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
