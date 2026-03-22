import streamlit as st
import json

keyNumber = 0;
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

    if st.button("click me"):
        createNewExpander(st.session_state.low, "Void Paper", "This guy sucks")

    for i, data in enumerate(st.session_state.low):
        with st.expander(data["name"]):
            st.write(data["description"])

            action = st.selectbox(
                "Action",
                ["Profile", "Low Match/Scam", "Medium Match", "High Match"],
                key=f"action_{keyNumber}"
            )

            if st.button("Confirm",  key=f"action_{keyNumber}"):
                st.write("ok")

with tab3:
    st.header("Medium Match/Clarification Needed")

    if "medium" not in st.session_state:
        st.session_state.medium = []

with tab4:
    st.header("High Match")

    if "high" not in st.session_state:
        st.session_state.high = []
