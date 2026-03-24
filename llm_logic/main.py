import json
from pathlib import Path

try:
    from llm_logic.lead_analyzer import analyze_lead
except ModuleNotFoundError:
    from lead_analyzer import analyze_lead

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
    return (
        f"Ideal wage: ${settings.get('ideal_wage', 'N/A')}/hr. "
        f"Current workload: {settings.get('current_workload', 'N/A')}. "
        f"Strengths: {settings.get('strengths', '')}. "
        f"Weaknesses: {settings.get('weaknesses', '')}."
    )


if __name__ == "__main__":
    test_email = load_test_email()
    my_settings = load_user_settings()

    result = analyze_lead(test_email, my_settings)

    if result:
        print(f"Scam Risk: {result.scam_likelihood}%")
        print(f"Budget Score: {result.budget_fit}/10")
        print(f"Red Flags: {', '.join(result.red_flags)}")
        print(f"Summary: {result.summary}")

    print(test_email)
    print(my_settings)
