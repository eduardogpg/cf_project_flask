#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import session
from flask import flash
from flask import redirect
from flask import url_for
from flask import abort
from flask import g
from flask_wtf.csrf import CsrfProtect

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import json     

import forms
import models

app = Flask(__name__)
#app.secret_key = 'my_secret_key'
#csrf = CsrfProtect(app)

@app.after_request
def after_request(response):
	return response

@app.before_request
def before_request():
	if 'username' not in session and request.endpoint not in ['login', 'create','abort']:
		return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.route('/')
def index():
	username = session.get('username', '')
	return render_template('index.html', username = username)

@app.route('/setcookie')
def cookie():
	response = make_response(render_template('cookie.html'))
	response.set_cookie('custom_cookie', 'Eduardo')
	return response

@app.route('/getcookie')
def getcookie():
	custome = request.cookies.get('custom_cookie', '')
	return render_template('cookie.html')

@app.route('/comment', methods = ['GET', 'POST'])
def comment():
	comment_form = forms.CommentForm(request.form)
	if request.method == 'POST' and comment_form.validate():
		print comment_form.honeypot.data
	return render_template('comment.html',form = comment_form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	login_form = forms.LoginForm(request.form)
	if request.method == 'POST' and login_form.validate():
		username = login_form.username.data
		password = login_form.password.data
		user = models.User.query.filter_by(username = username).first()

		final_message = 'Bienvenido a la plataforma {}'.format(username)
		if user is not None and check_password_hash(user.password, password):
			session['username'] = username
			flash('Bienvenido a la plataforma {}'.format(username))	
			return redirect(url_for('index'))
		else:
			flash('usuario o password no validos!')
	else:
		error_message='Error al validar el formulario!'
	return render_template('login.html', form = login_form)

@app.route('/create', methods = ['GET', 'POST'])
def create():
	create_form = forms.CreateForm(request.form)
	if request.method == 'POST' and create_form.validate():
		username = create_form.username.data
		user = models.User(
				username = username,
				password = generate_password_hash(create_form.password.data),
				email = create_form.email.data)

		models.db.session.add(user)
		models.db.session.commit()
		session['username'] = username
		
		success_message = 'Bienvenido a la plataforma {}'.format(username)
		flash(success_message)
		return redirect(url_for('index'))
	return render_template('create.html', form = create_form)

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))

if __name__ == '__main__':
	app.run(debug=True, port=8000)
	#models.db.create_all()
	#models.db.session.commit()


