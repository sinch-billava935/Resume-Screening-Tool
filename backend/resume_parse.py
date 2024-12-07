import pdfplumber
from docx import Document
import re

def extract_text_from_file(file):
    """ Extract text from a .docx or .pdf resume file. """
    if file.filename.endswith('.docx'):
        doc = Document(file)
        text = [para.text for para in doc.paragraphs]
        return '\n'.join(text)
    elif file.filename.endswith('.pdf'):
        with pdfplumber.open(file) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            return '\n'.join(pages)
    else:
        raise ValueError("Unsupported file format. Only .docx and .pdf are supported.")

def extract_name(text):
    """ Extract the candidate's name based on the assumption that the first non-empty line is the name. """
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if line:
            return line
    return None

def extract_email(text):
    """ Extract email using regex. """
    match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    """ Extract phone numbers using regex. """
    match = re.search(r'\+?\d{1,4}[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match.group(0) if match else None

def extract_skills(text, skills_list):
    """ Match skills from the given list in the resume text. """
    skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            skills.append(skill)
    return skills

def extract_experience(text):
    """ Extract experience section from the resume using keywords. """
    experience_keywords = ['Experience', 'Professional Experience', 'Work History']
    pattern = r'(?i)(?:' + '|'.join(experience_keywords) + r')[:\s]?.*?(?=Education|Qualifications|Skills|$)'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(0).strip() if match else "Not Found"



def extract_education(text):
    """ Extract only the education section from the resume. """
    education_keywords = ['Education', 'Educational Background', 'Academic Qualifications']
    # Pattern to capture content that follows education-related keywords
    # The key change is that the regex specifically looks for content related to education and stops before encountering certifications or internships.
    pattern = r'(?i)(?:' + '|'.join(education_keywords) + r')[:\s]?.*?(?=Certifications|Internships|Experience|Skills|$)'
    
    match = re.search(pattern, text, re.DOTALL)
    
    # Return the matched education section, or 'Not Found' if no match is found
    return match.group(0).strip() if match else "Not Found"
