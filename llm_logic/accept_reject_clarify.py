import json
from pathlib import Path
from typing import List, Literal, Union

import instructor
import litellm
from dotenv import load_dotenv
from pydantic import BaseModel, Field

try:
    from llm_logic.logger import log_complete_response, load_latest_logged_response
except ModuleNotFoundError:
    from logger import log_complete_response, load_latest_logged_response

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / "keys_and_tokens" / ".env")


class LeadAnalysisAccepted(BaseModel):  # user will edit
    suggested_reply_type: Literal["Accept"] = Field(
        description="Always 'Accept' for accepted leads."
    )
    deliverable_timeline: List[str] = Field(description="Break the project down into different phases, and provide a "
                                                        "specific date for the time of each "
                                                        "completion.")
    total_time: int = Field(ge=0, description="Total time in hours to complete the project. This is the number to be "
                                              "added to the current workload in hours.")
    estimated_cost: int = Field(description="Total cost of the freelance service in US dollars. This is the revenue "
                                            "the freelancer will make from this service.")
    deposit_amount: int = Field(description="Required upfront payment")
    required_assets: List[str] = Field(description="Items needed from client")
    subject: str = Field(
        description="Email subject line using [[brackets]] for values the freelancer must manually",
        examples=["Project Kickoff: [[Website Redesign]] – [[Alex Rivera]]",
                  "Project Confirmation: [[Email Marketing Campaign]] – [[Morgan Taylor]]"]
    )
    order_confirmation_template: str = Field(
        description="A full acceptance email draft using [[brackets]] for values the freelancer must manually."
                    "confirm, like price or dates.",
        examples=[
        """
            Hi [[Jordan]],
            
            I’m excited to officially get started on the website redesign for Apex Solutions! Following our discussion yesterday, I’ve outlined the project details below to ensure we are aligned on the path forward.
            
            Project Scope & Deliverables
            Full Redesign: A [[5-page]] responsive [[WordPress]] website (Home, About, Services, Case Studies, Contact).
            SEO Setup: Basic on-page SEO optimization for all new pages.
            Contact Integration: Setup of a custom contact form linked to your CRM.
            Revisions: Up to [[two rounds]] of design adjustments based on your feedback.
            
            Project Timeline
            [[April 1st]]: Project Kickoff & Discovery.
            [[April 8th]]: Initial wireframes and design mockups delivered for review.
            [[April 15th]]: Development phase completed on the staging site.
            [[April 20th]]: Final QA testing and site launch.
            
            Logistics & Communication
            Investment: The total project fee is [[$2,000]]. A [[50%]] commencement deposit ([[$1,000]]) is required to secure this window on my calendar.
            Status Updates: I will send a brief progress report every [[Friday afternoon]] via [[email]].
            Primary Contact: We will use email for all formal approvals, but I am available via [[Slack]] for quick daily questions.
            
            Next Steps
            Contract: Please review and digitally sign the attached Project Agreement.
            Deposit: I have attached the invoice for the [[$1,000]] deposit, payable via [[bank transfer or credit card]].
            Assets: Once the paperwork is handled, please upload your high-resolution logo and any existing brand style guides to the [[shared Google Drive folder]] I’ve set up.
            Once the deposit is confirmed and I have access to your assets, I will begin the Discovery phase on [[April 1st]].
            
            I’m looking forward to building something great for [[Apex Solutions]]!
            
            Best regards,
            
            [[Alex Rivera]]
            Web Developer & Designer
            [[www.alexriveradesign.com]]
            [[(555) 012-3456]]
        """,
        """
            Hi [[Casey]],

            I’m thrilled to officially begin work on the [[Email Marketing Campaign]] for [[Luminary Labs]]. Below is a quick summary of our agreed-upon terms and the immediate next steps.

            Project Terms
            Scope: Creation of [[four]] custom email templates and a [[3-week]] automated sequence.
            Timeline: Work begins on [[May 12th]], with the final sequence ready for launch by [[June 2nd]].
            Investment: The total project fee is [[$1,200]].
            Payment: A [[30%]] upfront deposit of [[$360]] is required via [[PayPal or Stripe]] to secure the start date.
            
            Next Steps
            Agreement: Please sign the attached [[Service Agreement]] and return it at your earliest convenience.
            Deposit: I have included the invoice for [[$360]] alongside this email.
            Onboarding: Once the deposit is received, I will send over a [[Typeform]] link to gather your brand voice guidelines and target audience data.
            
            I am looking forward to a successful collaboration!
            
            Best regards,
            
            [[Morgan Taylor]]
            [[Copywriter & Strategist]]
            [[www.morgantaylorwrites.com]]
            [[(555) 987-6543]]
        """]
    )


