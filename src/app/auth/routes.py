from . import auth_bp as app

# Librerias de Python
from functools import wraps

# Librerias de Flask
from flask import request
from flask import session
from flask import flash
from flask import url_for
from flask import redirect
from flask import render_template

# Modelos de la base de datos
from app.models import Users
from app.models import Category

# Formularios
from .forms import SignIn


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
               return redirect(url_for('admin.home'))
            elif name_category== 'team_leader':
               return redirect(url_for('team_leader.home'))
            else:
               return function(*args, **kwargs)
        else:
            return function(*args, **kwargs)

    return wrapper

#############################
#           API             #
#############################


@app.route('/api/v1/auth/signin', methods=['POST'])
@check_session
def sign_in_action():
    # Instanciar la clase
    form = SignIn()

    # Obtener los datos ingresados
    username = form.username.data
    password = form.password.data

    # Buscar el usuario
    user: Users = Users.by_username(username)

    # Si existe el usuario
    if user != None:
        # Validar contraseña
        match = user.validate_password(password)

        # Buscar categoria
        category: Category = Category.by_id(user.id_category) 

        # Si es valida
        if match:
            # Creo diccionario a guardar
            user = {
                'category': category.id_category,
                '_id': user.id_users
            }
         
            # Guardar usuario em la session
            session['user'] = user

            # Redireccionar usuario
            if category.category == 'team_leader':
                return redirect(url_for('team_leader.home'))
            elif category.category == 'admin':
                return redirect(url_for('admin.home'))
            elif category.category == 'manager':
                return redirect(url_for('manager.home'))
        else:
            flash("Upss! Password Incorrecta!")
            return redirect(url_for('auth.sign_in'))
    else:
        flash("Upss! Username Incorrecto!")
        return redirect(url_for("auth.sign_in"))

@app.route('/auth/closed')
def closed_session():
    session.pop('user')
    return redirect(url_for('auth.sign_in'))

#############################
#          Render           #
#############################

@app.route('/')
@app.route('/sign_in')
@check_session
def sign_in():
    return render_template("sign_in.html", form=SignIn())
