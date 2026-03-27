import os
import json
from pathlib import Path



# Attempt proper imports from llm_logic
try:
    from llm_logic.main import load_test_emails, load_user_settings
    from llm_logic.lead_analyzer import analyze_lead
    from llm_logic.accept_reject_clarify import (
        LeadAnalysisAccepted,
        LeadAnalysisClarification,
        LeadAnalysisRejected,
        write_client_reply,
    )
except ModuleNotFoundError:
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[1]))  # add project root
    from llm_logic.main import load_test_emails, load_user_settings
    from llm_logic.lead_analyzer import analyze_lead
    from llm_logic.accept_reject_clarify import (
        LeadAnalysisAccepted,
        LeadAnalysisClarification,
        LeadAnalysisRejected,
        write_client_reply,
    )

# Base template for the description
descriptionBase = """
Scam Likelihood: [BS]% \n
Budget Fit: [Money]/10 \n
Scope Clarity: [Clear]/10 \n
Project Fit: [Strong]/10 \n
Reasonable Timeline: [YayNay] \n
Summary: [LLM] 

Original Email:

Subject: [idkman] \n
[OG]
"""

def build_description(email, analysis):
    """
    Replace placeholders in descriptionBase with actual email and analysis info.
    """
    template = descriptionBase
    template = template.replace("[idkman]", email.get("subject", "N/A"))
    template = template.replace("[OG]", email.get("body", "N/A"))

    template = template.replace("[BS]", str(analysis.get("scam_likelihood", "N/A")))
    template = template.replace("[Money]", str(analysis.get("budget_fit", "N/A")))
    template = template.replace("[Clear]", str(analysis.get("scope_clarity", "N/A")))
    template = template.replace("[Strong]", str(analysis.get("project_fit", "N/A")))
    template = template.replace("[YayNay]", "Yes" if analysis.get("timeline_reasonable") else "No")
    template = template.replace("[LLM]", analysis.get("summary", "N/A"))

    return template

# Extract the suggested reply type from analysis dict
def get_verdict(analysis):
    return analysis.get("suggested_reply_type", "UNKNOWN")

# Extract email body from the client reply object (LLM output)
def get_return_email(client_reply):
    if client_reply:
        if hasattr(client_reply, "Accept"):
            return client_reply.order_confirmation_template
        elif hasattr(client_reply, "Reject"):
            return client_reply.rejection_email_template
        elif hasattr(client_reply, "Clarify"):
            return client_reply.clarification_email_template
    return "No reply generated"

# Main function: returns an array of arrays [verdict, description, return_email]
def consolidate():
    unread_emails = load_test_emails()
    my_settings = load_user_settings()
    results = []

    for email in unread_emails:
        # Build email text for analysis
        email_text = f"Subject: {email.get('subject', '')}\nBody: {email.get('body', '')}"

        # Run LLM analysis
        lead_analysis = analyze_lead(email_text, my_settings, email_details=email)
        if not lead_analysis:
            continue

        analysis_dict = lead_analysis.model_dump()  # convert LLM object to dict

        # Extract verdict & description
        verdict = get_verdict(analysis_dict)
        description = build_description(email, analysis_dict)

        # Generate client reply (for return email)
        lead_analysis = email.get("lead_analysis", {})
        return_email = lead_analysis.get("draft_reply")
        if not return_email:
            # fallback
            arguments = email.get("arguments", {})
            return_email = arguments.get("draft_reply", "Missing Recommended Response")

        sender_email = email.get("sender", "unknown_sender")
        # Append as [verdict, description, return_email]
        results.append([verdict, description, return_email, sender_email])

    return results

if __name__ == "__main__":
    final_array = consolidate()
    print(f"Processed {len(final_array)} emails.")
    for row in final_array:
        print("----")
        print("Verdict:", row[0])
        print("Sender: ", row[3])
        print("Return Email:", row[2])
        print("Description:\n", row[1])