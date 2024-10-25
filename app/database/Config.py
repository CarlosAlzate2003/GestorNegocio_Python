from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()


host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
dbName = os.getenv("DB_NAME")

conectionDB = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{dbName}"
engine = create_engine(conectionDB, echo=True)

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
