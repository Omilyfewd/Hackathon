import json
from datetime import datetime


def log_raw_response(response, filename="llm_logs.jsonl"):
    # Access the raw completion from the Instructor object
    # Instructor stores the original litellm response in _raw_response
    raw_data = response._raw_response.model_dump()

    # Add a timestamp so you know when this happened
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "raw_response": raw_data
    }

    # Append to the file (mode='a')
    with open(filename, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"--- Raw response saved to {filename} ---")