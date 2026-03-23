from pathlib import Path
from simplegmail import Gmail

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = PROJECT_ROOT / "keys_and_tokens" / "client_secret.json"
GMAIL_TOKEN_FILE = PROJECT_ROOT / "keys_and_tokens" / "gmail_token.json"


def test_connection():
    try:
        gmail = Gmail(
            client_secret_file=str(CLIENT_SECRET_FILE),
            creds_file=str(GMAIL_TOKEN_FILE),
        )
        print("Successfully connected to Gmail!")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
