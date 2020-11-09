from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class SignIn(FlaskForm):
    username = StringField("Username", validators=[
        DataRequired(),
        Length(max=4)
    ])

    password = PasswordField("Password", validators=[
        DataRequired(), 
        Length(max=20)
    ])

    btn_submit = SubmitField("Iniciar Sesion")
