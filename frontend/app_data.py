import os
import streamlit as st
import json


def _settings_path(filename="user_settings.json"):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def _load_from_json():
    path = _settings_path()
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    up = data.get("user_personal", {})
    st.session_state.email = up.get("email", st.session_state.get("email", ""))
    st.session_state.website = up.get("website", st.session_state.get("website", ""))
    st.session_state.idealStartTime = int(up.get("ideal_start", st.session_state.get("idealStartTime", 9)))
    st.session_state.idealEndTime = int(up.get("ideal_end", st.session_state.get("idealEndTime", 17)))
    st.session_state.idealWage = float(up.get("ideal_wage", st.session_state.get("idealWage", 15.0)))
    st.session_state.techStack = up.get("tech_stack", st.session_state.get("techStack", ""))
    st.session_state.userName = up.get("name", st.session_state.get("userName", ""))


def init_profile():
    if "profile_initialized" not in st.session_state:
        _load_from_json()
        st.session_state.profile_initialized = True

    if "idealWage" not in st.session_state or not isinstance(st.session_state.idealWage, (int, float)):
        st.session_state.idealWage = 15.0
    if "email" not in st.session_state:
        st.session_state.email = ""
        st.session_state.website = ""
        st.session_state.idealStartTime = 9
        st.session_state.idealEndTime = 17
        st.session_state.techStack = ""
    if "userName" not in st.session_state:
        st.session_state.userName = ""


def modifyData(email, website, startTime, endTime, wage, tech):
    st.session_state.idealStartTime = startTime
    st.session_state.idealEndTime = endTime

    if email == "clear":
        st.session_state.email = ""
    elif email != "":
        st.session_state.email = email

    if website == "clear":
        st.session_state.website = ""
    elif website != "":
        st.session_state.website = website

    if wage == "clear":
        st.session_state.idealWage = 0
    elif wage != "":
        st.session_state.idealWage = float(wage)

    if tech == "clear":
        st.session_state.techStack = ""
    elif tech != "":
        st.session_state.techStack = tech


def getData():
    return {
        "email": st.session_state.email,
        "website": st.session_state.website,
        "start_time": st.session_state.idealStartTime,
        "end_time": st.session_state.idealEndTime,
        "wage": st.session_state.idealWage,
        "tech": st.session_state.techStack,
    }


def save_to_json(filename="user_settings.json"):
    """Persist profile fields to JSON; keys align with `user_personal` in user_settings.json."""
    path = _settings_path(filename)
    payload = {
        "user_personal": {
            "name": st.session_state.get("userName", ""),
            "email": st.session_state.email,
            "website": st.session_state.website,
            "ideal_start": st.session_state.idealStartTime,
            "ideal_end": st.session_state.idealEndTime,
            "ideal_wage": st.session_state.idealWage,
            "tech_stack": st.session_state.techStack,
        }
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=4)
