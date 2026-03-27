import sys
import os

# Parent of `frontend/` so `email_integration` imports resolve when using `streamlit run app.py`
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import time
import re
import streamlit as st
from app_data import getData, init_profile, modifyData, save_to_json
from description_formating import getDescription

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


def pull_emails_from_gmail():
    """Import here so the app starts even if `simplegmail` is missing in this Python env."""
    from email_integration.email_to_json import save_email_as_json

    save_email_as_json()

#Top
col1, col2 = st.columns([5, 1])
sendButton = st.empty()

with col1:
    st.title("Dashboard")

with col2:
    st.write("")
    st.write("")
    if st.button("Pull Emails"):
        try:
            pull_emails_from_gmail()
            sendButton.success("Done!")
            sendButton.empty()
        except ModuleNotFoundError as e:
            if getattr(e, "name", None) == "simplegmail":
                st.error(
                    "Missing package `simplegmail`. Install it in the **same** environment you use "
                    "to run Streamlit, e.g. `python3 -m pip install simplegmail` or "
                    "`python3 -m pip install -r requirements.txt` from the project root."
                )
            else:
                raise



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
        value=(st.session_state.idealStartTime, st.session_state.idealEndTime),
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
            save_to_json("user_settings.json")
            confirmButton.success("Saved!")
            time.sleep(2) # Wait 3 Seconds
            st.rerun()
        else:
            confirmButton.error("Please enter a valid email")


with low:
    st.header("Low Match/Scam")

    if st.button("Send All Low Match Emails", key="send_all_low"):
        st.success("All low match emails sent successfully.")

    #Generate Test Expanders
    if st.button("low"):
        createNewExpander(st.session_state.low, "Void Paper")

    if(len(st.session_state.low) == 0):
        st.write("No Low Match or Scam Likely Emails...")

    for i in range(len(st.session_state.low)):
        data = st.session_state.low[i]

        with st.expander(data["name"]):
            st.markdown(data["description"])

            st.text_area(
                "Email Response",
                value="This is the default text",
                height=200,
                key=f"low_response_{i}"
            )

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Send Email", key=f"low_send_{i}"):
                    st.success("Email sent successfully.")
            with c2:
                if st.button("Move to High Match", key=f"low_to_high_{i}"):
                    item = st.session_state.low.pop(i)
                    st.session_state.high.append(item)
                    st.rerun()

with medium:
    st.header("Clarification Needed")

    if st.button("Send All Clarification Needed Emails", key="send_all_medium"):
        st.success("All clarification needed emails sent successfully.")

    #Generate Test Expanders
    if st.button("medium"):
        createNewExpander(st.session_state.medium, "Someone Shady")

    if(len(st.session_state.medium) == 0):
        st.write("No Medium Match or Clarification Needed Emails...")

    for i in range(len(st.session_state.medium)):
        data = st.session_state.medium[i]

        with st.expander(data["name"]):
            st.markdown(data["description"])

            st.text_area(
                "Email Response",
                value="This is the default text",
                height=200,
                key=f"medium_response_{i}"
            )

            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Send Email", key=f"medium_send_{i}"):
                    st.success("Email sent successfully.")
            with c2:
                if st.button("Move to Low Match", key=f"medium_to_low_{i}"):
                    item = st.session_state.medium.pop(i)
                    st.session_state.low.append(item)
                    st.rerun()
            with c3:
                if st.button("Move to High Match", key=f"medium_to_high_{i}"):
                    item = st.session_state.medium.pop(i)
                    st.session_state.high.append(item)
                    st.rerun()

with high:
    st.header("High Match")

    if st.button("Send All High Match Emails", key="send_all_high"):
        st.success("All high match emails sent successfully.")

    #Generate Test Expanders
    if st.button("high"):
        createNewExpander(st.session_state.high, "Big Yahu")

    if(len(st.session_state.high) == 0):
        st.write("No High Match Emails...")

    for i in range(len(st.session_state.high)):
        data = st.session_state.high[i]

        with st.expander(data["name"]):
            st.markdown(data["description"])

            st.text_area(
                "Email Response",
                value="This is the default text",
                height=200,
                key=f"high_response_{i}"
            )

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Send Email", key=f"high_send_{i}"):
                    st.success("Email sent successfully.")
            with c2:
                if st.button("Move to Low Match", key=f"high_to_low_{i}"):
                    item = st.session_state.high.pop(i)
                    st.session_state.low.append(item)
                    st.rerun()
