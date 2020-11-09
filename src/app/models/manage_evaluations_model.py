import uuid
from datetime import datetime
from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID
from app import sqlAlchemy as db

class ManageEvaluations(db.Model):
    """
        Modelo de la tabla Gestor de Evaluaciones
    """

    # Nombre de la tabla
    __tablename__ = 'manage_evaluations'

    # Columnas
    id_manage_evaluation = db.Column(
                UUID(as_uuid = True),
                primary_key = True,
                default = uuid.uuid4(),
                unique = True,
                nullable = True
            )

    quantity = db.Column(
                db.Integer,
                default = 0,
                nullable = True
            )

    date_last_evaluation = db.Column(
                db.DateTime,
                default = datetime.now(),
                nullable = True
            )
 
    def __init__(self):
        self.id_manage_evaluation = uuid.uuid4()
        self.quantity = 0
        self.date_last_evaluation = datetime.now()

    def __repr__(self):
        return f"<ManageEvaluations {self.id_manage_evaluation}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        self.quantity += 1
        self.date_last_evaluation = datetime.now()
        db.session.commit()

    @staticmethod
    def delete(id: uuid.UUID):
        return ManageEvaluations.query.filter_by(id_manage_evaluation = id).delete()

    @staticmethod
    def by_id(id: uuid.UUID):
        return ManageEvaluations.query.filter_by(id_manage_evaluation = id).first()

    @staticmethod
    def by_all():
        return ManageEvaluations.query.all()
