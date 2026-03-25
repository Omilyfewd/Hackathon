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
        st.session_state.techStack = ""



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
        "tech": st.session_state.techStack
    }

def save_to_json(filename="profile.json"):
    data = getData()  # get your session data
    
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)