import streamlit as st
import json
import random
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Adaptive English Test", layout="centered")

# ---------------- LOAD QUESTIONS ----------------
@st.cache_data
def load_questions():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "english.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions()

# ---------------- GROUP BY DIFFICULTY ----------------
easy_qs = [q for q in questions if q["difficulty"] == "Easy"]
medium_qs = [q for q in questions if q["difficulty"] == "Medium"]
hard_qs = [q for q in questions if q["difficulty"] == "Hard"]

# ---------------- SESSION STATE INIT ----------------
if "current_q" not in st.session_state:
    st.session_state.current_q = random.choice(easy_qs)
    st.session_state.difficulty = "Easy"
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.used_ids = set()

# ---------------- HELPER FUNCTION ----------------
def get_next_question(correct):
    if st.session_state.difficulty == "Easy":
        pool = medium_qs if correct else easy_qs
        st.session_state.difficulty = "Medium" if correct else "Easy"

    elif st.session_state.difficulty == "Medium":
        pool = hard_qs if correct else easy_qs
        st.session_state.difficulty = "Hard" if correct else "Easy"

    else:  # Hard
        pool = hard_qs if correct else medium_qs
        st.session_state.difficulty = "Hard" if correct else "Medium"

    remaining = [q for q in pool if q["id"] not in st.session_state.used_ids]
    return random.choice(remaining if remaining else pool)

# ---------------- UI ----------------
st.title("🧠 Adaptive English Test")

st.write(f"**Difficulty:** {st.session_state.difficulty}")
st.write(f"**Score:** {st.session_state.score} / {st.session_state.total}")

q = st.session_state.current_q
st.session_state.used_ids.add(q["id"])

st.subheader(q["question"])

choice = st.radio(
    "Choose the correct answer:",
    list(q["options"].keys()),
    format_func=lambda x: f"{x}. {q['options'][x]}"
)

# ---------------- SUBMIT ----------------
if st.button("Submit Answer"):
    st.session_state.total += 1
    correct = choice == q["correct_answer"]

    if correct:
        st.success("✅ Correct")
        st.session_state.score += 1
    else:
        st.error(f"❌ Wrong | Correct Answer: {q['correct_answer']}")
        st.info(q["explanation"])

    st.session_state.current_q = get_next_question(correct)
    st.rerun()
