from wtforms import Form, TextField, PasswordField


class Login(Form):
    email = TextField("Email") #, validators=[DataRequired()]
    password = PasswordField("Password") # , validators=[DataRequired()]