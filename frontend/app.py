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
from email_integration.send_email import send_test_email
try:
    from email_integration.email_to_json import save_email_as_json
    from email_integration.send_email import send_test_email
except ModuleNotFoundError:
    from email_to_json import save_email_as_json
    from send_email import send_test_email

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
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    target_dir = os.path.join(current_dir, "..", "logs_test_outputs")
                    os.makedirs(target_dir, exist_ok=True)

                    # 2. Define the HTML file path
                    file_path = os.path.join(target_dir, "example_email.html")

                    # 3. Create the HTML content with some basic styling
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            body {{ font-family: sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 40px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
                            .header {{ border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }}
                            .label {{ font-weight: bold; color: #555; }}
                            .content-box {{ background: #f9f9f9; padding: 15px; border-radius: 4px; border-left: 4px solid #4CAF50; white-space: pre-wrap; }}
                            .meta {{ font-size: 0.9em; color: #888; margin-top: 20px; }}
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <h2>Email Response Log</h2>
                            <p><span class="label">Recipient:</span> {data.get('name', 'N/A')}</p>
                            <p><span class="label">Sender:</span> {data.get('sender_email', 'N/A')}</p>
                        </div>

                        <div>
                            <p class="label">Original Analysis Description:</p>
                            <p>{data.get('description', 'No description provided.')}</p>
                        </div>

                        <div>
                            <p class="label">Final Sent Reply:</p>
                            <div class="content-box">{reply}</div>
                        </div>
                    </body>
                    </html>
                    """

                    # 4. Write the file
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(html_content)

                    st.success(f"HTML Log created at: {os.path.normpath(file_path)}")

                    # send_test_email()

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
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    target_dir = os.path.join(current_dir, "..", "logs_test_outputs")
                    os.makedirs(target_dir, exist_ok=True)

                    # 2. Define the HTML file path
                    file_path = os.path.join(target_dir, "example_email.html")

                    # 3. Create the HTML content with some basic styling
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            body {{ font-family: sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 40px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
                            .header {{ border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }}
                            .label {{ font-weight: bold; color: #555; }}
                            .content-box {{ background: #f9f9f9; padding: 15px; border-radius: 4px; border-left: 4px solid #4CAF50; white-space: pre-wrap; }}
                            .meta {{ font-size: 0.9em; color: #888; margin-top: 20px; }}
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <h2>Email Response Log</h2>
                            <p><span class="label">Recipient:</span> {data.get('name', 'N/A')}</p>
                            <p><span class="label">Sender:</span> {data.get('sender_email', 'N/A')}</p>
                        </div>

                        <div>
                            <p class="label">Original Analysis Description:</p>
                            <p>{data.get('description', 'No description provided.')}</p>
                        </div>

                        <div>
                            <p class="label">Final Sent Reply:</p>
                            <div class="content-box">{reply}</div>
                        </div>
                    </body>
                    </html>
                    """

                    # 4. Write the file
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(html_content)

                    st.success(f"HTML Log created at: {os.path.normpath(file_path)}")

                    send_test_email()

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
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    target_dir = os.path.join(current_dir, "..", "logs_test_outputs")
                    os.makedirs(target_dir, exist_ok=True)

                    # 2. Define the HTML file path
                    file_path = os.path.join(target_dir, "example_email.html")

                    # 3. Create the HTML content with some basic styling
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <style>
                            body {{ font-family: sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 40px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }}
                            .header {{ border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }}
                            .label {{ font-weight: bold; color: #555; }}
                            .content-box {{ background: #f9f9f9; padding: 15px; border-radius: 4px; border-left: 4px solid #4CAF50; white-space: pre-wrap; }}
                            .meta {{ font-size: 0.9em; color: #888; margin-top: 20px; }}
                        </style>
                    </head>
                    <body>
                        <div class="header">
                            <h2>Email Response Log</h2>
                            <p><span class="label">Recipient:</span> {data.get('name', 'N/A')}</p>
                            <p><span class="label">Sender:</span> {data.get('sender_email', 'N/A')}</p>
                        </div>

                        <div>
                            <p class="label">Original Analysis Description:</p>
                            <p>{data.get('description', 'No description provided.')}</p>
                        </div>

                        <div>
                            <p class="label">Final Sent Reply:</p>
                            <div class="content-box">{reply}</div>
                        </div>
                    </body>
                    </html>
                    """

                    # 4. Write the file
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(html_content)

                    st.success(f"HTML Log created at: {os.path.normpath(file_path)}")

                    send_test_email()

                    st.success(f"Log saved to: {os.path.normpath(file_path)}")
                st.rerun()
