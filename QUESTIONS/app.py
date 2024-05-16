from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
import random

# Create Flask application instance
app = Flask(__name__)

# Configure Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_BINDS'] = {
    'answers': 'sqlite:///answers.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Define database models
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)

class Answer(db.Model):
    __bind_key__ = 'answers'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.String(500), nullable=False)

# Create database tables before the first request
@app.before_first_request
def create_tables():
    db.create_all()

# Home view, for submitting questions
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Route to handle question submissions
@app.route('/submit_question', methods=['POST'])
def submit_question():
    question_content = request.form['question']
    new_question = Question(content=question_content)
    db.session.add(new_question)
    db.session.commit()
    return redirect(url_for('home'))

# Route to display questions
@app.route('/questions', methods=['GET'])
def show_questions():
    questions = Question.query.order_by(db.func.random()).limit(6)
    return render_template('questions.html', questions=questions)

# Route to handle answer submissions
@app.route('/submit_answer/<int:question_id>', methods=['POST'])
def submit_answer(question_id):
    answer_content = request.form['answer']
    new_answer = Answer(question_id=question_id, content=answer_content)
    db.session.add(new_answer)
    db.session.commit()
    return redirect(url_for('show_questions'))

# Run Flask application
if __name__ == '__main__':
    app.run(debug=True)
