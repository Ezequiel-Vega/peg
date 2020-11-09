from . import team_leader_bp as app

# Librerias de Python
import os
import uuid
from functools import wraps
from datetime import datetime
from werkzeug.utils import secure_filename
from typing import Any

# Librerias de Flask
from flask import redirect
from flask import render_template
from flask import url_for
from flask import session
from flask import flash
from flask import request
from flask import current_app

# Modelos de la base de datos
from app.models import Users
from app.models import Evaluations
from app.models import DataEvaluations
from app.models import ResultsEvaluation
from app.models import ManageEvaluations
from app.models import Tasks

# Formularios
from .forms import Evaluation
from .forms import Headline
from .forms import Third
from .forms import AnsweringMachine
from .forms import Results

# Librerias propias
from app.team_leader.calculator import Calculator

# Decoradores
def check_session(function):
   @wraps(function)
   def wrapper(*args, **kwargs):
      if 'user'in session:
         return function(*args, **kwargs)
      else:
         return redirect(url_for('auth.sign_in'))
   
   return wrapper

def get_corrections(form: Any) -> list:
    corrections = list()

    for  i in form:
        if i.name != 'csrf_token' and i.name != 'not_successful' and i.data == False:
            corrections.append(i.label.text)

    return corrections

#############################
#           API             #
#############################

@app.route('/api/v1/team_leader/data', methods=['POST'])
@check_session
def set_data():
    form = Evaluation()

    audio = request.files['audio']
    if audio == None:
        flash('Upss! No se selecciono un audio!')
        return redirect(url_for('team_leader.evaluation'))

    file_audio = secure_filename(audio.filename) 

    # Subir audio
    dir_upload = current_app.config['UPLOAD_FOLDER']
    audio.save(os.path.join(dir_upload, file_audio))

     # Obtener datos del nombre del audio
    data_audio = str(file_audio).split('-')[2].split('.')

    date_audio = '{}-{}-{}'.format(data_audio[0][:4], data_audio[0][4:6], data_audio[0][6:8])

    name_audio = file_audio

    phone = str(file_audio).split('-')[0]

    # Configurar valiarbes a guardar
    id_manager = form.id_manager.data

    date_evaluation = str(datetime.now().strftime('%Y-%m-%d'))

    default = form.default.data 

    contact = form.contact.data

    # Creo objeto a guardar
    user: Users = Users.by_id(session['user']['_id'])

    data = {
        'number_internal': id_manager,
        'team_leader': user.username,
        'phone': phone,
        'default': default,
        'contact': contact,
        'date_evaluation': date_evaluation,
        'date_audio': date_audio,
        'name_audio': name_audio,
        'audio': {
            'name': file_audio,
            'audio': True
        }
    }

    session['data_evaluation'] = data

    return redirect(url_for('team_leader.evaluation'))

@app.route('/api/v1/team_leader/results', methods=['POST'])
@check_session
def set_results():
    contact = session['data_evaluation']['contact']

    # Intanciar clase de calculador
    calculator: Calculator = Calculator()

    # Obtener que calculo se va hacer
    get_calculator = calculator.get_evaluation(contact)

    # Comprobar el tipo de contacto
    if contact == 'headline':
        form = Headline()

        # Obtener los items que no se cumplen
        corrections = get_corrections(form)

        # Obtener el resultado de los datos
        calc = get_calculator(form)
        result = calc.action()

    elif contact == 'third':
        form = Third()

        # Obtener los items que no se cumplen
        corrections = get_corrections(form)

        # Obtener el resultado de los dato 
        calc = get_calculator(form)
        result = calc.action()

    elif contact == 'answering_machine':
        form = AnsweringMachine()

        # Obtener los items que no se cumplen
        corrections = get_corrections(form)

        # Obtener el resultado de los datos
        calc = get_calculator(form)
        result = calc.action() 

    session['result_evaluation'] = result
    session['corrections'] = corrections

    return redirect(url_for('team_leader.result_evaluation'))

