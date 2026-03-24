from pathlib import Path
from typing import List

import instructor
import litellm
from dotenv import load_dotenv
from pydantic import BaseModel, Field


class LeadAnalysisAccepted(BaseModel): #user will edit
    queue_time: int = Field(ge=0, description="Estimated time in days for the freelancer to start working on the user's order due to current workload.")
    estimated_cost: int = Field(description="Total cost of the freelance service.")
    order_confirmation_template: int = Field(
        ge=1,
        le=10,
        description="Order confirmation letter for the freelancer, with estimated price of services.",
        examples=["""
            Dear client,

            Thank you very much for accepting my proposal. I’m really excited to start working with you on this project.
            
            Please find below the list of services that will be completed:
            [Music ] – $799.99
            [Videography] – $
            [Service 3] – $ Price
            
            The total amount for this music video will be [$X,XXX]
            Please visit the website 
            
            Best regards,
            Your signature
        
        """]
    )
