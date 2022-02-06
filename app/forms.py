from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User, Exercise

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired()])
    password2 = PasswordField("Please repeat the password", validators = [DataRequired(), EqualTo("password")])
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
    entered_solution = StringField("solution", validators = [DataRequired()])
    submit = SubmitField("Submit")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True
        correct_solution = Exercise.query.filter_by(id=self.exercise_id.data).first()
        print(correct_solution.answer)
        print(self.entered_solution.data)
        if self.entered_solution.data != correct_solution.answer:
            self.entered_solution.errors.append('Wrong answer! Correct -> {}'.format(
                correct_solution.answer))
            result = False
        return result


