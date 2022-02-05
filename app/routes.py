import random
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, MathQuizForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Lesson, Exercise
from werkzeug.urls import url_parse
from flask import request

def choose_random_exercise_id(lesson_id):
    exercise_ids_in_lesson = [exercise.id for exercise in Exercise.query.filter_by(lesson=lesson_id).all()]
    exercise_id = random.choice(exercise_ids_in_lesson)
    return exercise_id

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next.page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for signing up!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/")
@app.route("/index")
@login_required
def index():
    lesson_with_exercise_ids = []
    for lesson in Lesson.query.all():
        lesson_with_exercise_ids.append((lesson.title, lesson.id, choose_random_exercise_id(lesson.id)))
    return render_template("index.html", title="Home", lesson_with_exercise_ids=lesson_with_exercise_ids)

@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    lesson_id = request.args.get("lesson_id")
    exercise_id = request.args.get("exercise_id")
    form = MathQuizForm(exercise_id=exercise_id)
    if form.validate_on_submit():
        flash('Correct!')
        exercise_id = choose_random_exercise_id(lesson_id)
        return redirect(url_for('quiz', exercise_id=exercise_id, lesson_id=lesson_id))

    exercise = Exercise.query.filter_by(id=exercise_id).first()
    return render_template("quiz.html", title="Quiz", form=form, question=exercise.question)