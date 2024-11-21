# Quiz app using Flask
from flask import Flask, render_template, request, redirect, url_for, session
import random
import json

app = Flask(__name__)

app.secret_key = 'your_secret_key'

#Users for this program
USERS = {"port": "port123",
        "kazman": "kazman123"}

#Home Route
@app.route("/")
def home():
    return render_template('home.html')

#Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('username')
        userpass = request.form.get('password')
        
        # Check the username and password. If successful, take the user to the success page.
        if USERS.get(userid) == userpass:
            session['username'] = userid
            session['score'] = 0
            session['question_num'] = 0
            return redirect(url_for('success', username=userid))
        else:
            return("Sorry bud, please try again")
  
    return render_template('login.html')

#Success route
@app.route('/success/<username>')
def success(username):
    return render_template('success.html', username=username)

#Quiz Route
@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    # Check if user is logged in, otherwise redirect to login page
    if 'username' not in session:
        return redirect(url_for('login'))

    question_num = session.get('question_num', 0)

    # If we reach the end of the questions, redirect to result page
    if question_num >= len(question_list):
        return redirect(url_for('result'))

    # Get the current question and answer options
    current_question, alternatives = question_list[question_num]
    correct_answer = alternatives[0]  # Correct answer is always the first option
    random.shuffle(alternatives)  # Shuffle answer options

    feedback = None  # Initialize feedback

    # Handle form submission
    if request.method == 'POST' and 'answer' in request.form:
        selected_answer = request.form.get('answer')

        # Check if the selected answer is correct
        if selected_answer == correct_answer:
            session['score'] = session.get('score', 0) + 1  # Increase score if correct
            feedback = "Correct!"
        else:
            feedback = f"Incorrect! The correct answer was: {correct_answer}"

        # Move to the next question
        session['question_num'] = question_num + 1

        # Render quiz page again with feedback
        return render_template('quiz.html', 
                               question=current_question,
                               options=alternatives, 
                               score=session['score'], 
                               feedback=feedback)

    # Render quiz page with the current question and options
    return render_template('quiz.html', 
                           question=current_question, 
                           options=alternatives, 
                           score=session['score'], 
                           feedback=feedback)


@app.route('/result')
def result():
    score = session.get('score', 0)  # Get the score from session
    
    total_questions = len(question_list)

    if request.args.get('restart') == 'true':
        session['score'] = 0  # Reset the score
        session['question_num'] = 0  # Reset question number to start fresh
        return redirect(url_for('quiz'))
    
    return render_template('result.html', score=score)


# Load the question file and convert it to a list
with open("ques.json") as question_file:
    questions = json.load(question_file)
question_list = list(questions.items())

# Create some housekeeping variables
score = 0
question_num = 0

# Run the application
if __name__ == "__main__":
    app.run(debug=True)