
# app.py
import streamlit as st
from Backend.llm_utils import get_gemini_feedback, llm_feedback
from Backend.evaluation import final_score, get_quality, feedback, keyword_map

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Interview Feedback",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Interview Coach")
st.markdown("""
Enter your interview question and answer below.  
You will get ** Your Answer feedback**, **suggestion**.
""")

# ---------------- SIDEBAR INPUTS ----------------
st.sidebar.header("Input Your Answer")
question = st.sidebar.text_input("Enter Question")
answer = st.sidebar.text_area("Enter Your Answer", height=180)

# ---------------- SUBMIT ----------------
if st.sidebar.button("Submit"):

    if not question or not answer:
        st.warning("⚠ Please enter both question and answer")
    else:
        # 1️⃣ Keyword lookup
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

        # 2️⃣ Rule-based scoring
        score = final_score(answer, keywords)
        quality = get_quality(score)
        rule_fb = feedback(answer, keywords)

        # ---------------- LAYOUT ----------------
        col1, col2, col3 = st.columns(3, gap="large")

        # 3️⃣ RESULT + TRAFFIC LIGHT (INLINE)
        with col1:
            st.subheader("Result")

            if quality.lower() == "weak":
                st.markdown(
                    """
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:14px;height:14px;background:red;
                                    border-radius:50%;box-shadow:0 0 8px red;"></div>
                        <span style="font-size:18px;">Weak</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif quality.lower() == "average":
                st.markdown(
                    """
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:14px;height:14px;background:yellow;
                                    border-radius:50%;box-shadow:0 0 8px yellow;"></div>
                        <span style="font-size:18px;">Average</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:
                st.markdown(
                    """
                    <div style="display:flex; align-items:center; gap:10px;">
                        <div style="width:14px;height:14px;background:green;
                                    border-radius:50%;box-shadow:0 0 8px green;"></div>
                        <span style="font-size:18px;">Good</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        # 4️⃣ RULE-BASED FEEDBACK
        with col2:
            st.subheader("Your Answer Feedback ")
            if rule_fb:
                for r in rule_fb:
                    st.write("•", r)
            else:
                st.write("Looks good 👍")

        # 5️⃣ LLM FEEDBACK
        with col3:
            st.subheader("Suggestion for You")
            with st.spinner("Generating feedback..."):
                prompt = llm_feedback(question, answer, rule_fb, quality)
                llm_result = get_gemini_feedback(prompt)
            st.text_area("AI Feedback", llm_result, height=300)