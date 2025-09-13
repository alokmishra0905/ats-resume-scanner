from flask import Flask, render_template, request
from extensions import db
from utils import extract_resume_data, calculate_ats_score
from utils import extract_resume_data, calculate_ats_score
from models import Resume
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['resume']
    job_desc = request.form['job_description']

    if file.filename == '':
        return 'No file selected'

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    data = extract_resume_data(filepath)
    ats_score = calculate_ats_score(data['raw_text'], job_desc)

    resume = Resume(name=data['name'], email=data['email'], skills=data['skills'])
    db.session.add(resume)
    db.session.commit()

    return render_template('result.html', data=data, ats_score=ats_score)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
