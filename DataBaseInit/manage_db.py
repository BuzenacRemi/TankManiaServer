from sqlalchemy import create_engine
from sqlalchemy.sql import text
import os

def get_database_url():
    username = os.getenv('POSTGRES_USER')
    password = os.getenv('POSTGRES_PASSWORD')
    host = "postgres"
    port = "5432"
    database = os.getenv('POSTGRES_DB')
    return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}"

DATABASE_URL = get_database_url()
engine = create_engine(DATABASE_URL, echo=True)


def create_db_user(username, password):
    with engine.connect() as connection:
        with connection.begin() as transaction:
            try:
                # Création de l'utilisateur
                create_user_sql = text(f"CREATE USER {username} WITH PASSWORD :password")
                connection.execute(create_user_sql, {'password': password})

                # Attribution des permissions
                grant_read_sql = text(f"GRANT pg_read_all_data TO {username}")
                connection.execute(grant_read_sql)
                grant_write_sql = text(f"GRANT pg_write_all_data TO {username}")
                connection.execute(grant_write_sql)

                print(f"User {username} created and granted read/write permissions.")
            except Exception as e:
                print(f"An error occurred: {e}")
                transaction.rollback()
                return
            else:
                transaction.commit()

