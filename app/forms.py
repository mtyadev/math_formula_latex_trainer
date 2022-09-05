from flask_wtf import FlaskForm
from flask import flash
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, SelectField, RadioField
from wtforms.validators import DataRequired, ValidationError, InputRequired, Email, EqualTo
from app.models import User, Exercise
import difflib as dl

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Please repeat the password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please enter different email address.")

class MathQuizForm(FlaskForm):
    exercise_id = HiddenField("exercise_id")
    quiz_solution_image_previous = HiddenField("quiz_solution_image_previous")
    correct_answer_previous = HiddenField("correct_answer_previous")
    entered_answer_previous = HiddenField("entered_answer_previous")
    entered_solution = StringField("solution", validators=[DataRequired()])
    repetition_required = BooleanField("repetition_required")
    submit = SubmitField("Submit")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        correct_solution = Exercise.query.filter_by(id=self.exercise_id.data).first()
        solution_short = correct_solution.answer.split("\\\\")[-1].strip()
        solution_entered_short = self.entered_solution.data.split("\\\\")[-1].strip()
        if solution_entered_short != solution_short:
            flash(correct_solution.answer)
            self.entered_solution.errors.append("Nope ... !")
            result = False
        return result

class LessonSelection(FlaskForm):
    lesson = SelectField("Lesson", coerce=int, validators=[InputRequired()])
    submit = SubmitField("Submit")

class Editor(FlaskForm):
    question = StringField("question", validators=[DataRequired()])
    answer = StringField("answer", validators=[DataRequired()])
    submit = SubmitField("Update Exercise")



