# Backend/llm_utils.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load env vars
load_dotenv()

IS_PRODUCTION = os.getenv("IS_PRODUCTION") == "true"

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-flash-latest")


def get_gemini_feedback(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"


def llm_feedback(question, user_answer, rule_feedback, quality, language="english"):
    return f"""
You are an AI interview coach for freshers.

Question:
{question}

User Answer:
{user_answer}

Rule-based Evaluation:
Quality: {quality}
Issues: {rule_feedback}

Your task:
1. Explain WHY the answer is weak or incorrect in simple words
2. Give an IMPROVED correct answer
3. Keep the tone friendly and fresher-level
4. Language: {language}

Return response in this format:
- Reason:
- Improved Answer:
"""


def generate_keywords_from_llm(question):
    prompt = f"""
You are an AI interviewer.

Extract 5–7 important technical keywords for the following interview question.

Question:
{question}

Return ONLY a Python list.
"""
    try:
        response = model.generate_content(prompt)
        return eval(response.text.strip())
    except Exception as e:
        print("Keyword generation failed:", e)
        return []


# # ---------------- SAFE AUDIO FUNCTIONS ---------------- #

# def speak(text):
#     """
#     Text-to-speech (DISABLED in production).
#     """
#     if IS_PRODUCTION:
#         return  # Do nothing on Render

#     import pyttsx3
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()


# def listen():
#     """
#     Speech-to-text (DISABLED in production).
#     """
#     if IS_PRODUCTION:
#         return ""

#     import speech_recognition as sr
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         audio = r.listen(source, timeout=5)
#     try:
#         return r.recognize_google(audio)
#     except:
#         return ""
