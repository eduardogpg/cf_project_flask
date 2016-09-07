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

import json     
import forms

from models import User
from models import Comment
from models import db as database

app = Flask(__name__)
#app.secret_key = 'my_secret_key'
#csrf = CsrfProtect(app)

def generate_session(username, user_id):
	session['user_id'] = user_id
	session['username'] = username

@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.before_request
def before_request():
	pass

@app.after_request
def after_request(response):
	return response

@app.route('/')
def index():
	username = session.get('username', '')
	return render_template('index.html', username = username)

@app.route('/login', methods = ['GET', 'POST'])
def login():
	login_form = forms.LoginForm(request.form)
	if request.method == 'POST' and login_form.validate():
		username = login_form.username.data
		password = login_form.password.data
		final_message = 'Bienvenido a la plataforma {}'.format(username)

		user = User.query.filter_by(username = username).first()
		if user is not None and user.verify_password(password):
			generate_session(user.username, user.id)
			flash('Bienvenido a la plataforma {}'.format(username))	
			return redirect(url_for('index'))
		else:
			flash('usuario o password no validos!')
	else:
		error_message='Error al validar el formulario!'
	return render_template('login.html', form = login_form)

@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/create', methods = ['GET', 'POST'])
def create():
	create_form = forms.CreateForm(request.form)
	if request.method == 'POST' and create_form.validate():

		username = create_form.username.data
		user = User(
								username = username,
								password = create_form.password.data,
								email = create_form.email.data)

		database.session.add(user)
		database.session.commit()
		generate_session(user.username, user.id)
		session['username'] = username
		
		success_message = 'Bienvenido a la plataforma {}'.format(username)
		flash(success_message)
		return redirect(url_for('index'))
	return render_template('create.html', form = create_form)

@app.route('/comment', methods = ['GET', 'POST'])
def comment():
	comment_form = forms.CommentForm(request.form)
	if request.method == 'POST' and comment_form.validate():
		user_id = session['user_id']
		comment = Comment( user_id = user_id, text = comment_form.comment.data )
		database.session.add(comment)
		database.session.commit()
		flash("Muchas gracias por tu comentario!.")

	return render_template('comment.html',form = comment_form)

@app.route('/reviews/', methods=['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def review(page=1):
	per_page = 10
	comment_list = Comment.query.join(User).add_columns(
												User.username, User.email,
												Comment.created_date, Comment.text).paginate(page, per_page, False)

	return render_template('review.html', comments = comment_list )	

""" Funciones por questiones de tutoriales """
@app.route('/setcookie')
def cookie():
	response = make_response(render_template('cookie.html'))
	response.set_cookie('custom_cookie', 'val1')
	return response

@app.route('/getcookie')
def getcookie():
	custome = request.cookies.get('custom_cookie', '')
	return render_template('cookie.html')

@app.route('/ajax-login', methods = ['POST'])
def ajax_login():
	print request.form
	user =  request.form['username'];
	response = { 'status': 200, 'user': user, 'id': 1 }
	return json.dumps(response)

if __name__ == '__main__':
	app.run(debug=True, port=8000)

