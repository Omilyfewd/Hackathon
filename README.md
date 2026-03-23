# Hackathon

Project layout:

- `frontend/` contains the Streamlit UI.
- `llm_logic/` contains lead analysis and LLM logging.
- `email_integration/` contains Gmail fetch/send/test scripts.
- `keys_and_tokens/` contains `.env`, `client_secret.json`, and `gmail_token.json`.
- `logs_test_outputs/` contains generated logs and saved email payloads.

Instructions:

Obtain a `client_secret.json` file from Google Cloud Console's APIs & Services.
Obtain an API key for an OpenAI-compatible model and store it in `keys_and_tokens/.env`.
