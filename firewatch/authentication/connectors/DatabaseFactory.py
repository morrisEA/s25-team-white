import os
from django.conf import settings


from authentication.connectors.sql_orm_connector import SQLORMDatabaseConnector
from authentication.connectors.nosql_connector import NoSQLDatabaseConnector

class DatabaseFactory:
    """Factory to dynamically return the correct database connector"""

    @staticmethod
    def get_database_connector():
        database_type = os.getenv("FIREWATCH_DB_TYPE", "SQL").upper()

        if database_type == "SQL":
            sql_engine = os.getenv("SQL_ENGINE", "django.db.backends.sqlite3")

            if sql_engine == "django.db.backends.sqlite3":
                return SQLORMDatabaseConnector()  
            
            return SQLORMDatabaseConnector()  

        elif database_type == "NOSQL":
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/firewatch")
            return NoSQLDatabaseConnector(mongo_uri) 

        else:
            raise ValueError(f"Unsupported database type: {database_type}")

# Dependency injection
db_connector = DatabaseFactory.get_database_connector()
