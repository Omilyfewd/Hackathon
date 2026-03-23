from pathlib import Path
from simplegmail import Gmail

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLIENT_SECRET_FILE = PROJECT_ROOT / "keys_and_tokens" / "client_secret.json"
GMAIL_TOKEN_FILE = PROJECT_ROOT / "keys_and_tokens" / "gmail_token.json"

gmail = Gmail(
    client_secret_file=str(CLIENT_SECRET_FILE),
    creds_file=str(GMAIL_TOKEN_FILE),
)

def send_test_email():
    gmail.send_message(
        to="voidpaper1234@gmail.com",
        sender="bigyahufromohio@gmail.com",
        subject="YOU WON A FREE TRIP TO TEL-AVIV!!!",
        msg_html="<h1>Hi!</h1>When people step on these surfaces, pressure created. That pressure is converted into electrical energy. This method is considered an eco-friendly source of power. It is commonly used in crowded places like railway stations and shopping malls. Walking naturally helps produce energy without extra effort.The generated electricity is used for lights and electronic displays. This innovation helps reduce energy problems.Japan is generating electricity by using the energy produced when people walk. This technology works by installing special devices under floors or roads. When people step on these surfaces, pressure created. That pressure is converted into electrical energy. This method is considered an eco-friendly source of power. It is commonly used in crowded places like railway stations and shopping malls. Walking naturally helps produce energy without extra effort.The generated electricity is used for lights and electronic displays. This innovation helps reduce energy problems.</p>",
        msg_plain="Japan is generating electricity by using the energy produced when people walk. This technology works by installing special devices under floors or roads. When people step on these surfaces, pressure created. That pressure is converted into electrical energy. This method is considered an eco-friendly source of power. It is commonly used in crowded places like railway stations and shopping malls. Walking naturally helps produce energy without extra effort.The generated electricity is used for lights and electronic displays. This innovation helps reduce energy problems.Japan is generating electricity by using the energy produced when people walk. This technology works by installing special devices under floors or roads. When people step on these surfaces, pressure created. That pressure is converted into electrical energy. This method is considered an eco-friendly source of power. It is commonly used in crowded places like railway stations and shopping malls. Walking naturally helps produce energy without extra effort.The generated electricity is used for lights and electronic displays. This innovation helps reduce energy problems."
    )


if __name__ == "__main__":
    send_test_email()
