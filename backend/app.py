from flask import Flask, request, jsonify, render_template
import os
from resume_parse import extract_name, extract_email, extract_phone, extract_skills, extract_experience, extract_education, extract_text_from_docx

# Initialize the Flask app
app = Flask(__name__)

# Set up the folder for uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure the app to allow specific file extensions
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt'}

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
        job_role = request.form.get('job_role')

        if not resume or not job_role:
            return jsonify({'error': 'Resume or job role not provided.'}), 400

        # Ensure the file is a .docx file
        if not resume.filename.endswith('.docx'):
            return jsonify({'error': 'Only .docx files are supported.'}), 400

        # Extract text from the resume
        resume_text = extract_text_from_docx(resume)

        # Broad skill set for matching
        skills_list = [
            'Python', 'Java', 'SQL', 'AWS', 'Machine Learning', 'Data Science', 'C++', 'HTML', 'CSS', 
            'JavaScript', 'React', 'Angular', 'Node.js', 'Spring Boot', 'Hibernate', 'JPA', 'REST APIs',
            'SOAP', 'MongoDB', 'MySQL', 'PostgreSQL', 'Docker', 'Kubernetes', 'CI/CD', 'Jenkins', 'Git'
        ]

        # Analyze the resume
        raw_experience = extract_experience(resume_text)
        # Format the experience and remove unwanted characters
        formatted_experience = [point.strip().replace('\xa0', ' ') for point in raw_experience.split('.') if point.strip()]

        print(f"Formatted Experience: {formatted_experience}")  # Debugging: Check the structure of experience

        resume_info = {
            'name': extract_name(resume_text),
            'email': extract_email(resume_text),
            'phone': extract_phone(resume_text),
            'skills': extract_skills(resume_text, skills_list),
            'job_role': job_role,
            'experience': formatted_experience,  # This should be an array of bullet points
            'education': extract_education(resume_text)
        }

        return jsonify(resume_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
