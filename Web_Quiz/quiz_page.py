# Quiz app using Flask
from flask import Flask, render_template, request, redirect, url_for, session
import random
import json

app = Flask(__name__)
app.secret_key = 'secret_key'  # This is required for Flask to handle sessions

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form.get('username')
        userpass = request.form.get('password')
        # Check the username and password. If successful, take the user to the success page.
        
        if USERS.get(userid) == userpass:
            return redirect(url_for('success', username=userid))
        else:
            return("Sorry bud")
    else:    
        return render_template('login.html')

@app.route('/success/<username>')
def success(username):
    return render_template('success.html', username=username)

USERS = {"port": "port123",
        "kazman": "kazman123"}

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global question_num, score

    question_num = session['question_num']

    if request.method == 'POST':
        # Get the user's selected answer(s)
        selected_answer = request.form.get('options')
        current_question = questions[question_num]


    if selected_answer == current_question['answer']:
        session['score'] += 1
    else:
        score += 0

    #Move onto the next question
    session['question_num'] += 1

    if session[question_num] >= len(questions):
        return redirect(url_for('result'))
    
    return redirect(url_for('quiz'))

#grabbing result and score
@app.route('/result')
def result():
    global score
    score = session.get('score', 0)
    return render_template('result.html', score=score)

# Load the question file and convert it to a list
with open("ques.json") as question_file:
    questions = json.load(question_file)

# Create some housekeeping variables
score = 0
question_num = 0

# Run the application
if __name__ == "__main__":
    app.run(debug=True)