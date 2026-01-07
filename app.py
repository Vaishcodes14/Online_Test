import streamlit as st
import json
import random
import os

st.set_page_config(page_title="Adaptive English Test", layout="centered")

# ---------------- LOAD QUESTIONS ----------------
@st.cache_data
def load_questions():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base_dir, "data", "english.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

easy_qs = [q for q in questions if q["difficulty"] == "Easy"]
medium_qs = [q for q in questions if q["difficulty"] == "Medium"]
hard_qs = [q for q in questions if q["difficulty"] == "Hard"]

# ---------------- SESSION STATE INIT (SAFE) ----------------
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Easy"

if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(easy_qs)

if "score" not in st.session_state:
    st.session_state.score = 0

if "total" not in st.session_state:
    st.session_state.total = 0

if "correct_streak" not in st.session_state:
    st.session_state.correct_streak = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "selected_option" not in st.session_state:
    st.session_state.selected_option = None

# ---------------- GET NEXT QUESTION ----------------
def get_next_question():
    if st.session_state.difficulty == "Easy":
        pool = easy_qs
    elif st.session_state.difficulty == "Medium":
        pool = medium_qs
    else:
        pool = hard_qs
    return random.choice(pool)

# ---------------- UI ----------------
st.title("🧠 Adaptive English Test")

st.write(f"**Difficulty:** {st.session_state.difficulty}")
st.write(f"**Score:** {st.session_state.score} / {st.session_state.total}")
st.write(f"**Correct Streak:** {st.session_state.correct_streak}")

q = st.session_state.current_q
st.subheader(q["question"])

choice = st.radio(
    "Choose an answer:",
    list(q["options"].keys()),
    format_func=lambda x: f"{x}. {q['options'][x]}",
    key="choice_radio"
)

# ---------------- SUBMIT ----------------
if st.button("Submit", disabled=st.session_state.answered):
    st.session_state.selected_option = choice
    st.session_state.answered = True
    st.session_state.total += 1

    if choice == q["correct_answer"]:
        st.session_state.score += 1
        st.session_state.correct_streak += 1
        st.success("✅ Correct")
    else:
        st.session_state.correct_streak = 0
        st.error("❌ Wrong")

# ---------------- SHOW ANSWER ----------------
if st.session_state.answered:
    st.info(
        f"**Your Answer:** {st.session_state.selected_option}\n\n"
        f"**Correct Answer:** {q['correct_answer']} — {q['options'][q['correct_answer']]}"
    )
    st.write("📘 **Explanation:**")
    st.write(q["explanation"])

    if st.button("Next Question"):
        # Adaptive rule: 3 correct → level up
        if st.session_state.correct_streak >= 3:
            if st.session_state.difficulty == "Easy":
                st.session_state.difficulty = "Medium"
            elif st.session_state.difficulty == "Medium":
                st.session_state.difficulty = "Hard"
            st.session_state.correct_streak = 0

        st.session_state.current_q = get_next_question()
        st.session_state.answered = False
        st.session_state.selected_option = None
        st.rerun()
