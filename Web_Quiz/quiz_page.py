# Quiz app using Flask
from flask import Flask, render_template, request, redirect, url_for, session
import random
import json
import time

app = Flask(__name__)

app.secret_key = 'your_secret_key'

#Users for this program
USERS = {"port": "port123",
        "kazman": "kazman123"}

leaderboard = []

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
        
        #AI helped me apply session to reset quiz when new users login
        if USERS.get(userid) == userpass:
            session['username'] = userid
            session['score'] = 0
            session['question_num'] = 0
            session['start_time'] = time.time()
            session['answers'] = []
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
    # If the user is not logged in, redirect to the login page
    if 'username' not in session:
        return redirect(url_for('login'))

    #AI helped me apply session reset for when restarting on results
    if request.args.get('restart') == 'true':
        session['score'] = 0  
        session['question_num'] = 0
        session['answers'] = []
        return redirect(url_for('quiz'))
    
    #Setting score to 0
    if 'score' not in session:
        session['score'] = 0
    if 'question_num' not in session:
        session['question_num'] = 0

    #Grabbing current question number from session
    question_num = session['question_num']

    #Checks if questions are left if not sent to results
    if question_num >= len(question_list):
        return redirect(url_for('result'))

    # Get the current question and its answer choices
    current_question, alternatives = question_list[question_num]
    correct_answer = alternatives[0] 
    random.shuffle(alternatives)

    #When the user selects an answer, we check if it's correct
    if request.method == 'POST' and 'answer' in request.form:
        selected_answer = request.form.get('answer')

        # If answer is correct, increase score
        if selected_answer.strip() == correct_answer.strip():
            session['score'] += 1  

        session['question_num'] = question_num + 1

        # Return to the same quiz page with updated score
        return redirect(url_for('quiz'))  

    #Renders quiz page with current question and answer choices
    return render_template('quiz.html', 
                           question=current_question, 
                           options=alternatives, 
                           score=session['score'],
                           question_num=session['question_num'])

        
@app.route('/result', methods=['GET', 'POST'])
def result():
    global leaderboard

    if 'username' not in session:
        return redirect(url_for('login'))
    
    #Find the session
    score = session.get('score', 0)
    total_questions = len(question_list)

    #AI helped apply calclation time taken to finish the quiz
    start_time = session.get('start_time', None)
    time_taken = "N/A"
    
    if start_time:
        end_time = time.time()
        time_taken = round(end_time - start_time, 2) #allows to count in secons
    else:
        time_taken = "Time tracking error"
        
    #If the user submits their name, save it to the leaderboard
    if request.method == 'POST':
        username = request.form['username']
        leaderboard.append((username, score))

        #AI helped develop into applying leaderboard for top 10
        leaderboard.sort(key=lambda x: x[1], reverse=True)
        leaderboard = leaderboard[:10]

        #Applying session to reset for next
        session.pop('score', None)
        session.pop('question_num', None)
        session.pop('start_time', None)
        session.pop('answers', None)

        return redirect(url_for('leaderboard_route'))  

        #AI helped recover user's rank and calculate the leaderboard
    username = session.get('username', 'Anonymous')
    rank = "Not Ranked"
    for i, (name, s) in enumerate(leaderboard):
        if name == username and s == score:
            rank = i + 1  
            break

    return render_template('result.html', 
                           score=score, 
                           total_questions=total_questions, 
                           time_taken=time_taken, 
                           username=username, 
                           rank=rank)

# Leaderboard Route
@app.route('/leaderboard')
def leaderboard_route():
    return render_template('leaderboard.html')

# Load the question file and convert it to a list
with open("ques.json") as question_file:
    questions = json.load(question_file)

question_list = list(questions.items())

# Run the application
if __name__ == "__main__":
    app.run(debug=True)