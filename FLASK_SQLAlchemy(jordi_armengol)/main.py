from flask import Flask
from src.api.routes import init_api_routes
from src.config import db
# Importante: Importar el modelo para que SQLAlchemy sepa que existe al crear tablas
from src.models.book import Book

app = Flask(__name__)

# Creamos las tablas en la base de datos basándonos en los modelos
# Esto equivale al "create_all" mencionado en los apuntes [cite: 303]
db.Base.metadata.create_all(db.engine)

# Inicializamos las rutas
init_api_routes(app)

if __name__ == '__main__':
    # Ejecutamos en modo debug para ver errores detallados
    app.run(debug=True, port=5000)