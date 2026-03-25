import json
import types
from datetime import datetime
from pathlib import Path
from typing import Union, get_args, get_origin

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG_FILE = PROJECT_ROOT / "logs_test_outputs" / "llm_log.json"
DEFAULT_COMPLETE_RESPONSE_FILE = PROJECT_ROOT / "logs_test_outputs" / "complete_response.jsonl"
DEFAULT_EMAIL_DETAILS_FILE = PROJECT_ROOT / "logs_test_outputs" / "latest_email.json"


def _load_json_object(file_path: Path):
    if not file_path.exists():
        return None

    content = file_path.read_text(encoding="utf-8").strip()
    if not content:
        return None

    return json.loads(content)


def _load_email_details(file_path: Path = DEFAULT_EMAIL_DETAILS_FILE):
    latest_email = _load_json_object(file_path)
    if not latest_email:
        return None

    return {
        "sender": latest_email.get("sender"),
        "subject": latest_email.get("subject"),
        "date": latest_email.get("date"),
        "body": latest_email.get("body"),
    }


def _get_response_model_map(response_model):
    if response_model is None:
        try:
            from llm_logic.lead_analyzer import LeadAnalysis
        except ModuleNotFoundError:
            from lead_analyzer import LeadAnalysis

        response_model = LeadAnalysis

    if hasattr(response_model, "model_fields"):
        return {response_model.__name__: response_model}

    origin = get_origin(response_model)

    if origin in (types.UnionType, Union):
        union_args = get_args(response_model)
    else:
        union_args = ()

    return {
        model.__name__: model
        for model in union_args
        if hasattr(model, "model_fields")
    }


def _build_response_entries(entry, response_model=None):
    response_model_map = _get_response_model_map(response_model)
    email_details = _load_email_details()

    if not entry:
        return []

    raw_response = entry.get("raw_response", {})
    parsed_response = raw_response.get("parsed_response")
    response_type = raw_response.get("response_type")

    if parsed_response is not None:
        model_class = response_model_map.get(response_type)

        if model_class is None and len(response_model_map) == 1:
            model_class = next(iter(response_model_map.values()))

        if model_class is None:
            normalized_arguments = parsed_response
        else:
            field_order = list(model_class.model_fields.keys())
            normalized_arguments = {
                field_name: parsed_response.get(field_name)
                for field_name in field_order
            }

        return [
            {
                "timestamp": entry.get("timestamp"),
                "name": response_type,
                "arguments": normalized_arguments,
                "email_details": email_details,
            }
        ]

    choices = raw_response.get("choices", [])
    response_entries = []

    for choice in choices:
        tool_calls = choice.get("message", {}).get("tool_calls", [])

        for tool_call in tool_calls:
            function_name = tool_call.get("function", {}).get("name")
            arguments_raw = tool_call.get("function", {}).get("arguments")
            if not arguments_raw:
                continue

            parsed_arguments = json.loads(arguments_raw)
            model_class = response_model_map.get(function_name)

            if model_class is None and len(response_model_map) == 1:
                model_class = next(iter(response_model_map.values()))

            if model_class is None:
                normalized_arguments = parsed_arguments
            else:
                field_order = list(model_class.model_fields.keys())
                normalized_arguments = {
                    field_name: parsed_arguments.get(field_name)
                    for field_name in field_order
                }

            response_entries.append(
                {
                    "timestamp": entry.get("timestamp"),
                    "name": function_name,
                    "arguments": normalized_arguments,
                    "email_details": email_details,
                }
            )

    return response_entries


def _append_jsonl_entries(file_path: Path, entries):
    if not entries:
        return

    file_path.parent.mkdir(parents=True, exist_ok=True)
    with file_path.open("a", encoding="utf-8") as output_handle:
        for entry in entries:
            output_handle.write(json.dumps(entry) + "\n")


def load_logged_response_entries(source_file=None, response_model=None):
    log_file = Path(source_file) if source_file else DEFAULT_LOG_FILE
    entry = _load_json_object(log_file)
    return _build_response_entries(entry, response_model=response_model)


def load_latest_logged_response(source_file=None, response_model=None):
    response_entries = load_logged_response_entries(source_file=source_file, response_model=response_model)
    if not response_entries:
        return None
    return response_entries[-1]


def _write_raw_log(response, filename=None):
    if hasattr(response, "_raw_response"):
        raw_data = response._raw_response.model_dump()
    elif hasattr(response, "model_dump"):
        raw_data = {
            "parsed_response": response.model_dump(),
            "response_type": type(response).__name__,
        }
    else:
        raw_data = {
            "parsed_response": str(response),
            "response_type": type(response).__name__,
        }

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "raw_response": raw_data
    }

    log_file = Path(filename) if filename else DEFAULT_LOG_FILE
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with log_file.open("w", encoding="utf-8") as f:
        json.dump(log_entry, f, indent=2)

    return log_entry, log_file


def log_raw_response(response, filename=None, response_model=None):
    _, log_file = _write_raw_log(response, filename=filename)

    print(f"--- Raw response saved to {log_file} ---")


def log_complete_response(
    response,
    filename=None,
    response_model=None,
    analysis_source_file=None,
    analysis_response_model=None,
    complete_response_file=None,
):
    latest_analysis_entry = load_latest_logged_response(
        source_file=analysis_source_file,
        response_model=analysis_response_model,
    )
    log_entry, log_file = _write_raw_log(response, filename=filename)
    response_entries = _build_response_entries(log_entry, response_model=response_model)
    output_file = Path(complete_response_file) if complete_response_file else DEFAULT_COMPLETE_RESPONSE_FILE

    if not response_entries:
        print(f"--- Raw response saved to {log_file} ---")
        return

    complete_entries = []
    for response_entry in response_entries:
        complete_entry = dict(response_entry)
        complete_entry["lead_analysis"] = latest_analysis_entry
        complete_entries.append(complete_entry)

    _append_jsonl_entries(output_file, complete_entries)

    print(f"--- Raw response saved to {log_file} ---")
    print(f"--- Complete response saved to {output_file} ---")
