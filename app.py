import streamlit as st
import time
import json

from appData import init_profile, modifyData, getData

#Functions

#Expander Logic
def createNewExpander(origin, name, description):
    origin.append({
        "name": name,
        "description": description
        })

#Top
col1, col2 = st.columns([7, 1])
sendButton = st.empty()

with col1:
    st.title("Dashboard")

with col2:
    st.write("")
    st.write("")
    if st.button("Send All"):
        for i in range(len(st.session_state.low)):
            st.session_state.low.pop()
        for i in range(len(st.session_state.medium)):
            st.session_state.medium.pop()
        for i in range(len(st.session_state.high)):
            st.session_state.high.pop()

        sendButton.success("Sent!")
        time.sleep(2)
        sendButton.empty()

init_profile()
#Menu
profile, low, medium, high = st.tabs(["Profile", "Low Match/Scam", "Medium Match/Clarification Needed", "High Match"])

with profile:
    st.header("Profile")
    st.subheader("Please input your information")
    st.write("Input clear to delete current information")

    data = getData()
    with st.expander("Current Information"):
        st.write(f"**Current Working Hours:** {data['hours']}")
        st.write(f"**Ideal Wage:** {data['wage']}")
        st.write(f"**Current Workload:** {data['workload']}")
        

    idealWorkingHours = st.text_input(
        "What are your ideal working hours?",
        value=st.session_state.idealWorkHours
    )

    idealWage = st.text_input(
        "Preferred wage",
        value=st.session_state.idealWage
    )

    deadlines = st.text_input(
        "Current workload",
        value=st.session_state.currentWorkLoad
    )
    #add more questions

    if st.button("Confirm", key="profileButton"):
        confirmButton = st.empty()
        modifyData(idealWorkingHours, idealWage, deadlines)
        confirmButton.success("Saved!")
        time.sleep(2) # Wait 3 Seconds
        st.rerun()


with low:
    st.header("Low Match/Scam")

    if "low" not in st.session_state:
        st.session_state.low = []

    #Generate Test Expanders
    if st.button("low"):
        for x in range(5):
            createNewExpander(st.session_state.low, f"Void Paper_{x}", "This guy sucks")

    for i in range(len(st.session_state.low)):
        data = st.session_state.low[i]

        with st.expander(data["name"]):
            st.write(data["description"])

            action = st.selectbox(
                "Action",
                ["Send", "Move to Medium Match", "Move to High Match"],
                key=f"lowAction_{i}"
            )

            if st.button("Confirm", key=f"lowButton_{i}"):
                st.session_state.low.pop(i)
                st.rerun()

with medium:
    st.header("Medium Match/Clarification Needed")

    if "medium" not in st.session_state:
        st.session_state.medium = []

    #Generate Test Expanders
    if st.button("medium"):
        for x in range(5):
            createNewExpander(st.session_state.medium, f"Someone Shady_{x}", "This guys ok")

    for i in range(len(st.session_state.medium)):
        data = st.session_state.medium[i]

        with st.expander(data["name"]):
            st.write(data["description"])

            action = st.selectbox(
                "Action",
                ["Send", "Move to Low Match/Scam", "Move to High Match"],
                key=f"mediumAction_{i}"
            )

            if st.button("Confirm",  key=f"mediumButton_{i}"):
                st.session_state.medium.pop(i)
                st.rerun()

with high:
    st.header("High Match")

    if "high" not in st.session_state:
        st.session_state.high = []

    #Generate Test Expanders
    if st.button("high"):
        for x in range(5):
            createNewExpander(st.session_state.high, f"Big Yahu_{x}", "This guys great")

    for i in range(len(st.session_state.high)):
        data = st.session_state.high[i]

        with st.expander(data["name"]):
            st.write(data["description"])

            action = st.selectbox(
                "Action",
                ["Send", "Move to Low Match/Scam", "Move to High Match"],
                key=f"highAction_{i}"
            )

            if st.button("Confirm",  key=f"highButton_{i}"):
                st.session_state.high.pop(i)
                st.rerun()