class LeadAnalysisRejected(BaseModel):
    suggested_reply_type: Literal["Reject"] = Field(
        description="Always 'Reject' for rejected leads."
    )
    rejection_category: str = Field(
        description="The primary reason for rejection (e.g., 'Budget too low', 'Timeline impossible', 'Out of Scope', 'High Scam Risk', 'Capacity Full')."
    )
    internal_logic: str = Field(
        description="A brief 1-sentence internal explanation of why this lead doesn't meet the freelancer's specific criteria."
    )
    fit_score: int = Field(
        ge=0, le=5,
        description="A low-range score (0-5) representing how far off this client was from the ideal profile."
    )
    alternative_resources: List[str] = Field(
        description="Generic resources or platforms to suggest to the client (e.g., 'Upwork', 'Fiverr', 'a specialized agency') so the rejection remains helpful."
    )
    subject: str = Field(
        description="A professional, neutral email subject line using [[brackets]] for values the freelancer must manually confirm.",
        examples=["Inquiry Update: [[Project Name]] – [[Freelancer Name]]",
                  "Regarding your request for [[Service Type]]"]
    )
    rejection_email_template: str = Field(
        description="A polite rejection email draft using [[brackets]] for values the freelancer must manually confirm. "
                    "The tone should be professional and firm but helpful.",
        examples=[
            """
                Hi [[Jordan]],
                
                Thank you so much for reaching out and sharing the details regarding the [[Website Redesign]] for [[Apex Solutions]].
                After reviewing the project scope and the requested timeline of [[one week]], I’ve determined that I won’t be able to take this on at this time. To ensure the highest quality of work for my clients, I only accept projects where the timeline allows for a full discovery and testing phase, which typically requires a minimum of [[four weeks]].
                I would recommend looking into [[specialized WordPress agencies]] or platforms like [[Clutch.co]] to find a partner who might have the immediate bandwidth for a rapid turnaround.
                I wish you the best of luck with the launch of [[Apex Solutions]]!

                Best regards,
    
                [[Alex Rivera]]
            """,
            """
                Hi [[Casey]],
    
                I appreciate you thinking of me for the [[Email Marketing Campaign]] at [[Luminary Labs]]. 
                Based on the project requirements and the budget range of [[$200]] you mentioned, it looks like our current service packages aren't quite the right fit for this specific initiative. My minimum engagement for custom strategy and execution currently begins at [[$1,200]].
                Because I want to make sure you get the best results for your current stage, I'd suggest checking out [[Upwork]] or [[the Shopify Expert Marketplace]], where you can often find talented specialists who work with smaller-scale project budgets.
                Thank you again for the inquiry, and I hope the campaign is a great success!
    
                Best,
    
                [[Morgan Taylor]]
            """]
    )


