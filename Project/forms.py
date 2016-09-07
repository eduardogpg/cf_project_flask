from wtforms import Form
from wtforms import StringField
from wtforms import TextField
from wtforms import PasswordField
from wtforms import HiddenField
from wtforms import TextAreaField
from wtforms.fields.html5 import EmailField

from wtforms import validators
from models import User

def length_honeypot(form, field):
	if len(field.data) > 0:
		raise validators.ValidationError('Lo siento bot no vas a pasar')

class CommentForm(Form):
	comment = TextAreaField('Comentario', [validators.Length(min=5, max=255, 
    					message ='El comentario debe contener por lo menos 5 caracteres')],
    					render_kw={"placeholder": "Comentario"} )

	honeypot = HiddenField("",[length_honeypot])

class LoginForm(Form):
	username = TextField('Username', [validators.Required(message = 'El username es requerido')])
	password = PasswordField('Password', [validators.Required(message='El password es requerido')])

class CreateForm(Form):
	username = TextField('Username', 
						[
							validators.Required(message = 'El username es requerido'),
							validators.length(min=4, max=25, message='Ingrese un username valido') 
						])
	email = EmailField('Correo electronico',
						[	validators.Required(message = 'El email es requerido!.'),
							validators.Email(message='Ingre un email valido')
						])
	password = PasswordField('Password', [validators.Required(message='El password es requerido')])
	

	def validate_username(form, field):
	 	username = field.data
	 	user = User.query.filter_by(username = username).first()
	 	if user is not None:
	 		raise validators.ValidationError('El username ya se encuentra registrado!')


