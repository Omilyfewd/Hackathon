import json
import time

import streamlit as st

from app_data import getData, init_profile, modifyData

#Functions

#Expander Logic
def createNewExpander(origin, name, description):
    origin.append({
        "name": name,
        "description": description
        })


#Declare Arrays of Expanders
if "low" not in st.session_state:
    st.session_state.low = []
if "medium" not in st.session_state:
    st.session_state.medium = []
if "high" not in st.session_state:
    st.session_state.high = []

#Top
col1, col2 = st.columns([7, 1])
sendButton = st.empty()

with col1:
    st.title("Dashboard")

with col2:
    st.write("")
    st.write("")
    if st.button("Send All"):
        if len(st.session_state.low) != 0 or len(st.session_state.medium) != 0  or  len(st.session_state.high) != 0:
            for i in range(len(st.session_state.low)):
                st.session_state.low.pop()
            for i in range(len(st.session_state.medium)):
                st.session_state.medium.pop()
            for i in range(len(st.session_state.high)):
                st.session_state.high.pop()

            sendButton.success("Sending!")
            time.sleep(2)
            sendButton.empty()
        else:
            sendButton.error("No Emails to Send...")
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
        st.write(f"**Website:** {data['website']}")
        st.write(f"**Current Working Hours:** {data['start_time']} to {data['end_time']}")
        st.write(f"**Ideal Wage:** {data['wage']}")
        st.write(f"**Current Workload:** {data['workload']}")
        st.write(f"**Strengths:** {data['strengths']}")
        st.write(f"**Weaknesses:** {data['weaknesses']}")

    website = st.text_input(
        "Please give your website to provide to accepted clients",
        value=st.session_state.website
    )

    idealStartTime, idealEndTime = st.slider(
        "Ideal working hours:",
        value=(9, 17),
        min_value=0,
        max_value=24
    )

    idealWage = st.number_input(
        "Preferred wage (Dollars per Hour)",
        min_value=0.0,
        max_value=1000.0,
        value=st.session_state.idealWage,
        step=0.5
    )

    currentWorkLoad = st.text_input(
        "Current workload",
        value=st.session_state.currentWorkLoad
    )

    strengths = st.text_input(
        "Please list your strengths",
        value=st.session_state.strengths
    )

    weaknesses = st.text_input(
        "Please list your weaknesses(if any)",
        value=st.session_state.weaknesses
    )

    if st.button("Confirm", key="profileButton"):
        confirmButton = st.empty()
        modifyData(website, idealStartTime, idealEndTime, idealWage, currentWorkLoad, strengths, weaknesses)
        confirmButton.success("Saved!")
        time.sleep(2) # Wait 3 Seconds
        st.rerun()


with low:
    st.header("Low Match/Scam")

    #Generate Test Expanders
    if st.button("low"):
        for x in range(5):
            createNewExpander(st.session_state.low, f"Void Paper_{x}", "This guy sucks")

    if(len(st.session_state.low) == 0):
        st.write("No Low Match or Scam Likely Emails...")

    for i in range(len(st.session_state.low)):
        data = st.session_state.low[i]

        with st.expander(data["name"]):
            st.write(data["description"])

            action = st.selectbox(
                "Action",
                ["Send", "Move to High Match"],
                key=f"lowAction_{i}"
            )

            if st.button("Confirm", key=f"lowButton_{i}"):
                item = st.session_state.low.pop(i)

                if action == "Move to High Match":
                    st.session_state.high.append(item)

                st.rerun()

with medium:
    st.header("Clarification Needed")

    #Generate Test Expanders
    if st.button("medium"):
        for x in range(5):
            createNewExpander(st.session_state.medium, f"Someone Shady_{x}", "This guys ok")

    if(len(st.session_state.medium) == 0):
        st.write("No Medium Match or Clarification Needed Emails...")

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
                item = st.session_state.medium.pop(i)

                if action == "Move to Low Match/Scam":
                    st.session_state.low.append(item)
                elif action == "Move to High Match":
                    st.session_state.high.append(item)

                st.rerun()

with high:
    st.header("High Match")

    #Generate Test Expanders
    if st.button("high"):
        for x in range(5):
            createNewExpander(st.session_state.high, f"Big Yahu_{x}", "This guys great")

    if(len(st.session_state.high) == 0):
        st.write("No High Match Emails...")

    for i in range(len(st.session_state.high)):
        data = st.session_state.high[i]

        with st.expander(data["name"]):
            st.write(data["description"])

            action = st.selectbox(
                "Action",
                ["Send", "Move to Low Match/Scam"],
                key=f"highAction_{i}"
            )

            if st.button("Confirm",  key=f"highButton_{i}"):
                item = st.session_state.high.pop(i)

                if action == "Move to Low Match/Scam":
                    st.session_state.low.append(item)
                st.rerun()
