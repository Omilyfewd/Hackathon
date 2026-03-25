import json
import time
import re
import sys
import os
import streamlit as st
from app_data import getData, init_profile, modifyData
from description_formating import getDescription

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from email_integration.email_to_json import save_email_as_json
try:
    from email_integration.email_to_json import save_email_as_json
except ModuleNotFoundError:
    from email_to_json import save_email_as_json

#Declare Arrays of Expanders
if "low" not in st.session_state:
    st.session_state.low = []
if "medium" not in st.session_state:
    st.session_state.medium = []
if "high" not in st.session_state:
    st.session_state.high = []

#Functions

#Expander Logic
def createNewExpander(origin, name):
    description = getDescription()
    origin.append({
        "name": name,
        "description": description
        })

def is_valid_email(email):
    # A basic regex pattern for email validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

#Top
col1, col2 = st.columns([5, 1])
sendButton = st.empty()

with col1:
    st.title("Dashboard")

with col2:
    st.write("")
    st.write("")
    if st.button("Pull Emails"):
        save_email_as_json()
        sendButton.success("Done!")
        sendButton.empty()



init_profile()
#Menu
profile, low, medium, high = st.tabs(["Profile", "Low Match/Scam", "Clarification Needed", "High Match"])

with profile:
    st.header("Profile")
    st.subheader("Please input your information")
    st.write("Input clear to delete current information")

    data = getData()
    with st.expander("Current Information"):
        st.write(f"**Email:** {data['email']}")
        st.write(f"**Website:** {data['website']}")
        st.write(f"**Ideal Working Hours:** {data['start_time']} to {data['end_time']}")
        st.write(f"**Ideal Wage:** {data['wage']}")
        st.write(f"**Tech Stack:** {data['tech']}")


    email = st.text_input(
        "Please input your email",
        value=st.session_state.email
    )

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

    tech = st.text_input(
        "Please list your tech stack",
        value=st.session_state.techStack
    )

    if st.button("Confirm", key="profileButton"):
        confirmButton = st.empty()
        if is_valid_email(email):
            modifyData(email, website, idealStartTime, idealEndTime, idealWage, tech)
            confirmButton.success("Saved!")
            time.sleep(2) # Wait 3 Seconds
            st.rerun()
        else:
            confirmButton.error("Please enter a valid email")


with low:
    st.header("Low Match/Scam")

    #Generate Test Expanders
    if st.button("low"):
        createNewExpander(st.session_state.low, "Void Paper")

    if(len(st.session_state.low) == 0):
        st.write("No Low Match or Scam Likely Emails...")

    for i in range(len(st.session_state.low)):
        data = st.session_state.low[i]

        with st.expander(data["name"]):
            st.write(data["description"])

            text = st.text_area(
                "Email Response",
                value="This is the default text",
                height=200
            )

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
        createNewExpander(st.session_state.medium, "Someone Shady")

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
        createNewExpander(st.session_state.high, "Big Yahu")

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
