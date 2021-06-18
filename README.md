# math_formula_latex_trainer

* Mini Python Flask App to generate math quizzes and memorize math formulas using LaTeX.
* Current Status is WIP, not functional
* For setup of basic flask framework using best practices as outlined in https://blog.miguelgrinberg.com/

# Setup

## Generate venv

In the main folder, generate a venv using:

$ python -m venv venv

## Access venv

### Mac/Linux

$ source venv/bin/activate

### Windows

$ venv\Scripts\activate

## Inside venv install required libraries

$ pip install flask python-dotenv flask-wtf flask-sqlalchemy flask-migrate flask-login email-validator

## Start app in dev mode

From inside venv type

$ flask run
