import json
from pathlib import Path
from simplegmail import Gmail
from simplegmail import label

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = PROJECT_ROOT / "keys_and_tokens" / "client_secret.json"
GMAIL_TOKEN_FILE = PROJECT_ROOT / "keys_and_tokens" / "gmail_token.json"
UNREAD_EMAILS_FILE = PROJECT_ROOT / "logs_test_outputs" / "unread_emails.jsonl"


def save_email_as_json():
    try:
        gmail = Gmail(
            client_secret_file=str(CLIENT_SECRET_FILE),
            creds_file=str(GMAIL_TOKEN_FILE),
        )

        messages = gmail.get_unread_inbox()

        if not messages:
            print("No unread messages found.")
            return

        unread_email_entries = []
        for message in messages:
            unread_email_entries.append(
                {
                    "id": message.id,
                    "sender": message.sender,
                    "recipient": message.recipient,
                    "subject": message.subject,
                    "date": message.date,
                    "snippet": message.snippet,
                    "body": message.plain if message.plain else "HTML Content Only",
                }
            )

        UNREAD_EMAILS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with UNREAD_EMAILS_FILE.open("w", encoding="utf-8") as f:
            for entry in unread_email_entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        for message in messages:
            message.modify_labels(to_add=[], to_remove=[label.UNREAD])

        print(f"Successfully saved {len(unread_email_entries)} unread emails to {UNREAD_EMAILS_FILE}")
        print(f"Marked {len(messages)} emails as read.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    save_email_as_json()
