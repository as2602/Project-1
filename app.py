
import streamlit as st
from Backend.llm_utils import get_gemini_feedback, llm_feedback
from Backend.evaluation import final_score, get_quality, feedback, keyword_map

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Interview Feedback",
    page_icon="🎓",
    layout="wide"
)

# ==================================================
# 🌗 THEME TOGGLE
# ==================================================
st.sidebar.header("🎨 Appearance")
dark_mode = st.sidebar.toggle("Dark Mode", value=False)

# ---------------- THEME STYLES ----------------
if dark_mode:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        textarea, input {
            background-color: #1E1E1E !important;
            color: #FAFAFA !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }
        textarea, input {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------- TITLE ----------------
st.title("🎓 AI Interview Coach")
st.markdown("""
Enter your interview **question** and **answer** below.  
You will receive **result**, **answer feedback**, and **AI suggestions**.
""")

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("📝 Input Your Answer")
question = st.sidebar.text_input("Enter Interview Question")
answer = st.sidebar.text_area("Enter Your Answer", height=180)

# ---------------- SUBMIT ----------------
if st.sidebar.button("Submit"):

    if not question or not answer:
        st.warning("⚠ Please enter both question and answer")

    else:
        # ---------------- KEYWORD LOOKUP ----------------
        keywords = keyword_map.get(question)

        if not keywords:
            st.info("Extracting keywords using AI...")
            keywords_text = get_gemini_feedback(
                f"Extract 5 important keywords as a Python list for this question:\n{question}"
            )
            try:
                import ast
                keywords = ast.literal_eval(keywords_text)
            except:
                keywords = []

        # ---------------- RULE-BASED SCORING ----------------
        score = final_score(answer, keywords)
        quality = get_quality(score)
        rule_fb = feedback(answer, keywords)

        # ==================================================
        # ROW 1 → RESULT + FEEDBACK
        # ==================================================
        col1, col2 = st.columns([1, 2], gap="large")

        # ---------------- RESULT ----------------
        with col1:
            st.subheader("📊 Result")

            if quality.lower() == "weak":
                color = "red"
                label = "Weak"
            elif quality.lower() == "average":
                color = "orange"
                label = "Average"
            else:
                color = "green"
                label = "Good"

            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:12px;">
                    <div style="width:16px;height:16px;
                                background:{color};
                                border-radius:50%;
                                box-shadow:0 0 10px {color};">
                    </div>
                    <span style="font-size:20px; font-weight:600;">
                        {label}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.metric("Score", f"{score}/10")

        # ---------------- RULE-BASED FEEDBACK ----------------
        with col2:
            st.subheader("🧠 Your Answer Feedback")
            if rule_fb:
                for r in rule_fb:
                    st.write("•", r)
            else:
                st.success("Looks good 👍 No major issues found.")

        # ==================================================
        # ROW 2 → AI SUGGESTION
        # ==================================================
        st.subheader("🤖 Suggestion for You")

        with st.spinner("Generating AI feedback..."):
            prompt = llm_feedback(question, answer, rule_fb, quality)
            llm_result = get_gemini_feedback(prompt)

        st.text_area(
            label="AI Feedback",
            value=llm_result,
            height=320
        )
