import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app import sqlAlchemy as db

class Tasks(db.Model):
    """
        Modelo de la tabla Tareas
    """

    # Nombre de la tabla
    __tablename__ = 'tasks'

    # Columnas
    id_task = db.Column(
                UUID(as_uuid = True),
                primary_key = True,
                default = uuid.uuid4(),
                unique = True,
                nullable = True
            )

    managers = db.Column(
                db.Integer,
                nullable = True
            )

    date_task = db.Column(
                db.DateTime,
                default = datetime.now(),
                nullable = True
            )

    id_team_leader = db.Column(
                UUID(as_uuid = True),
                
            )

    def __init__(self, managers: list, date_task: datetime, id_team_leader: uuid.UUID):
        self.id_task = uuid.uuid4()
        self.managers = managers
        self.date_task = date_task
        self.id_team_leader = id_team_leader

    def __repr__(self):
        return f"<Tasks {self.id_task}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def by_id(id: uuid.UUID):
        return Tasks.query.filter_by(id_task = id).first()

    @staticmethod
    def by_team_leader(id_team_leader: uuid.UUID):
        return Tasks.query.filter_by(id_team_leader = id_team_leader).all()

    @staticmethod
    def by_all():
        return Tasks.query.all()
