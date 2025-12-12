import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config.config import Config

# 1. Creamos el Engine (el punto de entrada a la BD)
engine = sa.create_engine(Config.DATABASE_URI, echo=True) # echo=True para ver las queries en consola

# 2. Creamos la "Clase Base" para nuestros modelos
Base = declarative_base()

# 3. Creamos la factoría de Sesiones
Session = sessionmaker(bind=engine)

# 4. Creamos una instancia de sesión para usar en la app
session = Session()