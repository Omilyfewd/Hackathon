from bs4 import BeautifulSoup

from gmail_client import create_gmail_client, get_unread_messages


def clean_message_body(message):
    content = message.plain if message.plain else message.html or ""
    soup = BeautifulSoup(content, "html.parser")
    return soup.get_text(separator=" ", strip=True)


def message_to_lead(message):
    return {
        "id": message.id,
        "sender": message.sender,
        "subject": message.subject,
        "body": clean_message_body(message)[:2000],
    }


def get_clean_leads(gmail=None, mark_as_read=True):
    client = gmail or create_gmail_client()
    messages = get_unread_messages(client)

    leads = []
    for msg in messages:
        leads.append(message_to_lead(msg))
        if mark_as_read:
            msg.mark_as_read()

    return leads
