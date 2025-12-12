from sqlalchemy import Column, Integer, String, Float
from src.config.db import Base


class Book(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = 'books'

    # Definición de columnas (Atributos de clase mapeados a columnas)
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Float)

    # Opcional: Para que se imprima bonito si haces print()
    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author}')>"