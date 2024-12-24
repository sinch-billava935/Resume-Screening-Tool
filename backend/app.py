from flask import Flask, request, jsonify, render_template
import os
from resume_parse import extract_name, extract_email, extract_phone, extract_skills, extract_experience, extract_education, extract_text_from_file
from fuzzywuzzy import fuzz

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx'}

# Job role-specific requirements
job_role_requirements = {
    'Software Developer': {
        'skills': ['Python', 'Java', 'C++', 'JavaScript', 'Spring Boot', 'HTML', 'CSS'],
        'experience': 2,  # Minimum years of experience
        'education': 'B.Tech in Computer Science or IT'
    },
    'Data Scientist': {
        'skills': ['Python', 'R', 'SQL', 'Machine Learning', 'Data Analysis', 'Pandas', 'TensorFlow'],
        'experience': 2,
        'education': 'B.Tech in Computer Science or M.Sc. in Data Science'
    },
    'Database Administrator': {
        'skills': ['SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Database Optimization', 'Database Security'],
        'experience': 3,
        'education': 'B.Tech in Computer Science or IT'
    },
    'DevOps Engineer': {
        'skills': ['AWS', 'Docker', 'Kubernetes', 'CI/CD', 'Terraform', 'Jenkins', 'Cloud Computing'],
        'experience': 2,
        'education': 'B.Tech in Computer Science or IT'
    },
    'Machine Learning Engineer': {
        'skills': ['Python', 'TensorFlow', 'PyTorch', 'Scikit-learn', 'Deep Learning', 'Natural Language Processing'],
        'experience': 3,
        'education': 'B.Tech in Computer Science or M.Sc. in Machine Learning'
    },
    'Cloud Engineer': {
        'skills': ['AWS', 'Azure', 'Google Cloud', 'Serverless Architecture', 'Cloud Security', 'DevOps'],
        'experience': 2,
        'education': 'B.Tech in Computer Science or IT'
    },
    'Network Engineer': {
        'skills': ['Routing', 'Switching', 'Firewall', 'VPN', 'Networking Protocols', 'Cisco', 'LAN/WAN'],
        'experience': 2,
        'education': 'B.Tech in Electronics/Telecommunication or Computer Science'
    },
    '   ': {
        'skills': ['Penetration Testing', 'Firewalls', 'Incident Response', 'Cryptography', 'Vulnerability Assessment'],
        'experience': 2,
        'education': 'B.Tech in Computer Science or M.Sc. in Cyber Security'
    },
    'Project Manager': {
        'skills': ['Project Planning', 'Agile', 'Scrum', 'Stakeholder Management', 'Risk Management', 'Leadership'],
        'experience': 5,  # Project managers often require more years of experience
        'education': 'B.Tech or MBA in Project Management'
    },
    'Full Stack Developer': {
        'skills': ['React', 'Node.js', 'Express.js', 'MongoDB', 'HTML/CSS', 'JavaScript', 'MySQL'],
        'experience': 2,
        'education': 'B.Tech in Computer Science or IT'
    }
}

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

        if not allowed_file(resume.filename):
            return jsonify({'error': 'Only .docx and .pdf files are supported.'}), 400

        resume_text = extract_text_from_file(resume)

        if job_role not in job_role_requirements:
            return jsonify({'error': f"Job role '{job_role}' is not defined."}), 400

        job_requirements = job_role_requirements[job_role]
        required_skills = job_requirements['skills']
        required_experience = job_requirements['experience']
        required_education = job_requirements['education']

        matched_skills = extract_skills(resume_text, required_skills)
        raw_experience = extract_experience(resume_text)
        formatted_experience = [point.strip() for point in raw_experience.split('.') if point.strip()]
        education_info = extract_education(resume_text)

        # Score calculations
        max_skill_score = 50  # Adjust as needed
        max_experience_score = 30
        max_education_score = 20

        skill_score = min(len(matched_skills) * (max_skill_score / len(required_skills)), max_skill_score)
        experience_score = min(len(formatted_experience) * 10, max_experience_score) if len(formatted_experience) >= required_experience else 0
        education_score = max_education_score if fuzz.partial_ratio(required_education.lower(), education_info.lower()) >= 65 else 0

        total_max_score = max_skill_score + max_experience_score + max_education_score
        overall_score = ((skill_score + experience_score + education_score) / total_max_score) * 100
        overall_score = round(overall_score, 2)

        verdict = "Selected" if overall_score >= 60 else "Not Selected"

        resume_info = {
            'name': extract_name(resume_text),
            'email': extract_email(resume_text),
            'phone': extract_phone(resume_text),
            'job_role': job_role,
            'skills': matched_skills,
            'experience': formatted_experience,
            'education': education_info,
            'skill_score': skill_score,
            'experience_score': experience_score,
            'education_score': education_score,
            'overall_score': overall_score,
            'verdict': verdict,
            'job_requirements': {
                'required_skills': required_skills,
                'required_experience': required_experience,
                'required_education': required_education,
            }
        }

        return jsonify(resume_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

