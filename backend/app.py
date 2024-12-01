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

# Route to render the main page (index.html)
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle resume upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'resume' not in request.files:  # Check if file is in the request
        return jsonify({"error": "No file part"}), 400

    file = request.files['resume']  # Get the file from the form

    if file.filename == '':  # Check if no file was selected
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):  # Check if the file is allowed
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)  # Save the file to the uploads folder
        return jsonify({"message": "File uploaded successfully", "file_name": file.filename}), 200
    else:
        return jsonify({"error": "Invalid file format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
