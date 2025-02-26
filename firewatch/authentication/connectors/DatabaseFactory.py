import os
from django.conf import settings

# Fix Imports - Ensure absolute path
from authentication.connectors.sql_orm_connector import SQLORMDatabaseConnector
from authentication.connectors.nosql_connector import NoSQLDatabaseConnector

class DatabaseFactory:
    """Factory to dynamically return the correct database connector"""

    @staticmethod
    def get_database_connector():
        database_type = os.getenv("FIREWATCH_DB_TYPE", "SQL")

        if database_type == "SQL":
            engine = os.getenv("SQL_ENGINE", "django.db.backends.sqlite3")
            
            if engine == "django.db.backends.sqlite3":
                return SQLORMDatabaseConnector()

            return SQLORMDatabaseConnector(
                engine=os.getenv("SQL_ENGINE", "django.db.backends.postgresql"),
                name=os.getenv("DB_NAME", "firewatch_db"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "yourpassword"),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
            )

        elif database_type == "NoSQL":
            return NoSQLDatabaseConnector(os.getenv("MONGO_URI", "mongodb://localhost:27017/firewatch"))

        else:
            raise ValueError(f"Unsupported database type: {database_type}")

# Dependency injection
db_connector = DatabaseFactory.get_database_connector()
