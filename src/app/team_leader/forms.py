from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SelectField
from wtforms import FileField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
from wtforms.validators import Length

class Evaluation(FlaskForm):
    id_manager = StringField('Id del Gestor', validators=[
        DataRequired(),
        Length(max=4)
    ])

    default = SelectField('Seleccionar Mora', choices=[
        ('early', 'Temprana'), ('late', 'Tardia')
    ])

    contact = SelectField('Seleccionar Contacto', choices=[
        ('headline', 'Titular'), 
        ('third', 'Tercero'),
        ('answering_machine', 'Contestador')
    ])

    add_audio = FileField('Seleccionar Audio')

    btn_submit = SubmitField('Actualizar Datos')

class Headline(FlaskForm):
    # Saludo
    identity_holder = BooleanField('Identificar al titular')
    presentation = BooleanField('Presentacion')
    presentation_company = BooleanField('Presentar a la empresa')
    debt_presentation = BooleanField('Presentar la deuda')
    meets_criteria = BooleanField('Cumplir Criterios')

    # Actitudo
    voice_tone = BooleanField('Tono de voz')
    empathy = BooleanField('Empatia')
    words_repeat = BooleanField('Muletillas')
    treat_you = BooleanField('Tratar de usted')
    secure_presentation = BooleanField('Presentacion segura')
    
    # Negociacion 1
    start_negotiation = BooleanField('Comenzazr negociacion')
    active_listening = BooleanField('Escucha activa')
    preparation = BooleanField('Preparacion')

    # Negociacion 2
    negotiation_two = BooleanField('Cumple los punto de la negociacion 2')

    # Registro 1
    collector_registration = BooleanField('Registro en el collector')
    managementes_result = BooleanField('Gestion y Resultados')
    new_debtor_data = BooleanField('Nuevos datos')
    generate_promise = BooleanField('Generar promesa')
    load_promise_managment = BooleanField('Cargar promesa y gestion')

    # Registro 2
    add_contact = BooleanField('Agregar contacto')
    writing_field = BooleanField('Campo de escritura')
    abbreviations = BooleanField('Abreviaturas')

    # Cierre
    successful = BooleanField('Exitoso')
    not_successful = BooleanField('No Exitoso')
    remember_date = BooleanField('Recordar fecha')
    provide_data = BooleanField('Brindar datos')

    btn_submit = SubmitField('Mostrar Resultados')

class Third(FlaskForm):
    # Saludo
    identify_holder = BooleanField("Tono de voz")
    relationship = BooleanField("Confirma relacion con 3ro")
    presentation = BooleanField("Presentacion")
    presentation_company = BooleanField("Presenta la empresa/entidad")
    contact_theadline = BooleanField("Soliciar contacto del titular")

    # Actitud
    voice_tone = BooleanField("Tono de voz")
    empathy = BooleanField("Empatia")
    words_repeat = BooleanField("Muletillas")
    treat_you = BooleanField("Tratar de usted")
    secure_presentation = BooleanField("Presentacion segura")

    # Negociacion 1
    start_negotiation = BooleanField("Comenzar negociacion")
    active_listening = BooleanField("Escucha activa")
    preparation = BooleanField("Preparacion")

    # Negociacion 2
    negotiation_two = BooleanField("Cumple los punto de la negociacion 2")

    # Registro 1
    collector_registration = BooleanField("Registro en el collector")
    managementes_result = BooleanField("Gestion y Resultado")
    new_debtor_data = BooleanField("Nuevos datos")

    # Registro 2
    add_contact = BooleanField("Agregar contacto")
    writing_field = BooleanField("Campo de escritura")
    abbreviations = BooleanField("Abreviaturas")

    # Cierre
    term = BooleanField("Recordar el plazo")
    negative_consequences = BooleanField("Consecuencias negativas")
    provide_data = BooleanField("Brindar datos")

    btn_submit = SubmitField("Mostrar Resultados")

class AnsweringMachine(FlaskForm):
    # Saludo
    info_holder = BooleanField("Informar al titular")
    presentation = BooleanField("Presentacion")
    presentation_company = BooleanField("Presentacion de la empresa/Entidad")
    reason_call = BooleanField("Motivo del llamado")

    # Actitud
    voice_tone = BooleanField("Tono de voz")
    words_repeat = BooleanField("Muletilla")
    secure_presentation = BooleanField("Presentacion segura")

    # Mensaje
    message = BooleanField("Cumple el criterio del mensaje")

    # Registro 1
    collector_registration = BooleanField("Registro en el Collector")
    managementes_result = BooleanField("Gestion y Resultado")

    # Registro 2
    open_call_yes = BooleanField("Si")
    open_call_no = BooleanField("No")
    add_contact = BooleanField("Agregar contacto")
    writing_field = BooleanField("Campo de escritura")
    abbreviations = BooleanField("Abreviaturas")

    btn_submit = SubmitField("Mostrar Resultados")

class Results(FlaskForm):
    observation = StringField('Observacion', widget=TextArea(), validators=[DataRequired()])
    btn_submit = SubmitField("Guardar Resultados")
