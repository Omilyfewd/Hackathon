import json
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_FILE = PROJECT_ROOT / "logs_test_outputs" / "llm_log.json"
DEFAULT_ARGUMENTS_LOG_FILE = PROJECT_ROOT / "logs_test_outputs" / "llm_arguments.jsonl"


def _load_json_object(file_path: Path):
    if not file_path.exists():
        return None

    content = file_path.read_text(encoding="utf-8").strip()
    if not content:
        return None

    return json.loads(content)


def extract_argument_responses(source_file=None, output_file=None):
    try:
        from llm_logic.lead_analyzer import LeadAnalysis
    except ModuleNotFoundError:
        from lead_analyzer import LeadAnalysis

    log_file = Path(source_file) if source_file else DEFAULT_LOG_FILE
    arguments_file = Path(output_file) if output_file else DEFAULT_ARGUMENTS_LOG_FILE

    arguments_file.parent.mkdir(parents=True, exist_ok=True)
    field_order = list(LeadAnalysis.model_fields.keys())
    entry = _load_json_object(log_file)

    if not entry:
        return

    choices = entry.get("raw_response", {}).get("choices", [])

    with arguments_file.open("a", encoding="utf-8") as output_handle:
        for choice in choices:
            tool_calls = choice.get("message", {}).get("tool_calls", [])

            for tool_call in tool_calls:
                arguments_raw = tool_call.get("function", {}).get("arguments")
                if not arguments_raw:
                    continue

                parsed_arguments = json.loads(arguments_raw)
                normalized_arguments = {
                    field_name: parsed_arguments.get(field_name)
                    for field_name in field_order
                }

                output_entry = {
                    "timestamp": entry.get("timestamp"),
                    "name": tool_call.get("function", {}).get("name"),
                    "arguments": normalized_arguments,
                }
                output_handle.write(json.dumps(output_entry) + "\n")


def log_raw_response(response, filename=None):
    raw_data = response._raw_response.model_dump()

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "raw_response": raw_data
    }

    log_file = Path(filename) if filename else DEFAULT_LOG_FILE
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with log_file.open("w", encoding="utf-8") as f:
        json.dump(log_entry, f, indent=2)

    extract_argument_responses(source_file=log_file)

    print(f"--- Raw response saved to {log_file} ---")
