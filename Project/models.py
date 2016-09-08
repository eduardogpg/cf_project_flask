#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://flask-sqlalchemy.pocoo.org/2.1/
#pip install Flask-SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime

"""
To use SQLAlchemy in a declarative way with your application,
you just have to put the following code into your application module.
Flask will automatically remove database sessions at the end of the request
or when the application shuts down:
"""


"""
Changes to the database are managed through a database session,
which Flask- SQLAlchemy provides as db.session.
To prepare objects to be written to the database,
they must be added to the session:
Página 79
"""
db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(50))
	password = db.Column(db.String(66))
	comments = db.relationship('Comment', backref='users', lazy='dynamic')
	created_date = db.Column(db.DateTime, default=datetime.datetime.now)

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = self.__create_pasword(password)

	def __create_pasword(self, password):
		return generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password, password)

class Comment(db.Model):
	__tablename__ = 'comments'

	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	text = db.Column(db.String(250))
	created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	
if __name__ == '__main__':
	db.create_all()

