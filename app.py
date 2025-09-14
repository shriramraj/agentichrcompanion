import streamlit as st
from agent import run_agent
import json

st.set_page_config(page_title="TalentCraft: Your AI Hiring Architect", layout="centered")
st.title("✨ TalentCraft: Your AI Hiring Architect ✨")

st.markdown(
    """
    <style>
    .big-font {font-size: 24px !important;}
    .creative-header {color: #6c32a8; font-weight: bold; font-size: 22px;}
    .creative-section {background-color: #f3e8ff; border-radius: 10px; padding: 14px; margin-bottom: 10px;}
    .role-list {color: #1976d2; font-size: 20px; font-weight: bold;}
    </style>
    """,
    unsafe_allow_html=True,
)

for k, v in {
    "roles": [],
    "clarified": False,
    "answers": {},
    "awaiting_clarification": False,
    "output": {},
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def reset_all():
    for k in ["roles", "clarified", "answers", "awaiting_clarification", "output"]:
        st.session_state[k] = [] if isinstance(st.session_state[k], list) else False if isinstance(st.session_state[k], bool) else {} if isinstance(st.session_state[k], dict) else None
    st.rerun()

output = st.session_state.get("output", {})

if st.session_state["awaiting_clarification"]:
    st.markdown('<div class="creative-header">🔍 Let\'s Sharpen Your Hiring Vision!</div>', unsafe_allow_html=True)
    st.info("Before we craft your hiring masterpiece, could you answer these for me?")
    for i, q in enumerate(output.get("clarifying_questions", []), 1):
        st.markdown(f"**{i}. {q}**")
    st.warning(
        "🎨 *Paint me a quick picture*: Answer each question above in order, separated by semicolons. (Example: `100k; Python, ML; 2 months; Remote`)"
    )
    answer_input = st.text_input("Type your creative answers here:", key="answer_input")
    if st.button("Submit My Masterpiece"):
        output, new_state = run_agent(
            answer_input,
            {
                "roles": st.session_state["roles"],
                "clarified": st.session_state["clarified"],
                "answers": st.session_state["answers"],
                "awaiting_clarification": st.session_state["awaiting_clarification"],
            },
        )
        for k in new_state:
            st.session_state[k] = new_state[k]
        st.session_state["output"] = output
else:
    st.markdown('<div class="creative-header">🛠️ Dream Up Your Team</div>', unsafe_allow_html=True)
    user_input = st.text_input(
        "Who are your dream hires? (e.g. 'We need a Product Manager, a Frontend Developer and a Data Alchemist')",
        key="user_input"
    )
    if st.button("Cast My Hiring Spell"):
        output, new_state = run_agent(
            user_input,
            {
                "roles": st.session_state["roles"],
                "clarified": st.session_state["clarified"],
                "answers": st.session_state["answers"],
                "awaiting_clarification": st.session_state["awaiting_clarification"],
            },
        )
        for k in new_state:
            st.session_state[k] = new_state[k]
        st.session_state["output"] = output

output = st.session_state.get("output", {})
if output and not st.session_state["awaiting_clarification"]:
    if "error" in output:
        st.error("😬 Oops! " + output["error"])
    elif "roles" in output:
        st.markdown('<div class="creative-header">🚀 Your Talent Blueprint</div>', unsafe_allow_html=True)
        roles = output.get('roles', [])
        role_titles = [r.get('title', str(r)) for r in roles if isinstance(r, dict)]
        st.markdown(f"<div class='role-list'>🌟 {', '.join(role_titles)} 🌟</div>", unsafe_allow_html=True)
        st.markdown('<div class="creative-header">📝 Job Descriptions Crafted</div>', unsafe_allow_html=True)
        for jd in output.get('job_descriptions', []):
            st.markdown(f'<div class="creative-section">{jd}</div>', unsafe_allow_html=True)
        st.markdown('<div class="creative-header">🧭 Hiring Quest Checklist</div>', unsafe_allow_html=True)
        for i, checklist in enumerate(output.get('checklists', [])):
            st.markdown(f"<b>{role_titles[i]}</b>", unsafe_allow_html=True)
            st.markdown('\n'.join([f"- {item}" for item in checklist]))
        st.markdown('<div class="creative-header">💾 JSON Blueprint</div>', unsafe_allow_html=True)
        st.code(json.dumps(output, indent=2), language="json")

# Reset button at the bottom. Always works.
if st.button("Start Over"):
    reset_all()