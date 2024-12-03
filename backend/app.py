from flask import Flask, request, jsonify, render_template
import os
from resume_parse import extract_name, extract_email, extract_phone, extract_skills, extract_text_from_docx

# Initialize the Flask app
app = Flask(__name__)

# Set up the folder for uploaded files
UPLOAD_FOLDER = 'uploads'  # Folder where resumes will be saved
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

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        return jsonify({"message": "File uploaded successfully", "file_name": file.filename}), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    try:
        resume = request.files.get('resume')
        job_role = request.form.get('job_role')

        if not resume or not job_role:
            return jsonify({'error': 'Resume or job role not provided.'}), 400

        # Extract text from resume
        resume_text = extract_text_from_docx(resume)

        # Broad skill set for matching
        skills_list = [
            'Python', 'Java', 'SQL', 'AWS', 'Machine Learning', 'Data Science', 'C++', 'HTML', 'CSS', 
            'JavaScript', 'React', 'Angular', 'Node.js', 'Spring Boot', 'Hibernate', 'JPA', 'REST APIs',
            'SOAP', 'MongoDB', 'MySQL', 'PostgreSQL', 'Docker', 'Kubernetes', 'CI/CD', 'Jenkins', 'Git'
        ]

        # Analyze resume
        resume_info = {
            'name': extract_name(resume_text),
            'email': extract_email(resume_text),
            'phone': extract_phone(resume_text),  # Include phone number
            'skills': extract_skills(resume_text, skills_list),  # Include skills
            'job_role': job_role
        }

        return jsonify(resume_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
