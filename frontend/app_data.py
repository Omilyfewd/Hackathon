import streamlit as st
import json


def init_profile():
    if "idealWage" not in st.session_state or not isinstance(st.session_state.idealWage, (int, float)):
        st.session_state.idealWage = 15.0
    if "email" not in st.session_state:
        st.session_state.email = ""
        st.session_state.website = ""
        st.session_state.idealStartTime = 9
        st.session_state.idealEndTime = 17
        st.session_state.currentWorkLoad = ""
        st.session_state.strengths = ""
        st.session_state.weaknesses = ""



def modifyData(email, website, startTime, endTime, wage, workload, strength, weakness):
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

    if workload == "clear":
        st.session_state.currentWorkLoad = ""
    elif workload != "":
        st.session_state.currentWorkLoad = workload

    if strength == "clear":
        st.session_state.strengths = ""
    elif strength != "":
        st.session_state.strengths = strength

    if weakness == "clear":
        st.session_state.weaknesses = ""
    elif weakness != "":
        st.session_state.weaknesses = weakness


def getData():
    return {
        "email": st.session_state.email,
        "website": st.session_state.website,
        "start_time": st.session_state.idealStartTime,
        "end_time": st.session_state.idealEndTime,
        "wage": st.session_state.idealWage,
        "workload": st.session_state.currentWorkLoad,
        "strengths": st.session_state.strengths,
        "weaknesses": st.session_state.weaknesses,
    }

def save_to_json(filename="profile.json"):
    data = getData()  # get your session data
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def load_from_json(filename="profile.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        st.session_state.email = data.get("email", "")
        st.session_state.website = data.get("website", "")
        st.session_state.idealStartTime = data.get("start_time", 9)
        st.session_state.idealEndTime = data.get("end_time", 17)
        st.session_state.idealWage = data.get("wage", 15.0)
        st.session_state.currentWorkLoad = data.get("workload", "")
        st.session_state.strengths = data.get("strengths", "")
        st.session_state.weaknesses = data.get("weaknesses", "")

    except FileNotFoundError:
        pass  # first run, no file yet