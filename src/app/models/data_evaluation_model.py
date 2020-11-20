import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app import sqlAlchemy as db

class DataEvaluations(db.Model):
    """
        Modelo de la tabla Datos de la Evaluacion
    """

    # Nombre de la tabla
    __tablename__ = 'data_evaluations'

    # Columnas
    id_data_evaluation = db.Column(
                UUID(as_uuid = True),
                primary_key = True,
                default = uuid.uuid4(),
                unique = True,
                nullable = True
            )

    number_internal = db.Column(
                db.Integer,
                nullable = True
            )

    phone = db.Column(
                db.String(15),
                nullable = True
            )

    default = db.Column(
                db.String(20),
                nullable = True
            )

    contact = db.Column(
                db.String(20),
                nullable = True
            )

    date_evaluation = db.Column(
                db.DateTime,
                default = datetime.now(),
                nullable = True
            )

    date_audio = db.Column(
                db.DateTime,
                default = datetime.now(),
                nullable = True
            )

    name_audio = db.Column(
                db.String(100),
                nullable = True
            )
 
    def __init__(self,
                    number_internal: int,
                    phone: str,
                    contact: str,
                    date_evaluation: datetime,
                    date_audio: datetime,
                    name_audio: str,
                    default: str = None
                ):
        self.number_internal = number_internal
        self.phone = phone
        self.default = default
        self.contact = contact
        self.date_evaluation = date_evaluation
        self.date_audio = date_audio
        self.name_audio = name_audio
        self.id_data_evaluation = uuid.uuid4()

    def __repr__(self):
        return f"<DataEvaluations {self.id_data_evaluation}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def by_id(id: uuid.UUID):
        return DataEvaluations.query.filter_by(id_data_evaluation = id).first()

    @staticmethod
    def by_all():
        return DataEvaluations.query.all()
