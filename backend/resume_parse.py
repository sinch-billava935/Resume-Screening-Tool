import re
from docx import Document

def extract_name(text):
    """
    Extract the candidate's name based on the assumption that the first non-empty line is the name.
    """
    lines = text.splitlines()
    for line in lines:
        line = line.strip()  # Remove extra spaces
        if line:  # Check if the line is not empty
            return line  # Return the first non-empty line
    return None  # Fallback if no valid line is found

def extract_email(text):
    """
    Extract email using regex.
    """
    match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    return match.group(0) if match else None

def extract_phone(text):
    """
    Extract phone numbers using regex.
    """
    match = re.search(r'\+?\d{1,4}[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    return match.group(0) if match else None

def extract_skills(text, skills_list):
    """
    Match skills from the given list in the resume text.
    """
    skills = []
    for skill in skills_list:
        if skill.lower() in text.lower():
            skills.append(skill)
    return skills

def extract_experience(text):
    """
    Extract experience section from the resume using keywords.
    """
    experience_keywords = ['Experience', 'Professional Experience', 'Work History']
    pattern = r'(?i)(?:' + '|'.join(experience_keywords) + r')[:\s]?.*?(?=Education|Qualifications|Skills|$)'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(0).strip() if match else "Not Found"

def extract_education(text):
    """
    Extract education section from the resume using keywords.
    """
    education_keywords = ['Education', 'Educational Background', 'Academic Qualifications']
    pattern = r'(?i)(?:' + '|'.join(education_keywords) + r')[:\s]?.*?(?=Experience|Professional Experience|Skills|$)'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(0).strip() if match else "Not Found"

def extract_text_from_docx(file_path):
    """
    Extract text from a .docx resume file using python-docx.
    """
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)

# Example usage
if __name__ == "__main__":
    file_path = r'C:\Users\Sinchana T\Downloads\Resume_dataset\Resumes\Rashmitha R.docx'
    resume_text = extract_text_from_docx(file_path)

    # Broad skill set for matching
    skills_list = [
        'Python', 'Java', 'SQL', 'AWS', 'Machine Learning', 'Data Science', 'C++', 'HTML', 'CSS', 
        'JavaScript', 'React', 'Angular', 'Node.js', 'Spring Boot', 'Hibernate', 'JPA', 'REST APIs',
        'SOAP', 'MongoDB', 'MySQL', 'PostgreSQL', 'Docker', 'Kubernetes', 'CI/CD', 'Jenkins', 'Git'
    ]

    resume_info = {
        'name': extract_name(resume_text),
        'email': extract_email(resume_text),
        'phone': extract_phone(resume_text),
        'skills': extract_skills(resume_text, skills_list),
        'experience': extract_experience(resume_text),
        'education': extract_education(resume_text)
    }

    print(resume_info)
