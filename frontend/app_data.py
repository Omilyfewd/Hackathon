import streamlit as st


def init_profile():
    if "idealWorkHours" not in st.session_state:
        st.session_state.idealWorkHours = ""
        st.session_state.idealWage = ""
        st.session_state.currentWorkLoad = ""


def modifyData(hours, wage, workload):
    if hours == "clear":
        st.session_state.idealWorkHours = hours
    elif hours != "":
        st.session_state.idealWorkHours = hours

    if wage == "clear":
        st.session_state.idealWage = ""
    elif wage != "":
        st.session_state.idealWage = wage

    if workload == "clear":
        st.session_state.currentWorkLoad = ""
    elif workload != "":
        st.session_state.currentWorkLoad = workload


def getData():
    return {
        "hours": st.session_state.idealWorkHours,
        "wage": st.session_state.idealWage,
        "workload": st.session_state.currentWorkLoad,
    }
