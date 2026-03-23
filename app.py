import streamlit as st
import time
import json

#Functions

#Expander Logic
def createNewExpander(origin, name, description):
    origin.append({
        "name": name,
        "description": description
        })

#Button Logic
def timed_button(label, key, duration=3, success_text="Done!"):
    # Initialize state for this button
    if key not in st.session_state:
        st.session_state[key] = 0

    # Determine what text to show
    if time.time() - st.session_state[key] < duration:
        current_label = success_text
        disabled = True
    else:
        current_label = label
        disabled = False

    # Create button
    if st.button(current_label, key=key + "_btn", disabled=disabled):
        st.session_state[key] = time.time()
        return True  # button was clicked

    return False

#Top
col1, col2 = st.columns([7, 1])

with col1:
    st.title("Dashboard")

with col2:
    st.write("")
    st.write("")
    if st.button("Send All"):
        st.write("Sending...")



#Menu
profile, low, medium, high = st.tabs(["Profile", "Low Match/Scam", "Medium Match/Clarification Needed", "High Match"])

with profile:
    st.header("Profile")

    st.subheader("Please input your information")
    idealWorkingHours = st.text_input("What are your ideal working hours?")
    deadlines = st.text_input("What are your current deadlines?")
    idealWage = st.text_input("What is your prefered dollars earned per hour?")
    #add more questions
    
    if timed_button("Confirm", key="profileButton"):
        #implement Logic to change self
        st.write("placeholder")
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
