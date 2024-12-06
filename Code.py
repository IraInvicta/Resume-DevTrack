from dotenv import load_dotenv
import streamlit as st
import os
import PyPDF2
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set up API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBmoxhCE471n-vOUiKY_seamioMC6l6Wpw"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Function to fetch response from Gemini AI
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content([input_text, pdf_content, prompt])
    return response

# Function to extract text from PDF
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        pdf_text = ''
        for page in reader.pages:
            pdf_text += page.extract_text() + '\n'
        if pdf_text.strip() == '':
            raise ValueError("No text found in the PDF file.")
        return pdf_text
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app configuration
st.set_page_config(page_title="ATS Resume Expert")
st.header("GEN-AI MINIONS")

# User inputs: Job Description and Resume
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons for features
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("How Can I Improve My Skills")
submit3 = st.button("Percentage Match")
submit4 = st.button("Suggest Relevant Certifications")  # New feature button

# Prompts for different features
input_prompt1 = """
You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description. 
Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are a career coach with expertise in skill-building and career development. Based on the provided job description and resume, 
suggest actionable skills the candidate should develop or improve to increase their suitability for the job role. 
Include both technical and soft skills.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality. 
Your task is to evaluate the resume against the provided job description. Provide the percentage match if the resume matches
the job description. First, the output should come as a percentage, followed by missing keywords, and lastly, your final thoughts.
"""

input_prompt4 = """
You are an AI career advisor with extensive knowledge of professional certifications across various domains. 
Based on the given job description and resume, suggest relevant certifications that can enhance the candidate's profile 
and increase their suitability for the role.
"""

# Feature: Tell Me About the Resume
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt1)
        st.subheader("The Response is")
        st.write(response.text)
    else:
        st.write("Please upload the resume")

# Feature: How Can I Improve My Skills
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt2)
        st.subheader("Skill Improvement Suggestions")
        st.write(response.text)
    else:
        st.write("Please upload the resume")

# Feature: Percentage Match
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt3)
        st.subheader("The Response is")
        st.write(response.text)
    else:
        st.write("Please upload the resume")

# New Feature: Suggest Relevant Certifications
elif submit4:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_text, pdf_content, input_prompt4)
        st.subheader("Suggested Certifications")
        st.write(response.text)
    else:
        st.write("Please upload the resume")
