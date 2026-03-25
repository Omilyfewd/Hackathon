from pathlib import Path
from typing import List

import instructor
import litellm
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class LeadAnalysisAccepted(BaseModel): #user will edit
    queue_time: int = Field(ge=-1, description="Estimated time in days for the freelancer to start working on the "
                                               "user's order due to current workload and working hours based on ideal"
                                               " start time and end time.")
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
