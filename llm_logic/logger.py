import json
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_FILE = PROJECT_ROOT / "logs_test_outputs" / "llm_logs.jsonl"


def log_raw_response(response, filename=None):
    # Access the raw completion from the Instructor object
    # Instructor stores the original litellm response in _raw_response
    raw_data = response._raw_response.model_dump()

    # Add a timestamp so you know when this happened
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "raw_response": raw_data
    }

    log_file = Path(filename) if filename else DEFAULT_LOG_FILE
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Append to the file (mode='a')
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"--- Raw response saved to {log_file} ---")
