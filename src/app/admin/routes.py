from . import admin_bp as app

# Librerias de Python
import uuid
from functools import wraps

# Libreria Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import session
from flask import flash
from flask import redirect

# Modelos de la base de datos
from app.models import Users
from app.models import Employees
from app.models import Category
from app.models import ManageEvaluations
from app.models import Evaluations
from app.models import DataEvaluations
from app.models import ResultsEvaluation
from app.models import Tasks

# Formularios
from .forms import SearchEvaluation
from .forms import AddUser
from .forms import CreateTask

# Decoradores
def check_session(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            # Buscar categoria
            category: Category = Category.by_id(session['user']['category'])

            # Comprobar categoria
            name_category = category.category

            if name_category == 'admin':
               return function(*args, **kwargs)
            elif name_category== 'team_leader':
               return redirect(url_for('team_leader.home'))
            else:
               return redirect(url_for('auth.sign_in'))
        else:
            return redirect(url_for('auth.sign_in'))

    return wrapper

#############################
#           API             #
#############################

@app.route('/api/v1/admin/evaluations', methods=['POST'])
@check_session
def search_evaluations():
    
    form = SearchEvaluation()

    # Obtengo los datos del form
    number_internal_user = int(form.input_select.data)
    
    user: Users = Users.by_username(number_internal_user)

    if user == None:
        flash('No existe un usuario con este Numero de interno', 'alert-danger')
        return redirect(url_for('admin.get_evaluations'))

    # Agrego las evaluaciones respecto al ID ingresado
    evaluations = list()

    db_evaluations: Evaluations = Evaluations.by_id_user(user.id_users)

    for evaluation in db_evaluations:
        data_evaluation: DataEvaluations = DataEvaluations.by_id(db_evaluations.id_data_evaluation)
        result_evaluation: ResultsEvaluation = ResultsEvaluation.by_id(db_evaluations.id_results_evaluation)

        # Objeto a guardar
        data = {
            'data_evaluation': data_evaluation,
            'result_evaluation': result_evaluation,
            '_id': evaluation.id_evaluations
        }

        # Agregar objeto a la lista
        evaluations.append(data)

    session['evaluations'] = evaluations

    return redirect(url_for('admin.get_evaluations'))

@app.route('/api/v1/admin/tasks', methods=['POST'])
@check_session
def add_tasks():
    form = CreateTask()

    # Obtener datos del formulario
    team_leader = int(form.team_leader.data)
    managers = str(form.manager.data).split(';')
    date = form.date.data

    # Crear modelo de las tareas a guardar
    id_team_leader = Users.by_username(team_leader)

    for manager in managers:
        manager = int(manager)
        task: Tasks = Tasks(manager, date, id_team_leader.id_users)
        # Guardar tarea
        task.save()

    flash('Se agrego la tarea', 'alert-success')   
    return redirect(url_for('admin.tasks'))

@app.route('/api/v1/admin/tasks/<id>', methods=['GET'])
@check_session
def delete_task(id: uuid.UUID):
    task: Tasks = Tasks.by_id(id)
    task.delete()
    flash('Se elimino la tarea', 'alert-success') 
    return redirect(url_for('admin.tasks'))

@app.route('/api/v1/admin/user', methods=['POST'])
#@check_session
def add_user():
    form = AddUser()

    # Obtener datos del formulario
    number_internal = int(form.number_internal.data)
    password = form.password.data
    name = form.name.data
    last_name = form.last_name.data
    category = form.category.data

    # Buscar usuario
    user: Users = Users.by_username(number_internal)

    if user == None:
        # Guardar datos del usuario
        employees: Employees = Employees(name, last_name)
        employees.save()

        # Buscar categoria
        category_db: Category = Category.by_category(category)

        if category_db.category == 'team_leader':
            # Crear Gestion de evaluaciones
            management_evaluation: ManageEvaluations = ManageEvaluations()
            management_evaluation.save()

            # Crear modelo de usuario
            new_user: Users = Users(
                    number_internal,
                    number_internal,
                    employees.id_employees,
                    category_db.id_category,
                    management_evaluation.id_manage_evaluation
                ) 
        # Crear modelo de usuario
        new_user: Users = Users(
            number_internal,
            number_internal,
            employees.id_employees,
            category_db.id_category,
            None
        )

        # Encriptar password
        new_user.encrypt_password(password)

        new_user.save()

        flash('Upss! El usuario ya existe!', 'alert-success')
        return redirect(url_for('admin.users'))
    else:
        flash('Upss! El usuario ya existe!', 'alert-danger')
        return redirect(url_for('admin.users'))

@app.route('/api/v1/admin/user/<id>', methods=['GET'])
def delete_user(id: uuid.UUID):
    # Buscar usuario para eliminar
    Users.delete(id)
    flash('Se elimino el usuario', 'alert-success') 
    return redirect(url_for('admin.users'))

#############################
#          Render           #
#############################

@app.route('/home')
@check_session
def home():
    return render_template('home_admin.html')

@app.route('/evaluations')
@check_session
def get_evaluations():
    form = SearchEvaluation()
    # Comprobar si ya se pidio algun resultado
    if 'evaluations' in session:
        evaluations = session['evaluations']
        return render_template('evaluation_admin.html', evaluations = evaluations, form = form)
    else:
        evaluations = list()        

        db_evaluations: Evaluations = Evaluations.by_all()

        for evaluation in db_evaluations:
            data_evaluation: DataEvaluations = DataEvaluations.by_id(db_evaluations.id_data_evaluation)
            result_evaluation: ResultsEvaluation = ResultsEvaluation.by_id(db_evaluations.id_results_evaluation)

            # Objeto a guardar
            data = {
                'data_evaluation': data_evaluation,
                'result_evaluation': result_evaluation,
                '_id': evaluation.id_evaluations
            }

            # Agregar objeto a la lista
            evaluations.append(data)

        return render_template('evaluation_admin.html', evaluations = evaluations, form = form)

@app.route('/evaluations/<id>')
@check_session
def more_info(id: uuid.UUID):
    # Buscar la evaluacion correspondiente
    evaluation: Evaluations = Evaluations.by_id(id)

    # Busca los datos de la evaluacion correspondiente
    data_evaluation: DataEvaluations = DataEvaluations.by_id(evaluation.id_data_evaluation)

    # Buscar los resultados de la evaluacion
    result_evaluation: ResultsEvaluation = ResultsEvaluation.by_id(evaluation.id_results_evaluation)

    data = {
        'data_evaluation': data_evaluation,
        'result_evaluation': result_evaluation,
        'observation': evaluation.observations,
        'corrections': evaluation.corrections
    }

    return render_template('see_more_admin.html', data = data)


@app.route('/tasks')
@check_session
def tasks():
    db_tasks: Tasks = Tasks.by_all()

    tasks = list()

    # Recolectar todas las tareas
    for task in db_tasks:
        format_task = {
                '_id': task.id_task,
                'team_leader': task.id_team_leader,
                'managers': task.managers,
                'date': task.date_task
                }
        tasks.append(format_task)

    return render_template('tasks_admin.html', tasks = tasks, form = CreateTask())

@app.route('/user')
@check_session
def users():
    return render_template('users_admin.html', form=AddUser())

@app.route('/users/admin')
def get_admin():
    db_users: Users = Users.by_all()

    users = list()

    for user in db_users:  
        category: Category = Category.by_id(user.id_category)

        if category.category == 'admin':
            # Buscar datos del team leader
            employees: Employees = Employees.by_id(user.id_employees)

            # Crear diccionario del usuario
            data_user = {
                        '_id': user.username,
                        'username': user.username,
                        'name': employees.name,
                        'last_name': employees.last_name
                    }
            users.append(data_user)

    return render_template('admins_admin.html', admins = users)

@app.route('/users/team_leader')
@check_session
def get_team_leader():
    db_users: Users = Users.by_all()

    users = list()

    for user in db_users: 
        category_user: Category = Category.by_id(user.id_category)

        if category_user.category == 'team_leader':
            # Buscar gestor de evaluaciones
            manage_evaluation: ManageEvaluations = ManageEvaluations.by_id(user.id_manage_evaluation)

            # Buscar datos del team leader
            employees: Employees = Employees.by_id(user.id_employees)

            # Crear diccionario del usuario
            data_user = {
                        '_id': user.id_users,
                        'username': user.username,
                        'name': employees.name,
                        'last_name': employees.last_name,
                        'date_last_evaluation': manage_evaluation.date_last_evaluation,
                        'quantity_evaluations': manage_evaluation.quantity
                    }
            users.append(data_user)

    return render_template('team_leaders_admin.html', team_leaders = users)

@app.route('/users/manage')
@check_session
def get_manage():
    db_users: Users = Users.by_all()

    users = list()

    for user in db_users: 
        category_user: Category = Category.by_id(user.id_category)

        if category_user.category == 'manager':
            # Buscar gestor de evaluaciones
            manage_evaluation: ManageEvaluations = ManageEvaluations.by_id(user.id_manage_evaluation)

            # Buscar datos del team leader
            employees: Employees = Employees.by_id(user.id_employees)

            # Crear diccionario del usuario
            data_user = {
                        '_id': user.id_users,
                        'username': user.username,
                        'name': employees.name,
                        'last_name': employees.last_name,
                        'date_last_evaluation': manage_evaluation.date_last_evaluation,
                        'quantity_evaluations': manage_evaluation.quantity
                    }
            users.append(data_user)

    return render_template('managers_admin.html', managers = users)
