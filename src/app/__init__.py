from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

sqlAlchemy: SQLAlchemy = SQLAlchemy()
bcrypt: Bcrypt = Bcrypt()
migrate: Migrate = Migrate()

def created_app(settings_module: str) -> Flask:
    """
        Creacion del servidor 
        :param settings_module: Configuracion del servidor
    """

    # Intanciar servidor flask
    app = Flask(__name__, instance_relative_config = True)

    # Cargar configuracion
    app.config.from_object(settings_module)

    # Iniciar la base de datos
    sqlAlchemy.init_app(app)

    # Iniciar la migracion de la aplicacion
    migrate.init_app(app, sqlAlchemy)

    # Middlewares
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registrar rutas
    from .admin import admin_bp
    from .auth import auth_bp
    from .team_leader import team_leader_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(team_leader_bp)

    # Retornar Servidor
    return app

