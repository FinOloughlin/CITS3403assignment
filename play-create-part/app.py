from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'madlib.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class MadLib(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story = db.Column(db.String(1000), nullable=False)
    questions = db.Column(db.String(1000), nullable=False)
    placeholders = db.Column(db.String(1000), nullable=False)

@app.before_first_request
def initialize_database():
    try:
        db.create_all()

        # check data counts
        if MadLib.query.count() == 0:
            # insert Mad Libs stories, questions and placeholders
            stories = [
                (
                    "In the heart of October, the old {0} transformed into a haunting spectacle for Halloween. Jack, an adventurous {1}-year-old, donned his pirate costume and set sail through the sea of ghosts and goblins. At {2}'s door, instead of the usual treats, kids were dared to reach into a box of \"{3}.\" Jack’s brave plunge into the slimy unknown fetched him a handful of {4}, making him the victorious pirate of the night’s spooky adventures.",
                    "Please enter a street name. (like Madlibs Street)|Please enter a number.|Please enter a celebrities' name.|If your mailbox was stuffed full, what would it be filled with?|What is your favorite food?",
                    "noun|number|name|plural nouns|noun"
                ),
                (
                    "On a snowy Christmas Eve, {0} wished for a {1}, writing letters to Santa and hoping for a miracle. That night, as the town slept under a blanket of white, a {1} {2} found its way to {0}'s doorstep. The next morning, her squeals of delight upon finding the {2} {3}. {0}'s family welcomed the new member with {4}, and {0} knew her wish had been heard—a true Christmas miracle.",
                    "Please enter a girl name.|How would you like to describe a pet? Please enter an adjective.|Please enter a living creature.|What did you do when it was your first time receiving a present?|Please enter a noun.",
                    "name|adjective|living creature|phrase starts with past tense verb|noun"
                ),
                (
                    "In a {0} forest, a little rabbit discovered a lost {1} near the stream. Despite being small, the rabbit felt a strong urge to protect the {1} from the {2}. Courageously, the rabbit escorted the {1} across the dense forest, dodging {2} and overcoming {3}, until they found the {1}'s mother. The rabbit's bravery showed that no matter how small you are, you can make a big difference.",
                    "How do you describe the place where you are? Please enter an adjective.|Please enter an animal you like.|If there were a dangerous monster, what would it be?|What do you fear the most? Please enter a plural noun.|Who is your favorite family member? Please enter a relative.",
                    "adjective|animal|monster|plural noun|relative"
                )
            ]

            for story, questions, placeholders in stories:
                madlib = MadLib(story=story, questions=questions, placeholders=placeholders)
                db.session.add(madlib)

            db.session.commit()
        else:
            pass
    except Exception as e:
        print(f"Error initializing the database: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        story = request.form['story']
        words = session.get('words_input', [])
        questions = session.get('questions_input', [])
        next_word = request.form.get('next_word')
        next_question = request.form.get('next_question')

        if next_word and next_question:
            words.append(next_word)
            questions.append(next_question)
            session['words_input'] = words
            session['questions_input'] = questions

        if 'submit' in request.form:
            questions_str = '|'.join(questions)
            session['story_input'] = story
            session['questions_input'] = questions_str

            placeholders = {}
            for i, word in enumerate(words):
                placeholders[word] = placeholders.get(word, i)

            for word, index in placeholders.items():
                story = story.replace(word, f'{{{index}}}')


            display_story = story
            for i in range(len(words)):
                display_story = display_story.replace(f'{{{i}}}', '____')

            session['placeholders_input'] = '|'.join(f'{{{i}}}' for i in range(len(words)))

            # check if words are in the story
            word_check_results = []
            for word in words:
                if word in session['story_input']:
                    word_check_results.append('<span style="color:green;">ok</span>')
                else:
                    word_check_results.append('<span style="color:red;">&#10060; This word/phrase is not found in the story.</span>')

            return render_template('confirm.html', story=display_story, words=words, questions=questions, word_check_results=word_check_results, num_entries=len(words))

        return render_template('createLib.html', story=story, words=words, questions=questions, num_entries=len(words))

    session['words_input'] = []
    session['questions_input'] = []
    return render_template('createLib.html', story='', words=[], questions=[], num_entries=0)

@app.route('/clear', methods=['POST'])
def clear():
    session['story_input'] = ''
    session['words_input'] = []
    session['questions_input'] = []
    return '', 204

@app.route('/confirm', methods=['POST'])
def confirm():
    story = session.get('story_input')
    questions = session.get('questions_input')
    placeholders = session.get('placeholders_input')
    new_madlib = MadLib(story=story, questions=questions, placeholders=placeholders)
    db.session.add(new_madlib)
    db.session.commit()
    return redirect(url_for('success'))

@app.route('/revise', methods=['GET', 'POST'])
def revise():
    if request.method == 'POST':
        story = request.form['story']
        words = [request.form[key] for key in request.form.keys() if key.startswith('word')]
        questions = [request.form[key] for key in request.form.keys() if key.startswith('question')]
        num_entries = len(words)
        questions_str = '|'.join(questions)

        session['story_input'] = story
        session['words_input'] = words
        session['questions_input'] = questions_str

        placeholders = {}
        for i, word in enumerate(words):
            placeholders[word] = placeholders.get(word, i)

        for word, index in placeholders.items():
            story = story.replace(word, f'{{{index}}}')


        display_story = story
        for i in range(num_entries):
            display_story = display_story.replace(f'{{{i}}}', '____')

        # # check if words are in the story
        word_check_results = []
        for word in words:
            if word in session['story_input']:
                word_check_results.append('<span style="color:green;">ok</span>')
            else:
                word_check_results.append(
                    '<span style="color:red;">&#10060; This word/phrase is not found in the story.</span>')

        return render_template('confirm.html', story=display_story, words=words, questions=questions,
                               word_check_results=word_check_results, num_entries=num_entries)

    story = session.get('story_input', '')
    words = session.get('words_input', [])
    questions = session.get('questions_input', '').split('|')

    return render_template('revise.html', story=story, words=words, questions=questions, num_entries=len(words))

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/go_back_to_create', methods=['POST'])
def go_back_to_create():
    return redirect(url_for('create'))

@app.route('/play')
def play():
    # randomly extract a madlib game from db
    madlibs = MadLib.query.all()
    if madlibs:
        selected_madlib = random.choice(madlibs)
        session['story'] = selected_madlib.story
        session['questions'] = selected_madlib.questions.split('|')
        session['placeholders'] = selected_madlib.placeholders.split('|')
        session['answers'] = [''] * len(session['questions'])
        session['current_question'] = 0
        return redirect(url_for('play_lib'))
    return "No stories available."

@app.route('/play_lib', methods=['GET', 'POST'])
def play_lib():
    current_question = session.get('current_question', 0)
    questions = session.get('questions', [])
    placeholders = session.get('placeholders', [])
    answers = session.get('answers', [])

    if request.method == 'POST':
        answer = request.form.get('answer')
        answers[current_question] = answer
        session['answers'] = answers
        current_question += 1
        session['current_question'] = current_question

        if current_question >= len(questions):
            return redirect(url_for('display'))

    if current_question < len(questions):
        question = questions[current_question]
        placeholder = placeholders[current_question]
        last_question = (current_question == len(questions) - 1)
        return render_template('playLib.html', question=question, placeholder=placeholder, last_question=last_question)

    return redirect(url_for('display'))

@app.route('/display')
def display():
    story = session.get('story', '')
    answers = session.get('answers', [])
    for i, answer in enumerate(answers):
        story = story.replace(f'{{{i}}}', answer)
    return render_template('display.html', story=story)

if __name__ == '__main__':
    app.run(debug=True)
