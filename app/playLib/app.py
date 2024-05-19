from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///madlib.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class MadLib(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story = db.Column(db.String(1000), nullable=False)
    questions = db.Column(db.String(1000), nullable=False)

@app.before_first_request
def initialize_database():
    db.create_all()  # create table

    # check data counts
    if MadLib.query.count() == 0:
        # insert Mad Libs stories and question
        stories = [
            (
                "In the heart of October, the old {0} transformed into a haunting spectacle for Halloween. Jack, an adventurous {1}-year-old, donned his pirate costume and set sail through the sea of ghosts and goblins. At {2}'s door, instead of the usual treats, kids were dared to reach into a box of \"{3}.\" Jack’s brave plunge into the slimy unknown fetched him a handful of {4}, making him the victorious pirate of the night’s spooky adventures.",
                "Please enter a street name. (like Madlibs Street)|Please enter a number.|Please enter a celebrities' name.|If your mailbox was stuffed full, what would it be filled with? Please enter a noun.|What is your favorite food?"
            ),
            (
                "On a snowy Christmas Eve, {0} wished for a {1}, writing letters to Santa and hoping for a miracle. That night, as the town slept under a blanket of white, a {1} {2} found its way to {0}'s doorstep. The next morning, her squeals of delight upon finding the {2} {3}. {0}'s family welcomed the new member with {4}, and {0} knew her wish had been heard—a true Christmas miracle.",
                "Please enter a girl name.|How would you like to describe a pet? Please enter an adjective.|Please enter a living creature.|What did you do when it was your first time receiving a present?|Please enter a noun."
            ),
            (
                "In a {0} forest, a little rabbit discovered a lost {1} near the stream. Despite being small, the rabbit felt a strong urge to protect the {1} from the {2}. Courageously, the rabbit escorted the {1} across the dense forest, dodging {2} and overcoming {3}, until they found the {1}'s mother. The rabbit's bravery showed that no matter how small you are, you can make a big difference.",
                "How do you describe the place where you are? Please enter an adjective.|Please enter an animal you like.|If there were a dangerous monster, what would it be?|What do you fear the most? Please enter a plural noun.|Who is your favorite family member? Please enter a relative."
            )
        ]

        for story, questions in stories:
            madlib = MadLib(story=story, questions=questions)
            db.session.add(madlib)

        db.session.commit()
        print("Stories inserted into database.")
    else:
        print("Database already contains data. No insertion needed.")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        story = request.form['story']
        num_entries = int(session.get('num_entries', 5))
        words = [request.form[f'word{i}'] for i in range(num_entries)]
        questions = [request.form[f'question{i}'] for i in range(num_entries)]
        questions_str = '|'.join(questions)

        session['story_input'] = story
        session['words_input'] = words
        session['questions_input'] = questions_str

        placeholders = {}
        for i in range(num_entries):
            word = request.form[f'word{i}']
            placeholders[word] = placeholders.get(word, i)

        for word, index in placeholders.items():
            story = story.replace(word, f'{{{index}}}')

        display_story = story
        for i in range(num_entries):
            display_story = display_story.replace(f'{{{i}}}', '____')

        # word/phase checking
        word_check_results = []
        for word in words:
            if word in session['story_input']:
                word_check_results.append('<span style="color:green;">ok</span>')
            else:
                word_check_results.append('<span style="color:red;">&#10060; This word/phrase is not found in the story.</span>')

        return render_template('confirm.html', story=display_story, words=words, questions=questions, word_check_results=word_check_results, num_entries=num_entries)

    story_input = session.get('story_input', '')
    words_input = session.get('words_input', [''] * int(session.get('num_entries', 5)))
    questions_input = session.get('questions_input', '|'.join([''] * int(session.get('num_entries', 5)))).split('|')

    return render_template('createLib.html', story=story_input, words=words_input, questions=questions_input, num_entries=int(session.get('num_entries', 5)))

@app.route('/set_num_entries', methods=['POST'])
def set_num_entries():
    session['num_entries'] = int(request.form['numEntries'])
    session.pop('story_input', None)
    session.pop('words_input', None)
    session.pop('questions_input', None)
    return redirect(url_for('create'))

@app.route('/clear', methods=['POST'])
def clear():
    return '', 204

@app.route('/confirm', methods=['POST'])
def confirm():
    story = session.get('story_input')
    questions = session.get('questions_input')
    new_madlib = MadLib(story=story, questions=questions)
    db.session.add(new_madlib)
    db.session.commit()
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True)
