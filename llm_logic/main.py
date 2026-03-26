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
UNREAD_EMAILS_FILE = PROJECT_ROOT / "logs_test_outputs" / "unread_emails.jsonl"
USER_SETTINGS_FILE = PROJECT_ROOT / "frontend" / "user_settings.json"


def load_test_emails():
    if not UNREAD_EMAILS_FILE.exists():
        return []

    unread_emails = []
    with UNREAD_EMAILS_FILE.open("r", encoding="utf-8") as unread_emails_file:
        for line in unread_emails_file:
            stripped_line = line.strip()
            if stripped_line:
                unread_emails.append(json.loads(stripped_line))

    return unread_emails


def build_email_content(email_entry) -> str:
    subject = email_entry["subject"]
    body = email_entry["body"]
    return f"Subject: {subject}\nBody: {body}"


def load_user_settings() -> str:
    settings = json.loads(USER_SETTINGS_FILE.read_text(encoding="utf-8"))
    personal = settings.get("user_personal", {})
    technical = settings.get("user_technical", {})

    return (
        f"Name: {personal.get('name', 'N/A')}. "
        f"Email: {personal.get('email', 'N/A')}. "
        f"Website: {personal.get('website', 'N/A')}. "
        f"Current working hours: {personal.get('ideal_start', 'N/A')} to {personal.get('ideal_end', 'N/A')}. "
        f"Ideal wage: ${personal.get('ideal_wage', 'N/A')}/hr. "
        f"Tech stack: {personal.get('tech_stack', technical.get('strengths', 'N/A'))}. "
        f"Strengths: {technical.get('strengths', 'N/A')}. "
        f"Weaknesses: {technical.get('weaknesses', 'N/A')}."
    )


if __name__ == "__main__":
    unread_emails = load_test_emails()
    my_settings = load_user_settings()

    if not unread_emails:
        print(f"No unread emails found in {UNREAD_EMAILS_FILE}")

    for index, unread_email in enumerate(unread_emails, start=1):
        test_email = build_email_content(unread_email)
        lead_analysis = analyze_lead(test_email, my_settings, email_details=unread_email)

        if not lead_analysis:
            continue

        print(f"Email {index}:")
        print(f"Scam Risk: {lead_analysis.scam_likelihood}%")
        print(f"Budget Score: {lead_analysis.budget_fit}/10")
        print(f"Summary: {lead_analysis.summary}")

        lead_analysis_entry = {
            "timestamp": None,
            "name": type(lead_analysis).__name__,
            "arguments": lead_analysis.model_dump(),
            "email_details": unread_email,
        }

        client_reply = write_client_reply(
            my_settings,
            background_context=json.dumps(lead_analysis_entry, indent=2),
            suggested_reply_type=lead_analysis.suggested_reply_type,
            lead_analysis_entry=lead_analysis_entry,
            email_details=unread_email,
        )
        if client_reply:
            print(f"Reply Type: {client_reply.suggested_reply_type}")
            print(f"Reply Subject: {client_reply.subject}")

            if isinstance(client_reply, LeadAnalysisAccepted):
                print(f"Reply Body: {client_reply.order_confirmation_template}")
            elif isinstance(client_reply, LeadAnalysisRejected):
                print(f"Reply Body: {client_reply.rejection_email_template}")
            elif isinstance(client_reply, LeadAnalysisClarification):
                print(f"Reply Body: {client_reply.clarification_email_template}")