@app.route('/api/v1/team_leader/save/management', methods=['POST'])
@check_session
def save_management():
    form = Results()
    id_user = session['user']['_id']
    data_user = session['data_evaluation']
    result_user = session['result_evaluation']
    corrections = session['corrections']
    observation = form.observation.data
    default = data_user['default']

    # Buscar usuario
    user: Users = Users.by_id(id_user)

    # Mora
    if default == 'early':
        default == 'Temprana'
    elif default == 'last':
        default == 'Tardia'

    # Contacto
    if data_user['contact'] == 'headline':
        data_user['contact'] == 'Titular'
    elif data_user['contact'] == 'third':
        data_user['contact'] == 'Terceros'
    elif data_user['contact'] == 'answering_machine':
        data_user['contact'] == 'Contestador'
        default == None

    # Crear modelo de datos de la evaluacion a guardar
    data_evaluation: DataEvaluations = DataEvaluations(
                                                data_user['number_internal'],
                                                data_user['phone'],
                                                data_user['contact'],
                                                data_user['date_evaluation'],
                                                data_user['date_audio'], 
                                                data_user['name_audio'],
                                                default
                                            )
    # Guardar datos
    data_evaluation.save()

    # Crear modelo de resultados a guardar
    results_evaluation: ResultsEvaluation = ResultsEvaluation(
                                                    result_user['salute'],
                                                    result_user['attitude'],
                                                    result_user['negotiation_one'],
                                                    result_user['negotiation_two'],
                                                    result_user['registration_one'],
                                                    result_user['registration_two'],
                                                    result_user['result']
                                                )

    # Guardar resultado
    if 'message' in result_user:
        results_evaluation.save(message = result_user['message'])
    else:
        results_evaluation.save(closing = result_user['closing'])

    # Crear modelo de evaluaciones
    evaluation: Evaluations = Evaluations(
                                        observation, 
                                        corrections, 
                                        data_evaluation.id_data_evaluation, 
                                        results_evaluation.id_results_evaluation,
                                        user.id_users
                                    )

    # Guardar evaluaciones
    evaluation.save()

    # Actualizar gestion de evaluaciones 
    manage_evaluation: ManageEvaluations = ManageEvaluations.by_id(user.id_manage_evaluation)

    manage_evaluation.update()

    session.pop('data_evaluation')
    session.pop('result_evaluation')
    session.pop('corrections')

    return redirect(url_for('team_leader.results'))

@app.route('/api/v1/team_leader/task/<id>')
@check_session
def delete_task(id: uuid.UUID):
    Tasks.delete(id)
    return redirect(url_for('home'))

#############################
#          Render           #
#############################

@app.route('/home/team_leader')
@check_session
def home():
    print(session['user'])
    id_user = session['user']['_id']
    tasks = list()

    db_tasks = Tasks.by_team_leader(id_user)

    for task in db_tasks:
        data_task = {
                'managers': task.managers,
                'date': task.date_task,
                'id_tasks': task.id_tasks
                }
        tasks.append(data_task)

    return render_template("home_team_leader.html", tasks=tasks)


@app.route('/evaluation')
@check_session
def evaluation():
    if 'data_evaluation' in session:
        data = session['data_evaluation']
    else:
        data = {'audio':{}}
    return render_template('evaluation.html', form=Evaluation(), data=data)

@app.route('/results')
def results():
    evaluations_team_leader = list()
    id_user = session['user']['_id']
    
    # Buscar usuario
    user: Users = Users.by_id(id_user)

    # Buscar evaluaciones
    evaluations: Evaluations = Evaluations.by_id_user(id_user)

    for evaluation in evaluations:
        data_evaluation: DataEvaluations = DataEvaluations.by_id(evaluation.id_data_evaluation)
        result_evaluation: ResultsEvaluation = ResultsEvaluation.by_id(evaluation.id_results_evaluation)

        # Objeto a guardar
        data = {
            '_id': evaluation.id_evaluations,
            'data_evaluation': data_evaluation,
            'team_leader': user.username,
            'result_evaluation': result_evaluation,
            'audio': data_evaluation.name_audio
        }

        # Agregar objeto a la lista
        evaluations_team_leader.append(data)

    return render_template('results.html', datas = evaluations_team_leader)

@app.route('/see_more/<id>')
@check_session
def see_more(id: uuid.UUID):
    # Buscar la evaluacion correspondiente
    manage_evaluation: Evaluations = Evaluations.by_id(id)

    # Busca los datos de la evaluacion correspondiente
    data_evaluation: DataEvaluations = DataEvaluations.by_id(manage_evaluation.id_data_evaluation)

    # Buscar los resultados de la evaluacion
    result_evaluation: ResultsEvaluation = ResultsEvaluation.by_id(manage_evaluation.id_results_evaluation)

    data = {
        'data_evaluation': data_evaluation,
        'result_evaluation': result_evaluation,
        'observation': manage_evaluation.observations,
        'corrections': manage_evaluation.corrections
    }

    return render_template('see_more.html', data=data)

@app.route('/form_evaluation')
@check_session
def form_evaluation():
    data = {
       'name_audio': session['data_evaluation']['name_audio'],
       'contact': session['data_evaluation']['contact'],
       'audio': {
           'name': session['data_evaluation']['audio']['name'],
           'audio': True
       }
    }

    if data['contact'] == 'headline':
        return render_template('evaluation/headline.html', form=Headline(), data=data)
    elif data['contact'] == 'third':
        return render_template('evaluation/third.html', form=Third(), data=data)
    elif data['contact'] == 'answering_machine':
        return render_template('evaluation/answering_machine.html', form=AnsweringMachine(), data=data)

@app.route('/result_evaluation')
@check_session
def result_evaluation():
    results = session['result_evaluation']

    corrections = session['corrections']
    data = {
        'contact': session['data_evaluation']['contact'],
        'audio': session['data_evaluation']['audio']['name']    }

    return render_template('result_evaluation.html', results=results, data=data, corrections=corrections, form=Results())
