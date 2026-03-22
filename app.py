import streamlit as st
import json

#Functions
def createNewExpander(origin, name, description):
    origin.append({
        "name": name,
        "description": description
        })

st.title("Goated Website")

#Menu
tab1, tab2, tab3, tab4 = st.tabs(["Profile", "Low Match/Scam", "Medium Match/Clarification Needed", "High Match"])

with tab1:
    st.header("Profile")

    st.subheader("Please input your information")
    idealWorkingHours = st.text_input("What are your ideal working hours?")
    deadlines = st.text_input("What are your current deadlines?")
    idealWage = st.text_input("What is your prefered dollars earned per hour?")
    #add more questions
with tab2:
    st.header("Low Match/Scam")

    if "low" not in st.session_state:
        st.session_state.low = []

    if st.button("low"):
        for x in range(5):
            createNewExpander(st.session_state.low, f"Void Paper_{x}", "This guy sucks")

    for i, data in enumerate(st.session_state.low):
        with st.expander(data["name"]):
            st.write(data["description"])

            action = st.selectbox(
                "Action",
                ["Profile", "Move to Medium Match", "Move to High Match"],
                key=f"lowAction_{i}"
            )

            if st.button("Confirm",  key=f"lowButton_{i}"):
                st.session_state.low.pop(i)
                st.rerun()

with tab3:
    st.header("Medium Match/Clarification Needed")

    if "medium" not in st.session_state:
        st.session_state.medium = []

    if st.button("medium"):
        for x in range(5):
            createNewExpander(st.session_state.medium, f"Someone Shady_{x}", "This guy sucks")

    for i, data in enumerate(st.session_state.medium):
        with st.expander(data["name"]):
            st.write(data["description"])

            action = st.selectbox(
                "Action",
                ["Profile", "Move to Low Match/Scam", "Move to High Match"],
                key=f"mediumAction_{i}"
            )

            if st.button("Confirm",  key=f"mediumButton_{i}"):
                st.session_state.medium.pop(i)
                st.rerun()

with tab4:
    st.header("High Match")

    if "high" not in st.session_state:
        st.session_state.high = []

    if st.button("high"):
        for x in range(5):
            createNewExpander(st.session_state.high, f"Big Yahu_{x}", "This guy sucks")

    for i, data in enumerate(st.session_state.high):
        with st.expander(data["name"]):
            st.write(data["description"])

            action = st.selectbox(
                "Action",
                ["Profile", "Move to Low Match/Scam", "Move to High Match"],
                key=f"highAction_{i}"
            )

            if st.button("Confirm",  key=f"highButton_{i}"):
                st.session_state.high.pop(i)
                st.rerun()
