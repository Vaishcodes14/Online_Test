import streamlit as st
import json
import random

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_questions():
    with open("data/english.json", "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

# Group by difficulty
easy_qs = [q for q in questions if q["difficulty"] == "Easy"]
medium_qs = [q for q in questions if q["difficulty"] == "Medium"]
hard_qs = [q for q in questions if q["difficulty"] == "Hard"]

# ---------------- SESSION STATE ----------------
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(easy_qs)
    st.session_state.difficulty = "Easy"
    st.session_state.score = 0
    st.session_state.asked = set()
    st.session_state.total = 0

# ---------------- HELPER ----------------
def get_next_question(correct):
    if st.session_state.difficulty == "Easy":
        return random.choice(medium_qs if correct else easy_qs)

    if st.session_state.difficulty == "Medium":
        return random.choice(hard_qs if correct else easy_qs)

    if st.session_state.difficulty == "Hard":
        return random.choice(hard_qs if correct else medium_qs)

# ---------------- UI ----------------
st.title("🧠 Adaptive English Test")
st.write(f"**Current Difficulty:** {st.session_state.difficulty}")
st.write(f"**Score:** {st.session_state.score} / {st.session_state.total}")

q = st.session_state.current_q

st.subheader(q["question"])

choice = st.radio(
    "Choose an answer:",
    list(q["options"].keys()),
    format_func=lambda x: f"{x}. {q['options'][x]}"
)

# ---------------- SUBMIT ----------------
if st.button("Submit Answer"):
    st.session_state.total += 1
    correct = choice == q["correct_answer"]

    if correct:
        st.success("Correct ✅")
        st.session_state.score += 1
    else:
        st.error(f"Wrong ❌ | Correct: {q['correct_answer']}")
        st.info(q["explanation"])

    # Update difficulty
    if st.session_state.difficulty == "Easy":
        st.session_state.difficulty = "Medium" if correct else "Easy"
    elif st.session_state.difficulty == "Medium":
        st.session_state.difficulty = "Hard" if correct else "Easy"
    else:
        st.session_state.difficulty = "Hard" if correct else "Medium"

    # Next question
    st.session_state.current_q = get_next_question(correct)
    st.rerun()
