import json
import time
import re
import sys
import os
import streamlit as st
from app_data import getData, init_profile, modifyData
from description_formating import consolidate

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
if 'index' not in st.session_state:
    index = 0

if 'mapIndexToTextArea' not in st.session_state:
    st.session_state.mapIndexToTextArea = {}


def makeNewExpanders():
    final_array = consolidate()
    for row in final_array:
        if row[0] == "Reject":
            createNewExpander(st.session_state.low, row[3], row[1], row[2])
        elif row[0] == "Clarify":
            createNewExpander(st.session_state.medium, row[3], row[1], row[2])
        elif row[0] == "Accept":
            createNewExpander(st.session_state.high, row[3], row[1], row[2])


#Expander Logic
def createNewExpander(origin, name, description, response):
    origin.append({
        "name": name,
        "description": description,
        "id": st.session_state.index
        })
    st.session_state.mapIndexToTextArea[st.session_state.index] = response
    st.session_state.index += 1

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
        makeNewExpanders()
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

    if(len(st.session_state.low) == 0):
        st.write("No Low Match or Scam Likely Emails...")

    for i in range(len(st.session_state.low)):
        data = st.session_state.low[i]

        with st.expander(data["name"]):
            st.write(data["description"])
            key_name = f"lowReply_{i}"
            if key_name not in st.session_state:
                st.session_state[key_name] = st.session_state.mapIndexToTextArea.get(data["id"], "")

            reply = st.text_area(
                "Email Response",
                value=st.session_state[key_name],
                height=200,
                key=key_name
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
                elif action == "Send":
                    # 1. Setup the relative path
                    # This gets the folder containing your current script (frontend)
                    current_dir = os.path.dirname(os.path.abspath(__file__))

                    # This moves up to 'Hackathon' and then into 'logs_test_output'
                    target_dir = os.path.join(current_dir, "..", "logs_test_outputs")

                    # 2. Ensure the folder exists
                    os.makedirs(target_dir, exist_ok=True)

                    # 3. Create the file path (using .json for data)
                    file_path = os.path.join(target_dir, "example_email.json")

                    # 4. Prepare the data
                    output_data = {
                        "email_id": data.get("id"),
                        "recipient": data.get("name"),
                        "subject": "Proposal Denied",
                        "final_reply": reply,  # This is the value from your st.text_area
                    }

                    # 5. Save the file
                    with open(file_path, "w") as f:
                        json.dump(output_data, f, indent=4)

                    st.success(f"Log saved to: {os.path.normpath(file_path)}")
                st.rerun()

with medium:
    st.header("Clarification Needed")

    if(len(st.session_state.medium) == 0):
        st.write("No Emails Needing Clarification...")

    for i in range(len(st.session_state.medium)):
        data = st.session_state.medium[i]

        with st.expander(data["name"]):
            st.write(data["description"])
            key_name = f"mediumReply_{i}"
            if key_name not in st.session_state:
                st.session_state[key_name] = st.session_state.mapIndexToTextArea.get(data["id"], "")

            reply = st.text_area(
                "Email Response",
                value=st.session_state[key_name],
                height=200,
                key=key_name
            )

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
                elif action == "Send":
                    # 1. Setup the relative path
                    # This gets the folder containing your current script (frontend)
                    current_dir = os.path.dirname(os.path.abspath(__file__))

                    # This moves up to 'Hackathon' and then into 'logs_test_output'
                    target_dir = os.path.join(current_dir, "..", "logs_test_outputs")

                    # 2. Ensure the folder exists
                    os.makedirs(target_dir, exist_ok=True)

                    # 3. Create the file path (using .json for data)
                    file_path = os.path.join(target_dir, "example_email.json")

                    # 4. Prepare the data
                    output_data = {
                        "email_id": data.get("id"),
                        "recipient": data.get("name"),
                        "subject": "Follow Up for Clarification",
                        "final_reply": reply,  # This is the value from your st.text_area
                    }

                    # 5. Save the file
                    with open(file_path, "w") as f:
                        json.dump(output_data, f, indent=4)

                    st.success(f"Log saved to: {os.path.normpath(file_path)}")

                st.rerun()

with high:
    st.header("High Match")

    if(len(st.session_state.high) == 0):
        st.write("No High Match Emails...")

    for i in range(len(st.session_state.high)):
        data = st.session_state.high[i]

        with st.expander(data["name"]):
            st.write(data["description"])
            key_name = f"highReply_{i}"
            if key_name not in st.session_state:
                st.session_state[key_name] = st.session_state.mapIndexToTextArea.get(data["id"], "")

            reply = st.text_area(
                "Email Response",
                value=st.session_state.mapIndexToTextArea.get(data["id"], ""),
                height=200,
                key=f"highReply_{i}"
            )

            action = st.selectbox(
                "Action",
                ["Send", "Move to Low Match/Scam"],
                key=f"highAction_{i}"
            )

            if st.button("Confirm",  key=f"highButton_{i}"):
                item = st.session_state.high.pop(i)

                if action == "Move to Low Match/Scam":
                    st.session_state.low.append(item)
                elif action == "Send":
                    # 1. Setup the relative path
                    # This gets the folder containing your current script (frontend)
                    current_dir = os.path.dirname(os.path.abspath(__file__))

                    # This moves up to 'Hackathon' and then into 'logs_test_output'
                    target_dir = os.path.join(current_dir, "..", "logs_test_outputs")

                    # 2. Ensure the folder exists
                    os.makedirs(target_dir, exist_ok=True)

                    # 3. Create the file path (using .json for data)
                    file_path = os.path.join(target_dir, "example_email.json")

                    # 4. Prepare the data
                    output_data = {
                        "email_id": data.get("id"),
                        "recipient": data.get("name"),
                        "subject": "Proposal Accepted",
                        "final_reply": reply,  # This is the value from your st.text_area
                    }

                    # 5. Save the file
                    with open(file_path, "w") as f:
                        json.dump(output_data, f, indent=4)

                    st.success(f"Log saved to: {os.path.normpath(file_path)}")
                st.rerun()
