from pathlib import Path
from typing import List

import instructor
import litellm
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class LeadAnalysisAccepted(BaseModel): #user will edit
    queue_time: int = Field(ge=1, le=10, description="Estimated time in days for the freelancer to start working on the user's order due to current workload.")
    estimated_cost: int = Field(description="An upper and lower bound for the estimated cost of the freelance job.")
    order_confirmation_template: int = Field(
        ge=1,
        le=10,
        description="Order confirmation letter for the freelancer, with blank spaces represented by underscores (___) for fields the user",
        examples=["""
            Dear client,

            Thank you very much for accepting my proposal. I’m really excited to start working with you on this project.
            
            Please find below the list of services that will be completed:
            [Service 1] – $ Price
            [Service 2] – $ Price
            [Service 3] – $ Price
            
            The total amount for this project will be [$X,XXX]
            
            Best regards,
            Your signature
        
        """]
    )
