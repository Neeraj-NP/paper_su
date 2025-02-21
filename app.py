from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///papers.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
db = SQLAlchemy(app)

# Models
class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    exam_type = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Hackathon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    registration_link = db.Column(db.String(200))
    posted_at = db.Column(db.DateTime, default=datetime.utcnow)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/papers')
def papers():
    papers = Paper.query.order_by(Paper.uploaded_at.desc()).all()
    return render_template('papers.html', papers=papers)

@app.route('/upload', methods=['GET', 'POST'])
def upload_paper():
    if request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        exam_type = request.form.get('exam_type')
        file = request.files.get('paper_file')
        
        if file:
            filename = f"{year}_{exam_type}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            paper = Paper(
                title=title,
                year=year,
                exam_type=exam_type,
                file_path=filename
            )
            db.session.add(paper)
            db.session.commit()
            flash('Paper uploaded successfully!', 'success')
            return redirect(url_for('papers'))
    
    return render_template('upload.html')

@app.route('/hackathons')
def hackathons():
    hackathons = Hackathon.query.order_by(Hackathon.date.desc()).all()
    return render_template('hackathons.html', hackathons=hackathons)

if __name__ == '__main__':
    if not os.path.exists('static/uploads'):
        os.makedirs('static/uploads')
    with app.app_context():
        db.create_all()
    app.run(debug=True)
