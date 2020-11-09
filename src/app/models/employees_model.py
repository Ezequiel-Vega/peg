import uuid
from sqlalchemy.orm import backref
from sqlalchemy.dialects.postgresql import UUID
from app import sqlAlchemy as db

class Employees(db.Model):
    """
        Modelo de la tabla empleados
    """

    # Nombre de la tabla
    __tablename__ = 'employees'

    # Columnas
    id_employees = db.Column(
                UUID(as_uuid = True),
                primary_key = True,
                default = uuid.uuid4(),
                unique = True,
                nullable = True
            )

    name = db.Column(
                db.String(15),
                nullable = True
            )

    last_name = db.Column(
                db.String(15),
                nullable = True
            )
 
    def __init__(self, name: str, last_name: str):
        self.id_employees = uuid.uuid4()
        self.name = name
        self.last_name = last_name

    def __repr__(self):
        return f"<Employees {self.id_employees}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def delete(id: uuid.UUID):
        return Employees.query.filter_by(id_employees = id).delete()

    @staticmethod
    def by_id(id: uuid.UUID):
        return Employees.query.filter_by(id_employees = id).first()

    @staticmethod
    def by_all():
        return Employees.query.all()
