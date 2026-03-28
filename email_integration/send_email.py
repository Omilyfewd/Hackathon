from pathlib import Path
import re
from simplegmail import Gmail

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = PROJECT_ROOT / "keys_and_tokens" / "client_secret.json"
GMAIL_TOKEN_FILE = PROJECT_ROOT / "keys_and_tokens" / "gmail_token.json"

gmail = Gmail(
    client_secret_file=str(CLIENT_SECRET_FILE),
    creds_file=str(GMAIL_TOKEN_FILE),
)


def html_to_plain_text(html: str) -> str:
    text = re.sub(r"<style.*?</style>", "", html, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<script.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def send_test_email(html_content: str):
    plain_text = html_to_plain_text(html_content)

    gmail.send_message(
        to="voidpaper1234@gmail.com",
        sender="bigyahufromohio@gmail.com",
        subject="Service Request",
        msg_html=html_content,
        msg_plain=plain_text
    )

    print(plain_text)


if __name__ == "__main__":
    raise SystemExit("send_test_email() now requires an html_content argument.")
