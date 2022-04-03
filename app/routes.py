import random
from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, MathQuizForm, LessonSelection, Editor
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Lesson, Exercise, UserLessonExerciseProgress
from werkzeug.urls import url_parse
from flask import request

def choose_random_exercise_id(lesson_id):
    exercise_ids_in_lesson = [x.exercise_id for x in UserLessonExerciseProgress.query.filter_by(
        lesson_id=lesson_id, user_id=current_user.id) if x.times_shown <= 1]
    return random.choice(exercise_ids_in_lesson)

def persist_user_lesson_exercise_progress(lesson_id):
    # Only persist, if hasn't been persisted before.
    if not UserLessonExerciseProgress.query.filter_by(lesson_id=lesson_id, user_id=current_user.id).all():
        for exercise in Exercise.query.filter_by(lesson=lesson_id).all():
            db.session.add(UserLessonExerciseProgress(current_user.id, lesson_id, exercise.id, 0, 0))
        db.session.commit()

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

@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    form = LessonSelection()
    form.lesson.choices = [(lesson.id, lesson.title) for lesson in Lesson.query.all()]
    if form.validate_on_submit():
        persist_user_lesson_exercise_progress(form.lesson.data)
        return redirect(url_for('quiz', lesson_id=form.lesson.data,
                                exercise_id=choose_random_exercise_id(form.lesson.data)))
    return render_template("index.html", title="Home", form=form)

@app.route("/quiz", methods=["GET", "POST"])
@login_required
def quiz():
    lesson_id = request.args.get("lesson_id")
    exercise_id = request.args.get("exercise_id")
    quiz_solution_image_last = request.args.get("quiz_solution_image_last")
    exercise_current = Exercise.query.filter_by(lesson=lesson_id, id=exercise_id).first()
    quiz_question_image_current = f"{exercise_current.title}_question_image.png"
    quiz_solution_image_current = f"{exercise_current.title}_solution_image.png"
    update_exercise_stats = UserLessonExerciseProgress.query.filter_by(
        lesson_id=lesson_id, exercise_id=exercise_id, user_id=current_user.id).first()
    monitor_stats = UserLessonExerciseProgress.query.filter_by(
        lesson_id=lesson_id, user_id=current_user.id).all()
    form = MathQuizForm(exercise_id=exercise_id)
    if form.validate_on_submit():
        flash('Correct!')
        update_exercise_stats.times_shown += 1
        db.session.commit()
        next_exercise_id = choose_random_exercise_id(lesson_id)
        return redirect(url_for('quiz',
                                exercise_id=next_exercise_id,
                                lesson_id=lesson_id,
                                monitor_stats=monitor_stats,
                                question=exercise_current.question,
                                quiz_question_image_current=quiz_question_image_current,
                                quiz_solution_image_current=quiz_solution_image_current,
                                quiz_solution_image_last=quiz_solution_image_last))
    return render_template("quiz.html", title="Quiz", form=form, monitor_stats=monitor_stats,
                           question=exercise_current.question, lesson_id=lesson_id, exercise_id=exercise_id,
                           quiz_question_image_current=quiz_question_image_current)

@app.route("/editor", methods=["GET", "POST"])
@login_required
def editor():
    lesson_id = request.args.get("lesson_id")
    exercise_id = request.args.get("exercise_id")
    exercise = Exercise.query.filter_by(lesson=lesson_id, id=exercise_id).first()
    form = Editor(question=exercise.question, answer=exercise.answer)
    if form.validate_on_submit():
        exercise.question = form.question.data
        exercise.answer = form.answer.data
        db.session.commit()
        flash('Updated Exercise!')
    return render_template("editor.html", title="editor", form=form, exercise_id=exercise_id)
