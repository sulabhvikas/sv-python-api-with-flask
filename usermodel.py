from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from settings import app

db = SQLAlchemy(app)

class BookUser(db.Model):
	__tablename__ = 'bookusers'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)

	def validateLogin(_username, _password):
		user = BookUser.query.filter_by(username=_username).filter_by(password=_password).first()
		if user is None:
			return False
		else:
			return True

	def getAllUsers():
		return BookUser.query.all()

	def createUser(_username, _password):
		newUser = BookUser(username=_username, password=_password)
		db.session.add(newUser)
		try:
			db.session.commit()
		except:
			db.session.rollback()
		finally:
			db.session.close()

	def __repr__(self):
		user_object = {
			'username': self.username,
			'password': self.password
		}
		return json.dumps(user_object)

'''
db.create_all()
db.session.commit()
db.session.remove()
'''