import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import sqlAlchemy as db

class ResultsEvaluation(db.Model):
    """
        Modelo de la tabla Resultados de Evaluacion
    """

    # Nombre de la tabla
    __tablename__ = 'results_evaluation'

    # Columnas
    id_results_evaluation = db.Column(
                UUID(as_uuid = True),
                primary_key = True,
                default = uuid.uuid4(),
                unique = True,
                nullable = True
            )

    salute = db.Column(
                db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None),
                nullable = True
            )

    attitude = db.Column(
                db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None),
                nullable = True
            )

    negotiation_one = db.Column(
                db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None),
                nullable = True
            )

    negotiation_two = db.Column(
                db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None),
                nullable = True
            )

    registration_one = db.Column(
                db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None),
                nullable = True
            )

    registration_two = db.Column(
                db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None),
                nullable = True
            )

    message = db.Column(
                db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None),
                default = None,
                nullable = True
            )

    closing = db.Column(
                db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None),
                default = None,
                nullable = True
            )

    result = db.Column(
                db.Numeric(precision=8, asdecimal=False, decimal_return_scale=None),
                nullable = True
            )
 
    def __init__(self,
                    salute: float,
                    attitude: float,
                    negotiation_one: float,
                    negotiation_two: float,
                    registration_one: float,
                    registration_two: float,  
                    result: float
                ):
        self.salute = salute
        self.attitude = attitude
        self.negotiation_one = negotiation_one
        self.negotiation_two = negotiation_two
        self.registration_one = registration_one
        self.registration_two = registration_two
        self.result = result

    def save(self, message: float = None, closing: float = None):
        if message == None:
            self.closing = closing
            self.message = message
            db.session.add(self)
            db.session.commit()
        elif message != None:
            self.message = message
            self.closing = closing
            db.session.add(self)
            db.session.commit()

    @staticmethod
    def by_id(id: uuid.UUID):
        return ResultsEvaluation.query.filter_by(id_results_evaluation = id).first()

    @staticmethod
    def by_all():
        return ResultsEvaluation.query.all()

