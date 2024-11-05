from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
import os

load_dotenv()


host = os.getenv("DB_HOST", "localhost")
port = os.getenv("DB_PORT", "3306")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dbName = os.getenv("DB_NAME")


conectionDB = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbName}"

try:
    engine = create_engine(conectionDB, echo=True)
    # Intentar conectar
    with engine.connect() as connection:
        print("Conexión exitosa a la base de datos.")
except SQLAlchemyError as e:
    print(f"Error en la conexión a la base de datos: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection):
    cursor = dbapi_connection.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
    cursor.close()