class LeadAnalysisClarification(BaseModel):
    suggested_reply_type: Literal["Clarify"] = Field(
        description="Always 'Clarify' when more information is required."
    )
    missing_information: List[str] = Field(
        description="List of specific details missing from the inquiry (e.g., 'Budget', 'Technical Stack', 'Deadline')."
    )
    uncertainty_score: int = Field(
        ge=1, le=10,
        description="Score of 1-10 on how vague the request is. 10 is 'I have no idea what they want'."
    )
    clarification_priority: str = Field(
        description="How urgent is this lead if the info is right? (High, Medium, Low)."
    )
    subject: str = Field(
        description="A professional subject line using [[brackets]] for manual confirmation.",
        examples=["Quick question regarding your [[Project Name]] inquiry",
                  "Following up on your request for [[Service Type]]"]
    )
    clarification_email_template: str = Field(
        description="A polite follow-up email asking for the missing details using [[brackets]].",
        examples=[
            """
                Hi [[Jordan]],
    
                Thanks for reaching out about the [[Website Project]]! It sounds like an interesting initiative.
    
                To help me give you an accurate estimate and check my availability, could you clarify a few details? Specifically, I'd love to know more about:
                - The ideal [[launch date]] you have in mind.
                - The [[budget range]] allocated for this phase of the work.
                - Any existing [[technical documentation or brand assets]] you already have ready.
    
                Once I have a better sense of the scope, I can let you know if I'm the right fit to help you move this forward.
    
                Best regards,
    
                [[Alex Rivera]]
            """]
    )


LeadReplyResponse = Union[
    LeadAnalysisAccepted,
    LeadAnalysisRejected,
    LeadAnalysisClarification,
]

REPLY_TYPE_TO_MODEL = {
    "Accept": LeadAnalysisAccepted,
    "Reject": LeadAnalysisRejected,
    "Clarify": LeadAnalysisClarification,
}


client = instructor.from_litellm(litellm.completion)


def load_latest_analysis_entry():
    latest_entry = load_latest_logged_response()
    if not latest_entry:
        return None

    if latest_entry.get("arguments", {}).get("suggested_reply_type") in REPLY_TYPE_TO_MODEL:
        return latest_entry

    return None


def load_latest_background_context():
    latest_entry = load_latest_analysis_entry()
    if latest_entry is None:
        return "No prior lead analysis context available."

    return json.dumps(latest_entry, indent=2)


def load_latest_suggested_reply_type():
    latest_entry = load_latest_analysis_entry()
    if latest_entry is None:
        return None

    return latest_entry.get("arguments", {}).get("suggested_reply_type")


def write_client_reply(
    user_settings,
    background_context=None,
    suggested_reply_type=None,
    lead_analysis_entry=None,
    email_details=None,
):
    if lead_analysis_entry is not None:
        if background_context is None:
            background_context = json.dumps(lead_analysis_entry, indent=2)
        if suggested_reply_type is None:
            suggested_reply_type = lead_analysis_entry.get("arguments", {}).get("suggested_reply_type")

    if background_context is None:
        background_context = load_latest_background_context()

    if suggested_reply_type is None:
        suggested_reply_type = load_latest_suggested_reply_type()

    if suggested_reply_type not in REPLY_TYPE_TO_MODEL:
        print("Client reply generation failed: no valid suggested_reply_type found in llm_log.json")
        return None

    target_model_name = REPLY_TYPE_TO_MODEL[suggested_reply_type].__name__

    try:
        response = client.chat.completions.create(
            model="gemini/gemini-3.1-flash-lite-preview",
            response_model=LeadReplyResponse,
            max_retries=3,
            temperature=0.2,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional freelance email response agent. "
                        "Choose exactly one response schema based on the latest lead-analysis verdict. "
                        "Use LeadAnalysisAccepted for Accept, LeadAnalysisRejected for Reject, "
                        "and LeadAnalysisClarification for Clarify. "
                        "Write a polished client-facing email and populate the chosen schema completely. "
                        "Use [[brackets]] for values the freelancer must still confirm."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""
                    USER PREFERENCES:
                    {user_settings}

                    LATEST VERDICT:
                    {suggested_reply_type}

                    REQUIRED RESPONSE MODEL:
                    {target_model_name}

                    BACKGROUND CONTEXT:
                    {background_context}
                """,
                },
            ],
        )

        log_complete_response(
            response,
            response_model=LeadReplyResponse,
            email_details=email_details,
            lead_analysis_entry=lead_analysis_entry,
        )
        return response
    except Exception as e:
        print(f"Client reply generation failed: {e}")
        return None
