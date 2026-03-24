import streamlit as st


def init_profile():
    if "idealWage" not in st.session_state or not isinstance(st.session_state.idealWage, (int, float)):
        st.session_state.idealWage = 15.0
    if "website" not in st.session_state:
        st.session_state.website = ""
        st.session_state.idealStartTime = 9
        st.session_state.idealEndTime = 17
        st.session_state.currentWorkLoad = ""
        st.session_state.strengths = ""
        st.session_state.weaknesses = ""



def modifyData(website, startTime, endTime, wage, workload, strength, weakness):
    st.session_state.idealStartTime = startTime
    st.session_state.idealEndTime = endTime


    if website == "clear":
        st.session_state.website = ""
    elif website != "":
        st.session_state.website = wage

    if wage == "clear":
        st.session_state.idealWage = ""
    elif wage != "":
        st.session_state.idealWage = wage

    if workload == "clear":
        st.session_state.currentWorkLoad = ""
    elif workload != "":
        st.session_state.currentWorkLoad = workload

    if workload == "clear":
        st.session_state.strengths = ""
    elif workload != "":
        st.session_state.strengths = strength

    if workload == "clear":
        st.session_state.weaknesses = ""
    elif workload != "":
        st.session_state.weaknesses = weakness


def getData():
    return {
        "website": st.session_state.website,
        "start_time": st.session_state.idealStartTime,
        "end_time": st.session_state.idealEndTime,
        "wage": st.session_state.idealWage,
        "workload": st.session_state.currentWorkLoad,
        "strengths": st.session_state.strengths,
        "weaknesses": st.session_state.weaknesses,
    }
