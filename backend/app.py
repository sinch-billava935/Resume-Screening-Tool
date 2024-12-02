from flask import Flask, request, jsonify, render_template
import os

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

        # Example logic for processing the resume and job role
        parsed_info = {
            'name': 'John Doe',  # Replace with actual parsed data
            'email': 'johndoe@example.com',
            'job_role': job_role,
            'age': 30,
            'score': 85,  # Replace with actual calculated score
            'skills': {'Python': 80, 'Machine Learning': 70},  # Replace with actual skill analysis
            'job_requirements': {'Python': 90, 'Machine Learning': 80}  # Replace with actual job requirements
        }

        return jsonify(parsed_info)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
