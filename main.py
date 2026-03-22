import os
import instructor
from litellm import completion
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List

load_dotenv()


# 1. Define the Structured Output (Your Team's Criteria)
class LeadAnalysis(BaseModel):
    scam_likelihood: int = Field(description="0-100 score. 100 is definitely a scam.")
    budget_fit: int = Field(ge=1, le=10, description="Alignment with user's ideal wage.")
    scope_clarity: int = Field(ge=1, le=10, description="How well defined the task is.")
    timeline_reasonable: bool = Field(description="Is the deadline realistic?")
    red_flags: List[str] = Field(description="Specific concerns about the client or project.")
    summary: str = Field(description="2-sentence neutral overview of the request.")
    suggested_reply_type: str = Field(description="Options: 'Reject', 'Clarify', 'Accept'")


# 2. Patch LiteLLM with Instructor
client = instructor.from_litellm(completion)


def analyze_lead(email_content, user_preferences):
    try:
        # 3. Call the AI with the Pydantic model
        response = client.chat.completions.create(
            model="gemini/gemini-3.1-flash-lite-preview",
            response_model=LeadAnalysis,
            messages=[
                {"role": "system",
                 "content": "You are a professional freelance lead triage agent. Use straightforward language without trivializing details."},
                {"role": "user", "content": f"""
                    USER PREFERENCES:
                    {user_preferences}

                    EMAIL TO ANALYZE:
                    {email_content}
                """}
            ]
        )
        return response
    except Exception as e:
        print(f"Analysis failed: {e}")
        return None


if __name__ == "__main__":
    # Example Test Case
    test_email = "Hey, I need a website by tomorrow. My budget is $50 and I need it to be exactly like Amazon."
    my_settings = "Ideal wage: $100/hr. Minimum budget: $2000. Timeline: 2+ weeks."

    result = analyze_lead(test_email, my_settings)

    if result:
        print(f"Scam Risk: {result.scam_likelihood}%")
        print(f"Budget Score: {result.budget_fit}/10")
        print(f"Red Flags: {', '.join(result.red_flags)}")
        print(f"Summary: {result.summary}")