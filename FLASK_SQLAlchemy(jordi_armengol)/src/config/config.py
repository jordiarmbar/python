import os

class Config:
    # Usamos SQLite por defecto. Se creará un archivo 'library.db' en la raíz.
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///library.db')