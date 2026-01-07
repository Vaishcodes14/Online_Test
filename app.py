import streamlit as st
import json
import random
import os

st.set_page_config(page_title="Adaptive English Test", layout="centered")

# ---------------- LOAD QUESTIONS ----------------
@st.cache_data
def load_questions():
    path = os.path.join(os.path.dirname(__file__), "data", "english.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

easy_qs = [q for q in questions if q["difficulty"] == "Easy"]
medium_qs = [q for q in questions if q["difficulty"] == "Medium"]
hard_qs = [q for q in questions if q["difficulty"] == "Hard"]

# ---------------- SESSION STATE INIT ----------------
defaults = {
    "level": "Easy",                 # Easy | Easy-Medium | Medium | Hard
    "streak": 0,
    "score": 0,
    "total": 0,
    "answered": False,
    "selected_option": None,
    "current_q": random.choice(easy_qs)
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------- QUESTION PICKER ----------------
def get_question():
    if st.session_state.level == "Easy":
        return random.choice(easy_qs)
    elif st.session_state.level in ["Easy-Medium", "Medium"]:
        return random.choice(medium_qs)
    else:
        return random.choice(hard_qs)

# ---------------- UI ----------------
st.title("🧠 Adaptive English Test")

st.write(f"**Level:** {st.session_state.level}")
st.write(f"**Score:** {st.session_state.score} / {st.session_state.total}")
st.write(f"**Correct Streak:** {st.session_state.streak}")

q = st.session_state.current_q
st.subheader(q["question"])

choice = st.radio(
    "Choose an answer:",
    list(q["options"].keys()),
    format_func=lambda x: f"{x}. {q['options'][x]}",
    key="radio_choice"
)

# ---------------- SUBMIT ----------------
if st.button("Submit", disabled=st.session_state.answered):
    st.session_state.answered = True
    st.session_state.selected_option = choice
    st.session_state.total += 1

    if choice == q["correct_answer"]:
        st.session_state.score += 1
        st.session_state.streak += 1
        st.success("✅ Correct")
    else:
        st.session_state.streak = 0
        st.error("❌ Wrong")

# ---------------- FEEDBACK + NEXT ----------------
if st.session_state.answered:
    st.info(
        f"**Your Answer:** {st.session_state.selected_option}\n\n"
        f"**Correct Answer:** {q['correct_answer']} — {q['options'][q['correct_answer']]}"
    )
    st.write("📘 **Explanation:**")
    st.write(q["explanation"])

    if st.button("Next Question"):
        # -------- ADAPTIVE LOGIC --------
        if st.session_state.level == "Easy":
            if st.session_state.streak == 3:
                st.session_state.level = "Easy-Medium"
                st.session_state.streak = 0

        elif st.session_state.level == "Easy-Medium":
            if st.session_state.streak == 3:
                st.session_state.level = "Medium"
                st.session_state.streak = 0
            elif st.session_state.streak == 0:
                st.session_state.level = "Easy"

        elif st.session_state.level == "Medium":
            if st.session_state.streak == 3:
                st.session_state.level = "Hard"
                st.session_state.streak = 0
            elif st.session_state.streak == 0:
                st.session_state.level = "Easy"

        elif st.session_state.level == "Hard":
            if st.session_state.streak == 0:
                st.session_state.level = "Medium"

        # -------- RESET UI STATE --------
        st.session_state.current_q = get_question()
        st.session_state.answered = False
        st.session_state.selected_option = None
        st.rerun()
