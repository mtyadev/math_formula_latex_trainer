from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return 'Lesson %r' % self.title

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    lesson = db.Column(db.Integer, db.ForeignKey("lesson.id"))

    def __init__(self, question, answer, lesson):
        self.question = question
        self.answer = answer
        self.lesson = lesson

    def __repr__(self):
        return 'Exercise %r' % self.question

class UserLessonExerciseProgress(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercise.id"), primary_key=True)
    times_shown = db.Column(db.Integer, nullable=False)
    times_false = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, lesson_id, exercise_id, times_shown, times_false):
        self.user_id = user_id
        self.lesson_id = lesson_id
        self.exercise_id = exercise_id
        self.times_shown = times_shown
        self.times_false = times_false

    def __repr__(self):
        return f"User {self.user_id} Lesson {self.lesson_id} Exercise {self.exercise_id} Progress"
