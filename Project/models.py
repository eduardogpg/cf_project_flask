#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://flask-sqlalchemy.pocoo.org/2.1/
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#pip install Flask-SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/curso_flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120))
	password = db.Column(db.String(120))

	class Meta:
		table_name = 'users'

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password
 