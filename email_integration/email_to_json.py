import json
from pathlib import Path
from simplegmail import Gmail

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = PROJECT_ROOT / "keys_and_tokens" / "client_secret.json"
GMAIL_TOKEN_FILE = PROJECT_ROOT / "keys_and_tokens" / "gmail_token.json"
LATEST_EMAIL_FILE = PROJECT_ROOT / "logs_test_outputs" / "latest_email.json"


def save_email_as_json():
    try:
        # 1. Initialize Gmail (uses your client_secret.json and gmail_token.json)
        gmail = Gmail(
            client_secret_file=str(CLIENT_SECRET_FILE),
            creds_file=str(GMAIL_TOKEN_FILE),
        )

        # 2. Retrieve the most recent unread message
        messages = gmail.get_unread_inbox()

        if not messages:
            print("No unread messages found.")
            return

        latest_msg = messages[0]

        # 3. Structure the email data into a dictionary
        email_data = {
            "id": latest_msg.id,
            "sender": latest_msg.sender,
            "recipient": latest_msg.recipient,
            "subject": latest_msg.subject,
            "date": latest_msg.date,
            "snippet": latest_msg.snippet,
            "body": latest_msg.plain if latest_msg.plain else "HTML Content Only"
        }

        # 4. Save the dictionary as a JSON file
        LATEST_EMAIL_FILE.parent.mkdir(parents=True, exist_ok=True)
        with LATEST_EMAIL_FILE.open("w", encoding="utf-8") as f:
            json.dump(email_data, f, indent=4, ensure_ascii=False)

        print(f"Successfully saved the most recent email to {LATEST_EMAIL_FILE}")
        print(f"Subject: {email_data['subject']}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    save_email_as_json()
