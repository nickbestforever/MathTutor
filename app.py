import streamlit as st
import os
from src.tutor import TutorEngine

st.set_page_config(page_title="MathTutor: Interactive LA", page_icon="📐", layout="centered")

@st.cache_resource
def get_tutor():
    return TutorEngine("task_bank.json")

tutor = get_tutor()

st.title("📐 MathTutor: Verification-Guided Practice System for Linear Algebra")
st.markdown("Interactive Linear Algebra practice system backed by an independent symbolic math engine (`SymPy`).")

tasks = tutor.tasks
if not tasks:
    st.error("The task bank is empty or `task_bank.json` was not found!")
    st.stop()

# Strict ordering of all 9 topics
ordered_topics = [
    "1. Determinants",
    "2. Matrix Multiplication",
    "3. Inverse Matrix",
    "4. Matrix Equations",
    "5. Cramer's Rule",
    "6. Inverse Matrix SLAE",
    "7. Matrix Rank",
    "8. Gaussian Elimination",
    "9. Fundamental Solution Set"
]

available_topics = [t for t in ordered_topics if any(task["topic"] == t for task in tasks)]

# Session state initialization for topics and tasks
if "topic_idx" not in st.session_state:
    st.session_state["topic_idx"] = 0

if "task_idx" not in st.session_state:
    st.session_state["task_idx"] = 0

# Progress dictionary across topics
if "completed_topics" not in st.session_state:
    st.session_state["completed_topics"] = {t: False for t in available_topics}

current_topic = available_topics[st.session_state["topic_idx"] % len(available_topics)]

# --- SIDEBAR: NAVIGATION & TOPICS PROGRESS ---
st.sidebar.header("🧭 Navigation & Progress")
st.sidebar.markdown("Select a topic:")

for i, t in enumerate(ordered_topics):
    if t in available_topics:
        is_done = st.session_state["completed_topics"].get(t, False)
        is_current = (t == current_topic)
        icon = "✅" if is_done else "⏳"
        
        button_label = f"{'👉 ' if is_current else '   '}{t} [{icon}]"
        
        if st.sidebar.button(button_label, key=f"nav_topic_{i}"):
            st.session_state["topic_idx"] = available_topics.index(t)
            st.session_state["task_idx"] = 0
            st.rerun()
    else:
        st.sidebar.text(f"   {t} [🔒]")

# Current topic tasks
topic_tasks = [t for t in tasks if t["topic"] == current_topic]
if st.session_state["task_idx"] >= len(topic_tasks):
    st.session_state["task_idx"] = 0

current_task = topic_tasks[st.session_state["task_idx"]]

# Reset session state on task change
task_session_key = f"{current_topic}_{current_task['id']}"
if "active_task_key" not in st.session_state or st.session_state["active_task_key"] != task_session_key:
    st.session_state["active_task_key"] = task_session_key
    st.session_state["attempts"] = 0
    st.session_state["hint_index"] = 0
    st.session_state["solved"] = False

st.subheader(current_task["title"])
st.write(current_task["description"])

# Secure image rendering with fallback
img_rel_path = current_task.get("image_path")
is_image_valid = False

if img_rel_path:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(base_dir, img_rel_path)
    
    if os.path.exists(img_path) and os.path.getsize(img_path) > 0:
        try:
            st.image(img_path, caption=current_task["title"], use_container_width=True)
            is_image_valid = True
        except Exception:
            is_image_valid = False

if not is_image_valid:
    st.info("ℹ️ Graphical condition is loading or missing. Review the input data structure below:")
    if "matrix" in current_task["input_data"]:
        st.code(str(current_task["input_data"]["matrix"]), language="text")
    elif "coefficients" in current_task["input_data"]:
        st.write("Coefficients:", current_task["input_data"]["coefficients"])
        st.write("Free terms:", current_task["input_data"]["free_terms"])

# Dynamic input label based on topic
if "Determinants" in current_task["topic"] or "Matrix Rank" in current_task["topic"]:
    input_label = "Your answer (number, e.g., -30):"
else:
    input_label = "Your answer (comma or semicolon ';' separated rows/elements):"

user_input = st.text_input(input_label, key="user_answer_input")

# --- BUTTON STYLING ---
st.markdown("""
    <style>
    div.stButton > button {
        white-space: nowrap !important;
        font-size: 13px !important;
        padding: 6px 8px !important;
        border-radius: 6px !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Control panel buttons: Prev Topic, Prev Task, Check, Next Task, Next Topic
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("⏮️ Prev Topic"):
        st.session_state["topic_idx"] = (st.session_state["topic_idx"] - 1) % len(available_topics)
        st.session_state["task_idx"] = 0
        st.rerun()

with c2:
    if st.button("⬅️ Prev Task"):
        if len(topic_tasks) > 1:
            st.session_state["task_idx"] = (st.session_state["task_idx"] - 1) % len(topic_tasks)
            st.rerun()

with c3:
    if st.button("🔍 Check Answer"):
        if not st.session_state["solved"]:
            st.session_state["attempts"] += 1
            result = tutor.evaluate_attempt(current_task, user_input)
            
            if result.get("error"):
                st.error(result["error"])
            elif result["is_correct"]:
                st.success(result["message"])
                st.session_state["solved"] = True
                st.session_state["completed_topics"][current_topic] = True
            else:
                st.error(result["message"])
                hints = current_task.get("hints", [])
                h_idx = st.session_state["hint_index"]
                if h_idx < len(hints):
                    st.warning(f"💡 Hint #{h_idx + 1}: {hints[h_idx]}")
                    st.session_state["hint_index"] = min(h_idx + 1, len(hints) - 1)

with c4:
    if st.button("➡️ Next Task"):
        if len(topic_tasks) > 1:
            st.session_state["task_idx"] = (st.session_state["task_idx"] + 1) % len(topic_tasks)
            st.rerun()

with c5:
    if st.button("⏭️ Next Topic"):
        st.session_state["topic_idx"] = (st.session_state["topic_idx"] + 1) % len(available_topics)
        st.session_state["task_idx"] = 0
        st.rerun()

# Reset button and session status in the sidebar
st.sidebar.markdown("---")
if st.sidebar.button("🔄 Try Again"):
    st.session_state["attempts"] = 0
    st.session_state["hint_index"] = 0
    st.session_state["solved"] = False
    st.rerun()

status_text = "Solved ✅" if st.session_state['solved'] else "In Progress ⏳"
st.sidebar.markdown(f"**Current Topic:** {current_topic}\n\n**Attempts:** {st.session_state['attempts']}\n\n**Status:** {status_text}")