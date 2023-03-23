import os

from pymongo import MongoClient


class MongoDB():
    """
    Environment Variables:
        MONGODB__PATH
        MONGODB__DBNAME
    """
    client: None
    db: None

    def connect_to_database(self, mongo_path=None, db_name=None):
        mongo_path = mongo_path or os.getenv('MONGODB__PATH')
        db_name = db_name or os.getenv('MONGODB__DBNAME')
        self.client = MongoClient(mongo_path)
        assert self.client.config.command('ping')['ok'] == 1.0
        self.db = self.client[db_name]


mongodb = MongoDB()
