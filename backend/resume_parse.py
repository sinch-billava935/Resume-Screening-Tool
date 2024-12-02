import textract
import re

def parse_resume(file):
    text = textract.process(file).decode('utf-8')
    # Logic to parse fields
    return {
        'name': extract_name(text),
        'email': extract_email(text),
        'phone': extract_phone(text),
        'skills': extract_skills(text),
    }

def extract_email(text):
    match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    return match.group(0) if match else None

# Add functions for name, phone, and skills
