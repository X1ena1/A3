# Quiz app using Flask
from flask import Flask, render_template, request, redirect, url_for, session
import random
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/success/<username>')
def success(username):
    return render_template('success.html', username=username)

USERS = {"port": "port123",
        "kazman": "kazman123"}

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    global question_num, score

    #Check if not previously started and is continue
    if question_num >= len(questions):
        return redirect(url_for('result'))

        #Grabbing the current question
    current_question = questions[question_num]

    if request.method == 'POST':
        # Get the user's selected answer(s)
        selected_answer = request.form.get('options')

        if selected_answer == current_question['answer']:
            score += 1

        # Move to the next question
        question_num += 1

        # Redirect to the next question
        return redirect(url_for('quiz'))

    # Render the quiz question and options
    return render_template('quiz.html', num=question_num + 1,  # Show 1-based index
                           question=current_question['question'], 
                           options=current_question['options'], 
                           score=score)

#grabbing result and score
@app.route('/result')
def result():
    global score, question_num

    return render_template('result.html', score=score, num_questions=len(questions))

# Load the question file questions
with open("ques.json") as question_file:
    questions = json.load(question_file)

# Create some housekeeping variables
score = 0
question_num = 0

# Run the application
if __name__ == "__main__":
    app.run(debug=True)