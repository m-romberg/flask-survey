from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


responses = []

@app.get('/')

def start_page ():
    """Loads Survey Opening"""

    title = survey.title
    instructions = survey.instructions
    print ("title ", title , "inst", instructions)
    return render_template(
        "survey_start.html", title = title, instructions = instructions)

@app.post("/begin")

def begin_survey ():
    """Directs user to question 0 on start click"""
    return redirect ("/questions/0")

@app.get("/questions/<int:question_num>")

def test (question_num):
    question = survey.questions[question_num]
    prompt = question.prompt
    choices = question.choices
    return render_template ("question.html", prompt = prompt, choices = choices)

