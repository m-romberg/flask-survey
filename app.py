from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.get('/')
def start_page ():
    """Loads Survey Opening"""
    title = survey.title
    instructions = survey.instructions
    print ("title ", title , "inst", instructions)
    return render_template(
        "survey_start.html", survey = survey)

@app.post("/begin")
def begin_survey ():
    """Directs user to question 0 on start click"""
    session['responses'] = []
    return redirect ("/questions/0")

@app.get("/questions/<int:question_num>")
def show_question (question_num):
    """Loads a survey question"""
    question = survey.questions[question_num]

    responses = session['responses']
    if question_num > len(responses):
        return redirect (f"/questions/{len(responses)}")
    
    if len(survey.questions) == len(responses):
        return redirect('/thank-you')

    return render_template (
        "question.html",
        question = question,
        question_num = question_num)


@app.post('/answer')
def handle_question_submission ():
    """Appends submission data to responses and redirects to next questioin"""
    responses = session['responses']
    responses.append(request.form["answer"])
    session['responses'] = responses

    question_num = int(request.form["question_num"]) + 1
    print(responses)

    if question_num >= len(survey.questions):
        return redirect ("/thank-you")

    return redirect (f"/questions/{question_num}")


@app.get('/thank-you')
def show_thank_you ():
    """Shows a thank you page with list of answers"""
    responses = session['responses']

    return render_template (
        "completion.html",
        questions_length = len(survey.questions),
        questions = survey.questions,
        responses = responses
    )
