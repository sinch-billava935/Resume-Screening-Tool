from flask import Flask, request, jsonify, render_template
import os
from resume_parse import extract_name, extract_email, extract_phone, extract_skills, extract_experience, extract_education, extract_text_from_file

# Initialize the Flask app
app = Flask(__name__)

# Set up the folder for uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure the app to allow specific file extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

# Helper function to check if a file has a valid extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        resume = request.files.get('resume')
        job_role = request.form.get('job_role')  # Getting the job role entered by the user

        if not resume or not job_role:
            return jsonify({'error': 'Resume or job role not provided.'}), 400

        # Ensure the file is either .docx or .pdf
        if not allowed_file(resume.filename):
            return jsonify({'error': 'Only .docx and .pdf files are supported.'}), 400

        # Extract text from the resume
        resume_text = extract_text_from_file(resume)

        # Broad skill set for matching
        skills_list = [
            'Python', 'Java', 'SQL', 'AWS', 'Machine Learning', 'Data Science', 'C++', 'HTML', 'CSS', 
            'JavaScript', 'React', 'Angular', 'Node.js', 'Spring Boot', 'Hibernate', 'JPA', 'REST APIs',
            'SOAP', 'MongoDB', 'MySQL', 'PostgreSQL', 'Docker', 'Kubernetes', 'CI/CD', 'Jenkins', 'Git'
        ]

        # Extract skills from resume text
        matched_skills = extract_skills(resume_text, skills_list)

        # Extract experience and format it as a list of bullet points
        raw_experience = extract_experience(resume_text)
        formatted_experience = [point.strip() for point in raw_experience.split('.') if point.strip()]

        # Extract education details
        education_info = extract_education(resume_text)

        # Example placeholders for score calculations (can be enhanced later)
        skill_score = len(matched_skills) * 10  # Assuming each skill matched adds 10 points
        experience_score = 80  # Placeholder score, can be customized
        education_score = 90  # Placeholder score, can be customized

        # Calculate overall score and verdict
        overall_score = (skill_score + experience_score + education_score) / 3
        verdict = "Selected" if overall_score >= 75 else "Not Selected"

        resume_info = {
            'name': extract_name(resume_text),
            'email': extract_email(resume_text),
            'phone': extract_phone(resume_text),
            'job_role': job_role,  # Include the job role in the response
            'skills': matched_skills,  # Skills as a list
            'experience': formatted_experience,  # Experience as a list
            'education': education_info,  # Education as a string
            'skill_score': skill_score,
            'experience_score': experience_score,
            'education_score': education_score,
            'overall_score': overall_score,
            'verdict': verdict,
            'job_requirements': [90, 100, 85],  # Job requirement thresholds for Skills, Education, Experience
        }

        return jsonify(resume_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)