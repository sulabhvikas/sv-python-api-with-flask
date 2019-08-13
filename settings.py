from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/vinivik/vinivik/personal/source-code/trainings/pluralsight/python-projects/flask-projects/sv-first-flask/books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False