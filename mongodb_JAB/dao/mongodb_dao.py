from pymongo import MongoClient
from config.settings import MONGODB_URI, DATABASE_NAME


class MongoDBDAO:
    _instance = None

    def __new__(cls):
        # Patrón Singleton
        if cls._instance is None:
            cls._instance = super(MongoDBDAO, cls).__new__(cls)
            try:
                cls._instance.client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=2000)
                cls._instance.db = cls._instance.client[DATABASE_NAME]
                # Test de conexión rápida
                cls._instance.client.admin.command('ping')
                cls._instance.connected = True
            except Exception as e:
                print(f"Error conectando a MongoDB: {e}")
                cls._instance.connected = False
        return cls._instance

    def insert_session(self, session_data):
        if self.connected:
            self.db.sessions.insert_one(session_data)

    def insert_volume_event(self, event_data):
        if self.connected:
            self.db.volume_events.insert_one(event_data)

    def is_connected(self):
        return self.connected