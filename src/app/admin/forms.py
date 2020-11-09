# Librerias de Python
from datetime import date

# Librerias de Flask Form
from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms import StringField
from wtforms import DateField
from wtforms import SubmitField
from wtforms import PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class SearchEvaluation(FlaskForm):
    input_select = StringField('Buscar evaluacion', validators=[
        DataRequired(),
        Length(max=4)
    ])

    btn_submit = SubmitField('Buscar')

class CreateTask(FlaskForm):
    team_leader = StringField('Agregar Team Leader', validators=[
        DataRequired(),
    ])

    manager = StringField('Agregar Gestores', validators=[
        DataRequired()
    ])
    
    date = DateField('DatePicker: ', validators=[DataRequired()], default=date.today)
    btn_submit = SubmitField('Agregar Tarea')

class AddUser(FlaskForm):
    number_internal = StringField('Number de Interno', validators=[
        DataRequired(),
        Length(max=4)
    ])

    password = PasswordField('Password', validators=[
            DataRequired()
    ])
    
    name = StringField('Nombre', validators=[
        DataRequired()
    ])
    
    last_name = StringField('Apellido', validators=[
        DataRequired()
    ]) 
 
    category = SelectField('Seleccionar categoria', choices=[
        ('admin', 'Administrador'),
        ('team_leader', 'Team Leader'),
        ('manager', 'Gestor')
    ])

    btn_submit = SubmitField('Agregar usuario')
