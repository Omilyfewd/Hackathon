import base64

from gmail_client import create_gmail_client, get_unread_messages


def save_raw_email(gmail=None):
    client = gmail or create_gmail_client()
    messages = get_unread_messages(client)

    if not messages:
        print("No unread messages found. Send yourself a test lead!")
        return

    latest_msg = messages[0]

    raw_b64 = latest_msg.raw_format["raw"]
    raw_eml = base64.urlsafe_b64decode(raw_b64)

    filename = "latest_lead.eml"
    with open(filename, "wb") as f:
        f.write(raw_eml)

    print(f"--- Successfully saved: {filename} ---")
    print(f"Subject: {latest_msg.subject}")
    print(f"From: {latest_msg.sender}")
    print(f"Snippet: {latest_msg.snippet}")


if __name__ == "__main__":
    save_raw_email()
