import uuid
from sqlalchemy.dialects.postgresql import UUID
from app import sqlAlchemy as db

class Category(db.Model):
    """
        Modelo de la tabla Categoria
    """

    # Nombre de la tabla
    __tablename__ = 'category'

    # Columnas
    id_category = db.Column(
                UUID(as_uuid = True),
                primary_key = True,
                default = uuid.uuid4(),
                unique = True,
                nullable = True
            )

    category = db.Column(
                db.String(20),
                nullable = True
            )

    def __init__(self, category: str):
        self.id_category = uuid.uuid4()
        self.category = category

    def __repr__(self):
        return f"<Category {self.id_category}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def by_id(id: uuid.UUID):
        return Category.query.filter_by(id_category = id).first()

    @staticmethod
    def by_category(category: str):
        return Category.query.filter_by(category = category).first()

    @staticmethod
    def by_all():
        return Category.query.all()
