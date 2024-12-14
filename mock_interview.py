import pyttsx3
import speech_recognition as sr
import google.generativeai as genai
import streamlit as st

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak text using TTS
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's response using speech-to-text
def listen_to_user():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        st.write("Listening for your answer...")
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            return user_input
        except sr.UnknownValueError:
            speak_text("Sorry, I couldn't understand that. Could you please repeat?")
            return None
        except sr.RequestError:
            speak_text("Sorry, I am having trouble connecting to the speech recognition service.")
            return None

# Function to fetch response from Gemini AI based on user input and job description
def get_mock_interview_response(input_text, job_description, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([input_text, job_description, prompt])
    return response

# Streamlit UI elements
st.header("Real-Time Mock Interview")
job_description = st.text_area("Job Description: ", key="job_desc")
start_interview_button = st.button("Start Mock Interview")

# Mock Interview Flow
if start_interview_button:
    if job_description:
        # Ask the first question related to the job description
        speak_text("Welcome to the mock interview. I will ask you questions based on the job description.")
        st.write("Starting mock interview...")
        
        input_prompt = """
        You are an interview panelist for a job. Ask relevant questions to the candidate based on the job description provided.
        After the candidate answers, evaluate the response based on industry standards and provide constructive feedback.
        """
        
        # Initial question based on the job description
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        first_question = model.generate_content([job_description, input_prompt])
        question_text = first_question.text.strip()

        # Speak the first question
        speak_text(question_text)
        st.write(f"Question: {question_text}")
        
        # Listen to candidate's answer
        user_answer = listen_to_user()

        if user_answer:
            st.write(f"Your answer: {user_answer}")
            # Fetch feedback for the candidate's answer
            feedback_prompt = """
            You are a hiring manager. Based on the candidate's response and the job description provided, 
            evaluate the candidate's answer. Provide feedback on how well the answer matches the job requirements.
            """
            feedback_response = get_mock_interview_response(user_answer, job_description, feedback_prompt)
            st.subheader("Feedback:")
            st.write(feedback_response.text)
        else:
            st.write("No answer detected. Please try again.")
    else:
        st.write("Please provide the job description to start the mock interview.")
