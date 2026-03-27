import os
import json

descriptionBase = """
**Scam Likelihood:** [BS]%

**Budget Fit:** [Money]/10

**Scope Clarity:** [Clear]/10

**Project Fit:** [Strong]/10

**Reasonable Timeline:** [YayNay]

**Summary:** [LLM]

---

### Original Email

**Subject:** [idkman]

[OG]
"""

latest_email = None
llm_logs = []

def get_latest_analysis(llm_logs):
    latest = llm_logs[-1]
    
    args_str = latest["raw_response"]["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"]
    
    return json.loads(args_str)

def openFiles():
    global latest_email
    # Open Files
    BASE_DIR = os.path.dirname(__file__)

    # Go up one level -> then into logs_test_outputs
    logs_path = os.path.join(BASE_DIR, "..", "logs_test_outputs")

    latest_email_path = os.path.join(logs_path, "latest_email.json")
    llm_logs_path = os.path.join(logs_path, "llm_logs.jsonl")


    # Load latest_email.json (normal JSON)
    with open(latest_email_path, "r") as f:
        latest_email = json.load(f)


    # Load llm_logs.jsonl (JSON Lines format)
    llm_logs.clear()
    with open(llm_logs_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:  # skip empty lines
                continue
            try:
                llm_logs.append(json.loads(line))
            except json.JSONDecodeError as e:
                print("Skipping bad line:", line)
                print(e)

def allExpanders():
    listOfExpanders = []



def getDescription():
    openFiles()
    # Formating
    template = descriptionBase

    # Email
    template = template.replace("[idkman]", latest_email["subject"])
    template = template.replace("[OG]", latest_email["body"])

    #LLM Information
    analysis = get_latest_analysis(llm_logs)

    template = template.replace("[BS]", str(analysis["scam_likelihood"]))
    template = template.replace("[Money]", str(analysis["budget_fit"]))
    template = template.replace("[Clear]", str(analysis["scope_clarity"]))
    template = template.replace("[Strong]", str(analysis.get("project_fit", "—")))
    template = template.replace("[YayNay]", "Yes" if analysis["timeline_reasonable"] else "No")
    template = template.replace("[LLM]", analysis["summary"])

    return template

def getVerdict():
    verdict = llm_logs["suggested_reply_type"]
    return verdict

def getReturnEmail():
    return "test"

def consolidate():
    expander = []
    expander.append(getVerdict())
    expander.append(getDescription())
    expander.append(getReturnEmail())
    return expander
