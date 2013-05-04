from flask.ext.wtf import Form, TextField, PasswordField, HiddenField, Required
from wtforms import validators


class Login(Form):
    email = TextField("Email", validators=[Required()])
    password = PasswordField("Password", validators=[Required()])