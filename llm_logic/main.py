import json
from pathlib import Path

try:
    from llm_logic.lead_analyzer import analyze_lead
    from llm_logic.accept_reject_clarify import (
        LeadAnalysisAccepted,
        LeadAnalysisClarification,
        LeadAnalysisRejected,
        write_client_reply,
    )
except ModuleNotFoundError:
    from lead_analyzer import analyze_lead
    from accept_reject_clarify import (
        LeadAnalysisAccepted,
        LeadAnalysisClarification,
        LeadAnalysisRejected,
        write_client_reply,
    )

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LATEST_EMAIL_FILE = PROJECT_ROOT / "logs_test_outputs" / "latest_email.json"
USER_SETTINGS_FILE = PROJECT_ROOT / "frontend" / "user_settings.json"


def load_test_email() -> str:
    latest_email = json.loads(LATEST_EMAIL_FILE.read_text(encoding="utf-8"))
    subject = latest_email["subject"]
    body = latest_email["body"]
    return f"Subject: {subject}\nBody: {body}"


def load_user_settings() -> str:
    settings = json.loads(USER_SETTINGS_FILE.read_text(encoding="utf-8"))
    personal = settings.get("user_personal", {})
    technical = settings.get("user_technical", {})

    return (
        f"Email: {personal.get('email', 'N/A')}. "
        f"Website: {personal.get('website', 'N/A')}. "
        f"Current working hours: {personal.get('ideal_start', 'N/A')} to {personal.get('ideal_end', 'N/A')}. "
        f"Ideal wage: ${personal.get('ideal_wage', 'N/A')}/hr. "
        f"Tech stack: {personal.get('tech_stack', technical.get('strengths', 'N/A'))}. "
        f"Strengths: {technical.get('strengths', 'N/A')}. "
        f"Weaknesses: {technical.get('weaknesses', 'N/A')}."
    )


if __name__ == "__main__":
    test_email = load_test_email()
    my_settings = load_user_settings()

    lead_analysis = analyze_lead(test_email, my_settings)

    if lead_analysis:
        print(f"Scam Risk: {lead_analysis.scam_likelihood}%")
        print(f"Budget Score: {lead_analysis.budget_fit}/10")
        print(f"Summary: {lead_analysis.summary}")

        client_reply = write_client_reply(my_settings)
        if client_reply:
            print(f"Reply Type: {client_reply.suggested_reply_type}")
            print(f"Reply Subject: {client_reply.subject}")

            if isinstance(client_reply, LeadAnalysisAccepted):
                print(f"Reply Body: {client_reply.order_confirmation_template}")
            elif isinstance(client_reply, LeadAnalysisRejected):
                print(f"Reply Body: {client_reply.rejection_email_template}")
            elif isinstance(client_reply, LeadAnalysisClarification):
                print(f"Reply Body: {client_reply.clarification_email_template}")

    # print(test_email)
    # print(my_settings)
