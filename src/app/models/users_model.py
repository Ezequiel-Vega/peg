import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app import sqlAlchemy as db
from app import bcrypt
from app.models import ManageEvaluations
from app.models import Employees

class Users(db.Model):
    """
        Modelo de la tabla Usuarios
    """

    # Nombre de la tabla
    __tablename__ = 'users'

    # Columnas
    id_users = db.Column(
                UUID(as_uuid = True),
                primary_key = True,
                default = uuid.uuid4(),
                unique = True,
                nullable = True
            )

    internal_user = db.Column(
                db.Integer,
                nullable = True
            )

    username = db.Column(
                db.Integer,
                nullable = True
            )

    password = db.Column(
                db.String(150),
                nullable = True
            )

    created_user = db.Column(
                db.DateTime,
                default = datetime.now(),
                nullable = True
            )

    # Foreign Key
    id_employees = db.Column(
                UUID(as_uuid = True)
            )

    id_category = db.Column(
                UUID(as_uuid = True)
            )

    id_manage_evaluation = db.Column(
                UUID(as_uuid = True) 
            )

    def __init__(self, 
            internal_user: int, 
            username: int, 
            id_employees: uuid.UUID,
            id_category: uuid.UUID,
            id_manage_evaluation: uuid.UUID
        ):
        self.id_users = uuid.uuid4()
        self.internal_user = internal_user
        self.username = username
        self.created_user = datetime.now()
        self.id_employees = id_employees
        self.id_category = id_category
        self.id_manage_evaluation = id_manage_evaluation

    def __repr__(self):
        return f"<User {self.id_users}>"

    def encrypt_password(self, password: str):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def validate_password(self, password: str):
        return bcrypt.check_password_hash(self.password, password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    async def delete(id: uuid.UUID):
        await Employees.delete(Users.id_employees)
        await ManageEvaluations.delete(Users.id_manage_evaluation)
        return Users.query.filter_by(id_users = id).delete()

    @staticmethod
    def by_id(id: uuid.UUID):
        return Users.query.filter_by(id_users = id).first()

    @staticmethod
    def by_username(username: int):
        return Users.query.filter_by(username = username).first()

    @staticmethod
    def by_all():
        return Users.query.all()
