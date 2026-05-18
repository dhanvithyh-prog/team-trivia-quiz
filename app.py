import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Team Trivia Quiz", layout="wide")

# 1. Setup Questions + The Correct Answer
# Format: "Question": [ [Options], "Correct Option" ]
quiz_data = {
    "Q1: What year was the company founded?": [["2010", "2015", "2018", "2020"], "2015"],
    "Q2: Which planet is known as the Red Planet?": [["Mars", "Venus", "Jupiter", "Saturn"], "Mars"],
    "Q3: Who was the first person to walk on the moon?": [["Buzz Aldrin", "Neil Armstrong", "Yuri Gagarin"], "Neil Armstrong"]
}

if 'responses' not in st.session_state:
    st.session_state.responses = []

# 2. Sidebar: Identity & Navigation
st.sidebar.title("👤 Player Info")
user_name = st.sidebar.text_input("Enter your name:", key="user_name")

st.sidebar.divider()
current_q = st.sidebar.radio("Select Question:", list(quiz_data.keys()))

# 3. Main Quiz Area
st.title("🏆 Team Trivia Challenge")

if not user_name:
    st.warning("Please enter your name in the sidebar to join the game!")
else:
    options, correct_answer = quiz_data[current_q]
    
    with st.form(key=f"form_{current_q}", clear_on_submit=True):
        st.subheader(current_q)
        choice = st.radio("Your Answer:", options)
        submit = st.form_submit_button("Submit Answer")

    if submit:
        # Check if right or wrong
        is_correct = (choice == correct_answer)
        
        # Save the result
        st.session_state.responses.append({
            "Who": user_name,
            "Question": current_q,
            "Answer": choice,
            "Is Correct": is_correct,
            "Points": 1 if is_correct else 0
        })
        
        if is_correct:
            st.success("🎯 Correct!")
            st.balloons()
        else:
            st.error("❌ Not quite!")

# 4. LEADERBOARD (The "End Game")
st.sidebar.divider()
if st.sidebar.button("📊 SHOW LEADERBOARD"):
    st.header("👑 Current Leaderboard")
    
    if st.session_state.responses:
        df = pd.DataFrame(st.session_state.responses)
        
        # Group by Name and sum the points
        leaderboard = df.groupby("Who")["Points"].sum().sort_values(ascending=False).reset_index()
        
        # Display as a nice table
        st.table(leaderboard)
        
        # Show a bar chart of scores
        st.bar_chart(leaderboard.set_index("Who"))
# --- MOVE THE WINNER ANNOUNCEMENT HERE ---
        if not leaderboard.empty:
            winner = leaderboard.iloc[0]['Who']
            st.markdown(f"## 🏆 The Champion is **{winner}**! 🏆")
    else:
        st.write("No scores recorded yet!")

