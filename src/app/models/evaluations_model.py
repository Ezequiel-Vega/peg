import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String
from sqlalchemy import ARRAY
from app import sqlAlchemy as db

class Evaluations(db.Model):
    """
        Modelo para la tabla Evaluaciones
    """

    # Nombre de la tabla
    __tablaname__ = "evaluations"

    # Columnas
    id_evaluations = db.Column(
                UUID(as_uuid = True),
                primary_key = True,
                default = uuid.uuid4(),
                unique = True,
                nullable = True
            )

    observations = db.Column(
                db.Text,
                nullable = True
            )

    corrections = db.Column(
                db.ARRAY(String),
                nullable = True
            )

    # Foreign Key
    id_data_evaluation = db.Column(
                UUID(as_uuid = True)
                            )

    id_results_evaluation = db.Column(
                UUID(as_uuid = True),
                
            )

    id_users = db.Column(
                UUID(as_uuid = True),
                
            )

    def __init__(self, observations: str, corrections: list, 
                        id_data_evaluation: uuid.UUID, id_results_evaluation: uuid.UUID, id_user: uuid.UUID):
        self.observations = observations
        self.corrections = corrections
        self.id_data_evaluation = id_data_evaluation
        self.id_results_evaluation = id_results_evaluation
        self.id_users = id_user
        self.id_evaluations = uuid.uuid4()

    def __repr__(self):
        return f"<Evaluations {self.id_evaluations}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def by_id_user(id_user: uuid.UUID):
        return Evaluations.query.filter_by(id_users = id_user).all()

    @staticmethod
    def by_id(id: uuid.UUID):
        return Evaluations.query.filter_by(id_evaluations = id).first()

    @staticmethod
    def by_all():
        return Evaluations.query.all()
