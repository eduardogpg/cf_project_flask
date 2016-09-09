import os

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_custome_secret_key'
	MAIL_SERVER = "smtp.gmail.com"
	MAIL_PORT = 587
	MAIL_USE_SSL = False
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_CF')
	MAIL_PASSWORD = os.environ.get('PASSWORD_EMAIL_CF')

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/curso_flask'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	