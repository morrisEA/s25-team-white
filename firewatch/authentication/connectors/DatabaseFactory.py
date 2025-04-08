import os

from authentication.connectors.SQL import SQLORMDatabaseConnector
from authentication.connectors.nosql_connector import NoSQLDatabaseConnector

class DatabaseFactory:
    """Factory to dynamically return the correct database connector"""

    @staticmethod
    def get_database_connector():
        database_type = os.getenv("FIREWATCH_DB_TYPE", "SQL").upper()

        if database_type == "AUTO":
            # Prefer PostgreSQL if configured
            sql_engine = os.getenv("SQL_ENGINE", "")
            db_host = os.getenv("DB_HOST", "")
            if sql_engine == "django.db.backends.postgresql" and db_host:
                return SQLORMDatabaseConnector()

            # Fallback to MongoDB if available
            mongo_uri = os.getenv("MONGO_URI", "")
            if mongo_uri:
                return NoSQLDatabaseConnector(mongo_uri)

            # Fallback to SQLite
            return SQLORMDatabaseConnector()

        elif database_type == "SQL":
            sql_engine = os.getenv("SQL_ENGINE", "django.db.backends.sqlite3")
            return SQLORMDatabaseConnector()

        elif database_type == "NOSQL":
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/firewatch")            
            return NoSQLDatabaseConnector(mongo_uri)
        elif database_type == "SQLITE": 
            os.environ["SQL_ENGINE"] = "django.db.backends.sqlite3"
            os.environ["DB_NAME"] = os.environ.get("DB_NAME", "db.sqlite3")
            return SQLORMDatabaseConnector()

        else:
            raise ValueError(f"Unsupported database type: {database_type}")
